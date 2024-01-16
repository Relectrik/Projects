from exercise_clause import ExerciseClause
import itertools
from copy import deepcopy


class ExerciseKnowledgeBase:
    """
    Specifies a simple, Conjunctive Normal Form Propositional
    Logic Knowledge Base for use in soreness tracking in muscles.
    """

    def __init__(self) -> None:
        """
        Initializes a new ExerciseKnowledgeBase, which will be used to track the
        soreness levels of muscles, but is also structured more generally to track
        ExerciseClauses of any kind.

        It begins as an empty knowledgebase with no contained clauses.
        """
        self.clauses: set["ExerciseClause"] = set()

    def tell(self, clause: "ExerciseClause") -> None:
        """
        Adds the given clause to the CNF ExerciseKnowledgeBase

        Parameters:
            clause (ExerciseClause):
                A new ExerciseClause to add to this knowledgebase
        """
        self.clauses.add(clause)

    def ask(self, query: "ExerciseClause") -> bool:
        """
        Given an ExerciseClause query, returns True if the KB entails the query,
        False otherwise. Uses the proof by contradiction technique.

        Parameters:
            query (ExerciseClause):
                The query clause to determine if this is entailed by the KB

        Returns:
            bool:
                True if the KB entails the query, False otherwise
        """

        working_clauses: set["ExerciseClause"] = deepcopy(self.clauses)
        for alpha_prop in query.props.items():
            working_clauses.add(ExerciseClause([(alpha_prop[0], not alpha_prop[1])]))

        new_clauses: set["ExerciseClause"] = set()

        while True:
            for clause_1, clause_2 in itertools.combinations(working_clauses, 2):
                resolvents: set["ExerciseClause"] = ExerciseClause.resolve(
                    clause_1, clause_2
                )

                if any(resolvent.is_empty() for resolvent in resolvents):
                    return True
                new_clauses |= resolvents

            if new_clauses <= working_clauses:
                return False
            working_clauses |= new_clauses

    def __len__(self) -> int:
        """
        Returns the number of clauses currently stored in the KB

        Returns:
            int:
                The number of stored clauses
        """
        return len(self.clauses)

    def __str__(self) -> str:
        """
        Converts the KB into its string presentation, printing out ALL
        contained clauses in set format.

        Returns:
            str:
                All clauses in the KB converted to their str format
        """
        return str([str(clause) for clause in self.clauses])
