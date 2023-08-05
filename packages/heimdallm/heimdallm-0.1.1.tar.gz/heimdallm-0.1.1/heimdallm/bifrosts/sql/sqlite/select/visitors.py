import math
from collections import defaultdict as dd
from typing import MutableMapping, Optional

from lark import Token, Transformer, Tree, Visitor

from ... import exc
from ...utils import FqColumn, JoinCondition, RequiredConstraint
from ..utils.identifier import get_identifier
from ..utils.visitors import AliasCollector


class Facets:
    """this simple class is used to collect all of the facets of a query, so
    that we can easily validate them with a constraint validator"""

    def __init__(self) -> None:
        # tables that were joined but do not reference the table in the join
        # condition. if this list has values, validation fails.
        self.bad_joins: list[str] = []
        # the table selected in the FROM clause. this will always be set after a
        # successful parse
        self.selected_table: Optional[str] = None
        # the tables joined to the query, this could include the table selected
        # in the FROM clause, if there are JOINs in the query
        self.joined_tables: MutableMapping[str, set[JoinCondition]] = dd(set)
        # the columns selected in the query
        self.selected_columns: set[FqColumn] = set()
        # the columns used in the WHERE, JOIN, HAVING, and ORDER BY clauses
        self.condition_columns: set[FqColumn] = set()
        # the required conditions in the WHERE and JOIN clauses, used to
        # constrain the query so that it is safe
        self.required_constraints: set[RequiredConstraint] = set()
        # all of the functions used in the query
        self.functions: set[str] = set()
        # the row limit of the query
        self.limit = math.inf


