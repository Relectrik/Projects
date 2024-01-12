import pandas as pd
import datetime as dt
import exercise_clause as EC
import exercise_kb as EKB
from typing import List
from typing import Union


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
