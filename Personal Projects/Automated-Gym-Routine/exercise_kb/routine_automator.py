from soreness_aggregator import SorenessAggregator as SA
import pandas as pd
import datetime as dt


class RoutineAutomator:
    def __init__(self, workout_record: str, soreness_record: str) -> None:
        self.workout_record: pd.DataFrame = pd.read_csv(workout_record)
        self.aggregator: SA = SA(soreness_record, workout_record)

    def give_workout(self):
        approved_muscle_groups = self.aggregator.decide_muscles()
        muscle_index = input(
            f"Choose which one (by index) of these workouts you would like to do: {approved_muscle_groups} \n"
        )

        for muscle in approved_muscle_groups[muscle_index]:
            new_entry = {
                "Muscle Group": muscle,
                "Weight": self._get_last_workout_by_muscle(muscle)["Weight"],
                "Reps": self._get_last_workout_by_muscle(muscle)["Reps"],
                "Sets": self.aggregator.calculate_volume(muscle),
                "Reps": self._get_last_workout_by_muscle(muscle)["RIR"],
                "Date": dt.datetime.now().date,
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
