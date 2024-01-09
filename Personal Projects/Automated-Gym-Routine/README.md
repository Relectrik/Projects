# Automated Gym Routine

## Project Overview
I personally find it cumbersome to do trivial tasks that have deterministic outcomes myself because of how much time I waste doing it everyday. I believe that automating these tasks with code is an investment into saving time in the future. One such time waster is constructing an exercise routine for the gym.

I am a huge advocate for Renaissance Periodization, which is a group that focuses efforts towards sharing scientific research in digestible ways to the general public to optimize workouts. As such, I wanted to utilize algorithmic paradigms I know to build a project that automates creating a gym routine for you based on your soreness levels and RP's ideals.

As a brief overview, the program should be able to take the individual's soreness levels per muscle group, and intelligently decide which exercises you should do based on what muscles are not sore. However, it should also be able to aggregate your recent soreness levels for your individual muscles to decide whether to change your volume (set count) for the exercise.

## Day 0 | 1/7/24
Thus far, I've only thought about the project abstractly and realized that the amount of time I take to decide these things and create spreadsheets for my routines can be done automatically.

I also want to note that I use ChatGPT as my assistant when I work on projects. I understand that it can't get code right every single time, but it is useful when I want something trivial to be done that I do not want to waste my time with. I used it in this project to create a CSV file to hold exercises that pertain to a particular muscle group so that my program will be able to fetch one when needed.

## Day 1 | 1/8/24
I've built out a rough outline of my project:
<img src="Flowchart for Automated Gym Project.jpg" alt="Flowchart" width="800"/>
### Motivations
**The Knowledge Base**
From a previous academic project in my Artifical Intelligence class, we utilized propositional logic (e.g. $\neg P$) stored in Conjunctive Normal Form within a Knowledge Base for querying to navigate a Blind Bot within a maze of pitfalls. We would use proof by contradiction to query whether a new proposition is in line with the KB's current knowledge. Since this project is also deterministic (e.g. if your chest is sore you are not working that out), we can utilize this paradigm within the context of this project.

* Example KB:

    * $\neg Ch$

    * $\neg T$

    * $\neg SD$

    * $Q$

    * $H$
    
    * $Ca$

This example knowledge base indicates to us that the chest, triceps, and side deltoids are NOT sore, whereas the quadriceps, hamstrings, and calves ARE sore, such that when we query it with an example routine (e.g. $Ch \land T \land SD$), we would assume to the contrary, convert to CNF, then ask our knowledge base whether this results in a contradiction.

**How do I implement progression based on soreness level?**

* Knowledge Base only needs booleans to determine WHICH muscles to target

* Therefore, I need some other tracking to determine volume increases based on previous workout's soreness levels (tracked through CSV file, where entries can also be vectorized)

* KB determines WHAT exercises to do based on muscle groups that are NOT sore.

**How to determine set count based on soreness record?**

* Needs to aggregate (based on a heuristic) past days soreness levels to then decide how much to increment next session's set count.

## Day 2 | 1/9/24
I have finished implementing the ExerciseClause object such that it can now hold whether a muscle is sore or not. It is in the form: $Ch$ or $\neg Ch$, which represents whether the chest is able to be worked out or not, or whether the chest is not sore or is respectively. 

In code:

```
            ExerciseClause([("Ch", True)])
            ExerciseClause([("T", True)])
            ExerciseClause([("Sd", False)])
```
which is represented as a dictionary:
```
            {
                ("Ch" : True),
                ("T" : True),
                ("Sd" : False)
            }
```
which indicates that the chest and triceps are not sore, while the side deltoid is.

Furthermore, I have also implemented the knowledge base that will hold these clauses, which is simply a set that holds these clauses to be told and queried for the context of doing a predetermined routine for the day aka don't exercise a muscle that is sore on that day.

Here's how we query:
```
def ask(self, query: "ExerciseClause") -> bool:
        """
        Given a ExerciseClause query, returns True if the KB entails the query,
        False otherwise. Uses the proof by contradiction technique detailed
        during the lectures.

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
```

It's quite an unoptimized way to perform proof by contradiction on the knowledge base to check if the proposed query is entailed by the KB, however since the KB will have a maximum of 10-15 statements to inidicate the soreness of each muscle, there is a limit to the nested loop.