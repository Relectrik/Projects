from soreness_aggregator import SorenessAggregator as SA
from typing import List
import pandas as pd
import datetime as dt
import random


class RoutineAutomator:
    def __init__(self, workout_record: str, soreness_record: str) -> None:
        self.workout_record: pd.DataFrame = pd.read_csv(workout_record)
        self.aggregator: SA = SA(soreness_record, workout_record)

        self.workout_record["Date"] = pd.to_datetime(self.workout_record["Date"])

        self.workout_record.sort_values(by="Date")

        self.loop = 0

    def give_workout(self):
        self.aggregator.record_soreness()
        approved_muscle_groups: List[str] = self.aggregator.decide_muscles()
        if not approved_muscle_groups:
            print("Do not workout today")
            return
        muscle_index = input(
            f"Choose which one (by index) of these workouts you would like to do: {approved_muscle_groups} \n"
        )

        for muscle in approved_muscle_groups[int(muscle_index)]:
            new_entry = {
                "Muscle Group": muscle,
                "Weight": self._random_progress(
                    self._get_last_workout_by_muscle(muscle)
                )["Weight"],
                "Reps": self._random_progress(self._get_last_workout_by_muscle(muscle))[
                    "Reps"
                ],
                "Sets": self.aggregator.calculate_volume(muscle),
                "RIR": self._random_progress(self._get_last_workout_by_muscle(muscle))[
                    "RIR"
                ],
                "Date": pd.to_datetime(dt.datetime.now()),
            }
            self.workout_record.loc[len(self.workout_record)] = new_entry

        self.workout_record.to_csv("data/workout_record.csv", index=False, mode="w")

    def _get_last_workout_by_muscle(self, muscle: str) -> dict[str, int]:
        sorted_workout_record: pd.DataFrame = self.workout_record.sort_values(
            by="Date", ascending=False
        )
        return (
            sorted_workout_record[sorted_workout_record["Muscle Group"] == muscle]
            .iloc[0]
            .to_dict()
        )

    def _random_progress(self, last_workout: dict[str, int]) -> dict[str, int]:
        to_progress: str = random.choice(["Weight", "RIR", "Reps"])

        match to_progress:
            case "Weight":
                last_workout.update(
                    {"Weight": last_workout["Weight"] + 5}
                    if last_workout["Weight"] < 50
                    else {"Reps": last_workout["Reps"] + 1}
                )

            case "RIR":
                last_workout.update(
                    {"RIR": last_workout["RIR"] - 1}
                    if last_workout["RIR"] > 0
                    else {"Reps": last_workout["Reps"] + 1}
                )
            case "Reps":
                last_workout["Reps"] += 1
            case _:
                pass
        print(last_workout)
        return last_workout