class FacetCollector(Visitor):
    """collects all of the facets of the query that we care about. this will
    feed directly into the constraint validator"""

    def __init__(self, facets: Facets, collector: AliasCollector):
        self._collector = collector
        self._facets = facets

    def _resolve_column(self, node):
        if node.data == "column_alias":
            maybe_alias = get_identifier(node)
            table, column = self._collector._aliased_columns.get(
                maybe_alias, (None, maybe_alias)
            )
            return table, column

        # should never happen
        raise RuntimeError(f"unknown column reference type: {type(node)}")

    def _resolve_table(self, table_ref):
        if isinstance(table_ref, Tree):
            if table_ref.data == "aliased_table":
                table_name = get_identifier(table_ref)
                return table_name

            elif table_ref.data == "table_name":
                # we have no way of knowing if this is an alias or not, other
                # than testing for its existence in the collector's alias map
                maybe_alias = get_identifier(table_ref)
                table = self._collector._aliased_tables.get(maybe_alias, maybe_alias)
                return table

        elif isinstance(table_ref, Token):
            return table_ref.value

        # should never happen
        raise RuntimeError(f"unknown table reference type: {type(table_ref)}")

    def join(self, node):
        if join_type := list(node.find_data("illegal_join")):
            join_type = join_type[0].children[0].type
            raise exc.IllegalJoinType(join_type=join_type)

        joined_table = node.children[1].children[0]
        joined_table_name = self._resolve_table(joined_table)

        # if a required_comparison node exists, it means it is actually required
        # (enforced by the grammar, see grammar comments). a required comparison has
        # a placeholder for the RHS
        for required_comparison in node.find_data("required_comparison"):
            self._add_required_comparison(required_comparison)

        for condition in node.find_data("connecting_join_condition"):
            # from_table may be an alias, but from_column will always be authoritative.
            # the LHS of the join condition is always a fully-qualified column
            from_fq_column_node = condition.children[0]
            from_table_node, from_column_node = from_fq_column_node.children
            from_column = get_identifier(from_column_node)
            from_table = self._resolve_table(from_table_node)

            # conditions in a join are compared against are allowed conditions, so
            # record the LHS
            self._collect_condition_column(from_fq_column_node)

            # to_table may be an alias, but to_column will always be authoritative.
            # the RHS of the join condition can be a `value` rule.
            to_fq_column_node = condition.children[2]

            # token? it's probably a string or number, keep going
            if isinstance(to_fq_column_node, Token):
                continue
            # not a fq column? it's probably a function or something nested, keep going.
            elif (
                isinstance(to_fq_column_node, Tree)
                and to_fq_column_node.data != "fq_column"
            ):
                continue

            to_table, to_column_node = to_fq_column_node.children
            to_column = get_identifier(to_column_node)

            to_table = self._resolve_table(to_table)

            # the joined table must be one of the parts of the join condition
            if joined_table_name != from_table and joined_table_name != to_table:
                self._facets.bad_joins.append(joined_table_name)
                continue

            # conditions in a join are compared against are allowed conditions, so
            # record the RHS
            self._collect_condition_column(to_fq_column_node)

            # our join represents two sides, the from table and the to table.
            # we'll record both in our joined_tables set.
            join_spec = JoinCondition(
                f"{from_table}.{from_column}",
                f"{to_table}.{to_column}",
            )
            self._facets.joined_tables[from_table].add(join_spec)
            self._facets.joined_tables[to_table].add(join_spec)

    def selected_table(self, node):
        table_node = list(node.find_data("table_name"))[0]
        table_name = get_identifier(table_node)
        self._facets.selected_table = table_name

    def selected_column(self, node):
        child = node.children[0]

        if isinstance(child, Token) and child.type == "COUNT_STAR":
            return

        elif isinstance(child, Token) and child.type == "ALL_COLUMNS":
            raise exc.IllegalSelectedColumn(column="*")

        elif isinstance(child, Tree):
            # if it's an aliased column, we need to ensure that the thing being aliased
            # isn't a non-fully-qualified column. we do that by looking for
            # `column_alias`
            if child.data == "aliased_column":
                alias_child = child.children[0]
                # if we're aliasing COUNT(*), it's safe to ignore, since it doesn't
                # reveal any of the underlying values
                if isinstance(alias_child, Token) and alias_child.type == "COUNT_STAR":
                    return

                if list(alias_child.find_data("column_alias")):
                    alias = get_identifier(alias_child)
                    raise exc.UnqualifiedColumn(column=alias)

            # if the column looks like a column alias (meaning a non-fully-qualified
            # column), then that's an error, because we only work with fully-qualified
            # columns
            elif child.data == "column_alias":
                alias = get_identifier(child)
                raise exc.UnqualifiedColumn(column=alias)

            # if we're not an aliased column, but we contain a column alias somewhere,
            # that's an error, because we only work with fully-qualified columns
            elif column_alias := list(child.find_data("column_alias")):
                alias = get_identifier(column_alias[0])
                raise exc.UnqualifiedColumn(column=alias)

            # if we've made it this far, we're sure we're dealing with a fully-qualified
            # column, or a non-column based expression
            try:
                table_node = next(child.find_data("table_name"))
            # it's some non-column expression, which we don't care about
            except StopIteration:
                pass
            # there's a fully qualified column there, so we'll record it
            else:
                table_name = self._resolve_table(table_node)
                # column_name will always be authoritative, even if it is aliased in
                # this node
                column_name = get_identifier(list(child.find_data("column_name"))[0])
                self._facets.selected_columns.add(
                    FqColumn(
                        table=table_name,
                        column=column_name,
                    )
                )

    def _add_required_comparison(self, node):
        """takes a node representing a required comparison and adds it to the
        facets"""
        maybe_fq_column_node, placeholder = node.children
        placeholder_name = placeholder.children[0].value

        if maybe_fq_column_node.data == "column_alias":
            table_name, column_name = self._resolve_column(maybe_fq_column_node)

        elif maybe_fq_column_node.data == "fq_column":
            fq_column_node = maybe_fq_column_node
            table_node, column_node = fq_column_node.children

            table_name = self._resolve_table(table_node)
            column_name = get_identifier(column_node)
        else:
            raise RuntimeError(
                f"Unknown required column type {type(maybe_fq_column_node)}"
            )

        self._facets.required_constraints.add(
            RequiredConstraint(
                column=f"{table_name}.{column_name}",
                placeholder=placeholder_name,
            )
        )

    def where_clause(self, where_node: Tree):
        """here we'll do a breadth-first search on the where clause, going level
        by level. if any level contains an "OR", that means the entire level is
        tainted and can't be used for a required constraint, because the
        required constraint may be optional.

        if a level is tainted, then all of its children (WHERE subclauses) are
        tainted as well, so we will not process them.

        the end result is that we only collect a required comparison node IFF it
        is not joined by an OR anywhere in the WHERE clause, either at its
        level, or at any level above it. only then can we know that the
        comparison is actually constraining to the query"""
        conditions = where_node.children[1]
        stack: list[Tree] = [conditions]

        while stack:
            conditions = stack.pop()

            level_stack: list[Tree] = []
            for child in conditions.children:
                if isinstance(child, Token):
                    # is the level tainted? if so, clear the stack and exit the loop
                    if child.type == "WHERE_TYPE" and child.value.lower() == "or":
                        level_stack = []
                        break
                elif isinstance(child, Tree):
                    level_stack.append(child)

            for child in reversed(level_stack):
                stack.append(child)
                if child.data == "required_comparison":
                    self._add_required_comparison(child)

    def _collect_condition_column(self, node):
        """here we'll parse out the columns that are referenced anywhere in the
        WHERE, regardless of the depth of the expression. we care if a column is being
        referenced at all, even optionally, because that will be checked against the
        allowlist"""
        for fq_column_node in node.find_data("fq_column"):
            table_node, column_node = fq_column_node.children
            table_name = self._resolve_table(table_node)
            column_name = get_identifier(column_node)
            self._facets.condition_columns.add(
                FqColumn(
                    table=table_name,
                    column=column_name,
                )
            )

        for column_alias_node in node.find_data("column_alias"):
            table_name, column_name = self._resolve_column(column_alias_node)
            if not table_name:
                # no table name AND no column name means the inserted alias is an alias
                # for a non-column expression, like `COUNT(*) as thing`. this is valid
                # as it is, so we don't raise, and we don't track it as a condition
                # column.
                if not column_name:
                    pass
                else:
                    raise exc.UnqualifiedColumn(column=column_name)
            self._facets.condition_columns.add(
                FqColumn(
                    table=table_name,
                    column=column_name,
                )
            )

    where_condition = _collect_condition_column
    having_condition = _collect_condition_column
    order_column = _collect_condition_column

    def limit(self, node):
        self._facets.limit = float(node.children[0].value)

    def function_name(self, node):
        self._facets.functions.add(node.children[0].value.lower())


