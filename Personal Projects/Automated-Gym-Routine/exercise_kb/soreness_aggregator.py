import pandas as pd
import datetime as dt
import exercise_clause as EC
import exercise_knowledge_base as EKB
from typing import List, Union


class SorenessAggregator:
    def __init__(self, soreness_record: str, workout_record: str) -> None:
        self.example_routines = [
            {"Chest", "Triceps", "Front Deltoids"},
            {"Chest", "Triceps", "Side Deltoids"},
            {"Rear Deltoids", "Back", "Biceps"},
            {"Chest", "Back", "Biceps"},
            {"Chest", "Back", "Triceps"},
            {"Quadriceps", "Hamstring", "Calves"},
        ]
        self.soreness_record: pd.DataFrame = pd.read_csv(soreness_record)
        self.workout_record: pd.DataFrame = pd.read_csv(workout_record)
        self.soreness_record.sort_values(by="Date")
        self.workout_record.sort_values(by="Date")

    def record_soreness(self) -> None:
        cleaned_soreness = (
            input(
                "Enter space separated soreness rating between 0-2 for the following muscles in that order: Chest, Triceps, Front Deltoids, Side Deltoids, Rear Deltoids, Back, Biceps, Quadriceps, Hamstring, Calves \n"
            )
            .replace(" ", "")
            .split(",")
        )
        soreness: List[Union[int, dt.date]] = [
            int(soreness_rating) for soreness_rating in cleaned_soreness
        ]

        if len(soreness) == 10:
            soreness.append(dt.datetime.now().date())

        self.soreness_record.loc[len(self.soreness_record)] = soreness

    def decide_muscles(self) -> List[str]:
        curr_kb = EKB()
        approved_workouts: List[str]

        for muscle, soreness_val in self.soreness_record.iloc[-1].iloc[:-1].items():
            curr_kb.tell(EC([(muscle, False if soreness_val > 0 else True)]))
        for routine in self.example_routines:
            working_set: set()
            for muscle in routine:
                if not curr_kb.ask(EC([(muscle, True)])):
                    working_set = set()
                    break
                else:
                    working_set.add(muscle)
            approved_workouts.append(frozenset(working_set))

        return approved_workouts

    def calculate_volume(self, muscle: str) -> int:
        prev_week_soreness: pd.DataFrame = self.soreness_record.tail(7)
        volume_increase: int = 0

        total_soreness: int = 0
        for soreness_val in prev_week_soreness[muscle].items():
            total_soreness += soreness_val[1]

        if total_soreness < 2:
            volume_increase = 2
        elif total_soreness >= 2 and total_soreness <= 4:
            volume_increase = 1

        return self._get_recent_volume_by_muscle(muscle) + volume_increase

    def _get_recent_volume_by_muscle(self, muscle: str) -> int:
        sorted_workout_record: pd.DataFrame = self.workout_record.sort_values(
            by="Date", ascending=False
        )
        return sorted_workout_record[
            sorted_workout_record["Muscle Group"] == muscle
        ].iloc[0]["Sets"]
