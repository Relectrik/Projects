from soreness_aggregator import SorenessAggregator as SA
from typing import List, Union
import pandas as pd
import datetime as dt


class RoutineAutomator:
    def __init__(self, workout_record: str, soreness_record: str) -> None:
        """
        Initializes new Automator class that will automatically provide routines
        with progression based on past workouts.

        Parameters:
            workout_record (str): File path for workout_record.csv
            soreness_record (str): File path for soreness_record.csv
        """
        self.workout_record: pd.DataFrame = pd.read_csv(workout_record)
        self.aggregator: SA = SA(soreness_record, workout_record)

        self.workout_record["Date"] = pd.to_datetime(self.workout_record["Date"])

        self.workout_record.sort_values(by="Date")

        self.loop = 0

    def give_workout(self) -> None:
        """
        Main workhorse for automator class. Utilizes SorenessAggregator to
        record and aggregate soreness such that it provides a set of muscles to
        work that day, in conjunction with its new volume and a user-chosen
        progression (Weight, Rep count, RIR) for that day.

        Prints:
            dict[str, Union[int, dt.datetime]]: The new entry for the workout_record.csv and
            the information required to perform your workout
        """
        self.aggregator.record_soreness()
        approved_muscle_groups: List[str] = self.aggregator.decide_muscles()
        if not approved_muscle_groups:
            print("Do not workout today")
            return
        muscle_index = input(
            f"Choose which one (by index starting 0) of these workouts you would like to do: {approved_muscle_groups} \n"
        )

        for muscle in approved_muscle_groups[int(muscle_index)]:
            new_entry: dict[str, Union[int, dt.datetime]] = self._progress(
                self._get_last_workout_by_muscle(muscle)
            )
            new_entry["Date"] = pd.to_datetime(dt.datetime.now())
            self.workout_record.loc[len(self.workout_record)] = new_entry
            print(new_entry)

        self.workout_record.to_csv("data/workout_record.csv", index=False, mode="w")

    def _get_last_workout_by_muscle(
        self, muscle: str
    ) -> dict[str, Union[int, dt.datetime]]:
        """
        Private helper method to return the most recent entry in the CSV/Dataframe
        pertaining to the muscle being queried.

        Parameters:
            muscle (str): Muscle being queried

        Returns:
            dict[str, Union[int, dt.datetime]]: Most recent dataframe workout entry for that muscle.
        """
        sorted_workout_record: pd.DataFrame = self.workout_record.sort_values(
            by="Date", ascending=False
        )
        return (
            sorted_workout_record[sorted_workout_record["Muscle Group"] == muscle]
            .iloc[0]
            .to_dict()
        )

    def _progress(
        self, last_workout: dict[str, Union[int, dt.datetime]]
    ) -> dict[str, Union[int, dt.datetime]]:
        """
        Private helper method to decide which attribute of the workout to progress
        for the next session.

        Parameters:
            last_workout (dict[str, Union[int, dt.datetime]]): Information from last workout
            to progress from.

        Returns:
            dict[str, Union[int, dt.datetime]]: Information for new workout to progress to.
        """
        progress_options = ["Weight", "RIR", "Reps"]
        to_progress_index: str = input(
            f"Which of {progress_options} would you like to progress for {last_workout['Muscle Group']}?"
        )
        to_progress: str = progress_options[int(to_progress_index)]

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
        return last_workout