class AmbiguityResolver(Transformer):
    """this transformer's purpose is to resolve ambiguities in the parse tree
    that can only be resolved through some extra knowledge that would be
    difficult to embed in the grammar itself.
    """

    def __init__(self, query: str):
        self.query = query
        super().__init__()

    def test_alias(self, i, tree, trees) -> bool:
        """
        This resolves ambiguities in the parse tree related to aliases. For
        example, the following query is ambiguous:

            select t1.secret from t1 left join t2 on t1.jid = t2.jid

        Is "left" an alias for "t1", or is it part of the "left join"? It's
        ambiguous. We know it's not ambiguous because "left" is a keyword, but
        the parser can't know this. This class resolves those ambiguities by
        looking at all possible ambiguous parse trees in the ambiguity, and
        selecting only the one that does not have an alias conflict with a
        reserved keyword.
        """
        for alias_node in tree.find_data("generic_alias"):
            try:
                get_identifier(alias_node)
            except exc.ReservedKeyword:
                return False
        return True

    def test_req_comparisons(self, i, tree, trees) -> bool:
        """in a where_condition rule, the children can include
        `relational_comparison` and `required_comparison` rules, which are
        ambiguous, because required comparisons are a subset of relational
        comparisons. we always prefer to interpret the ambiguity as a required
        comparison though, because it is more strict, and it satisfies our
        required comparison validator constraints"""
        if tree.data in ("where_condition", "join_condition"):
            return tree.children[0].data == "required_comparison"
        return True

    def test_arith_expr(self, i, tree, trees) -> bool:
        """the arith_expr node is recursive, so it can be ambiguous. just choose the
        first parse of it, since this node doesn't really matter"""
        if tree.data == "arith_expr":
            return i == 0
        return True

    def _ambig(self, trees):
        def test_tree(i, tree):
            return (
                self.test_alias(i, tree, trees)
                and self.test_req_comparisons(i, tree, trees)
                and self.test_arith_expr(i, tree, trees)
            )

        pruned_trees = [tree for i, tree in enumerate(trees) if test_tree(i, tree)]

        if len(pruned_trees) == 0:
            raise exc.InvalidQuery(query=self.query)
        elif len(pruned_trees) == 1:
            return pruned_trees[0]
        else:
            raise exc.AmbiguousParse(trees=pruned_trees, query=self.query)
