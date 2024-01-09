# TODO: Convert KB to context of exercises
from typing import *


class ExerciseClause:
    def __init__(self, props: Sequence[tuple]) -> None:
        """
        Constructs a new ExerciseClause from the given list of MazePropositions,
        which are thus assumed to be disjoined in the resulting clause (by
        definition of a clause). After checking that the resulting clause isn't
        valid (i.e., vacuously true, or logically equivalent to True), stores
        the resulting props mapped to their truth value in a dictionary.

        Example:
            The clause: P(1,1) v P(2,1) v ~P(1,2):
            ExerciseClause([
                (("P", (1, 1)), True),
                (("P", (2, 1)), True),
                (("P", (1, 2)), False)
            ])

            Will thus be converted to a dictionary of the format:

            {
                ("P", (1, 1)): True,
                ("P", (2, 1)): True,
                ("P", (1, 2)): False
            }

        Parameters:
            props (Sequence[tuple]):
                A list of maze proposition tuples of the format:
                ((symbol, location), truth_val), e.g.
                (("P", (1, 1)), True)
        """
        self.props: dict[str, bool] = dict()
        self.valid: bool = False

        for prop in props:
            if len(self.props) > 0:
                if prop[0] in self.props and prop[1] != self.props.get(prop[0]):
                    self.valid = True
                    self.props = dict()
                    break
            self.props[prop[0]] = prop[1]

    def get_prop(self, prop: str) -> Optional[bool]:
        """
        Returns the truth value of the requested proposition if it exists
        in the current clause.

        Returns:
            - None if the requested prop is not in the clause
            - True if the requested prop is positive in the clause
            - False if the requested prop is negated in the clause
        """
        return None if prop not in self.props else self.props.get(prop)

    def is_valid(self) -> bool:
        """
        Determines if the given ExerciseClause is logically equivalent to True
        (i.e., is a valid or vacuously true clause like (P(1,1) v P(1,1))

        Returns:
            - True if this clause is logically equivalent with True
            - False otherwise
        """
        return self.valid

    def is_empty(self) -> bool:
        """
        Determines whether or not the given clause is the "empty" clause,
        i.e., representing a contradiction.

        Returns:
            - True if this is the Empty Clause
            - False otherwise
            (NB: valid clauses are not empty)
        """
        return (not self.valid) and (len(self.props) == 0)

    def __eq__(self, other: Any) -> bool:
        """
        Defines equality comparator between ExerciseClauses: only if they
        have the same props (in any order) or are both valid or not

        Parameters:
            other (Any):
                The other object being compared

        Returns:
            bool:
                Whether or not other is a ExerciseClause with the same props
                and valid status as the current one
        """
        if other is None:
            return False
        if not isinstance(other, ExerciseClause):
            return False
        return (
            frozenset(self.props) == frozenset(other.props)
            and self.valid == other.valid
        )

    def __hash__(self) -> int:
        """
        Provides a hash for a ExerciseClause to enable set membership

        Returns:
            int:
                Hash code for the current set of props and valid status
        """
        return hash((frozenset(self.props.items()), self.valid))

    def _prop_str(self, prop: str) -> str:
        """
        Returns a string representing a single prop, in the format: (X,(1, 1))

        Parameters:
            prop (tuple[str, tuple[int, int]]):
                The proposition being stringified, like ("P" (1,1))

        Returns:
            str:
                Stringified version of the given prop
        """
        return f"{prop}"

    def __str__(self) -> str:
        """
        Returns a string representing a ExerciseClause in the format:
        {(X, (1,1)):True v (Y, (1,1)):False v (Z, (1,1)):True}

        Returns:
            str:
                Stringified version of this ExerciseClause's props and mapped truth vals
        """
        if self.valid:
            return "{True}"
        result = "{"
        for prop in self.props:
            result += self._prop_str(prop) + ":" + str(self.props.get(prop)) + " v "
        return result[:-3] + "}"

    def __len__(self) -> int:
        """
        Returns the number of propositions in this clause

        Returns:
            int:
                The number of props in this clause
        """
        return len(self.props)

    @staticmethod
    def resolve(c1: "ExerciseClause", c2: "ExerciseClause") -> set["ExerciseClause"]:
        """
        Returns the set of non-valid ExerciseClauses that result from applying
        resolution to the two input.

        [!] We return a set of ExerciseClauses for ease of dealing with sets in
        other contexts (like in MazeKnowledgeBase) even though the set
        will only ever contain 0 or 1 resulting ExerciseClauses.

        Parameters:
            c1, c2 (ExerciseClause):
                The two ExerciseClauses being resolved.

        Returns:
            set[ExerciseClause]:
                There are 2 possible types of results:
                - {}: The empty set if either c1 and c2 do NOT resolve (i.e., have
                  no propositions shared between them that are negated in one but
                  not the other) or if the result of resolution yields valid clauses
                - {some_clause}: where some_clause is a non-valid clause either
                  containing propositions OR is the empty clause in the case that
                  c1 and c2 yield a contradiction.
        """
        if c1.props == c2.props:
            return set()

        common_props = set(c1.props.keys()) & set(c2.props.keys())

        if len(common_props) == 0:
            return set()

        for match in common_props:
            if c1.props[match] != c2.props[match]:
                new_clause = ExerciseClause(
                    [
                        (prop, negation)
                        for prop, negation in c1.props.items()
                        if prop != match
                    ]
                    + [
                        (prop, negation)
                        for prop, negation in c2.props.items()
                        if prop != match
                    ]
                )

                return set() if new_clause.is_valid() else set([new_clause])

        return set()
