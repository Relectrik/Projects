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

## Day 3 1/11/2024
Since the logic for the knowledge base is working, it will accurately give me truth values that pertain to whether the muscle is able to be worked out or not. Now I can start on the Soreness Aggregator class. 

This should be able to:
* Record soreness onto a CSV file to keep track of my soreness over a period of time.
* It should be able to decide what workout I should do, or not do depending on the soreness levels of my muscles by leveraging the knowledge base.
* It should also be able to aggregate my past soreness levels to determine my workout volume that I should be undertaking per muscle group.


```
class SorenessAggregator:
    def __init__(self, soreness_record: str) -> None:
        self.soreness_record: pd.DataFrame = pd.read_csv(soreness_record)

    def record_soreness(self) -> None:
        soreness: List[Union[int, dt.date]]
        cleaned_soreness = (
            input(
                "Enter space separated soreness rating between 0-2 for the following muscles in that order: ch, t, fd, sd, rd, ba, bi, q, h, ca"
            )
            .replace(" ", "")
            .split(",")
        )
        soreness = [int(soreness_rating) for soreness_rating in cleaned_soreness]

        if len(soreness) == 7:
            soreness.append(dt.datetime.now().date())

        self.soreness_record.add(soreness)

    def decide_workout(self) -> set():
        pass

    def calculate_volume(self, workout_record: pd.DataFrame) -> pd.DataFrame:
        self.soreness_record.sort_values(by="Date")
        prev_week_soreness = self.soreness_record.tail(7)

        for row in prev_week_soreness:
            # do some calculation to aggregate previous week's score
            pass

```

After populating the appropriate methods, I simply need to find a heuristic for determining how I want the volume of the workout to be calculated based upon the soreness levels in the past week.

## Day 4 1/12/2024
Here is an example entry of 7 days from the soreness_record.csv file:
(Each of the soreness levels are between 0 - 2 to not overcomplicate the heuristic)

```
Chest, Triceps, Front Deltoid, Side Deltoid, Rear Deltoid, Back, Biceps, Quadriceps, Hamstring, Calves, Date
1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1/12/2024
0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1/13/2024
0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1/14/2024
1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 1/15/2024
2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1/16/2024
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1/17/2024
1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1/18/2024
```

In this example, I do a push day (targets chest, triceps, front and side delt) before the record starts, and so my soreness levels that pertain to those muscles is a 1, so the algorithm chooses a pull day (back, biceps, rear delt) for me to perform. The next day, I record my soreness levels from the previous day, and so it chooses a leg day and so on. Notice, on the 16th, all my muscles have a soreness level, which is why you see that the next day that nothing is sore. The program, provided with the soreness levels of that day, suggested that I should do a break day to account for that.

### Aggregator Heuristic

Now let's figure out the logic for calculating volume from the entries above. I don't want the aggregator to take more than the last 7 days of information, because those soreness levels refer to workouts with different volumes. 

We can observe that if we add up the last 7 days of soreness levels for the chest, it will result in the number 5. The rest of the muscles will be: 5, 5, 5, 2, 2, 2, 4, 4, 4. Obviously in a more realistic circumstance, there will be more variation to the individual muscles in the bigger muscle group (e.g. the chest will likely be more sore than the side deltoids because the side deltoids can take more volume in a period of time).

Thus, we can set some ranges of total soreness levels over the past week to determine what the volume of the next workout should be for that same muscle. If the muscle has had a total soreness that exceeds 4, we know that the current volume is affecting the muscle enough such that it *requires* recovery days, but if the muscle only feels kinda sore the next day, the next session must increase the volume for that muscle accordingly. These are relatively arbritrary from my own experience, but in pseudocode:

```
(per muscle)
soreness = 0
for entry in previous 7 days:
    soreness += entry
if soreness < 2:
    set_count += 2
elif soreness > 2 and soreness < 4:
    set_count += 1
```