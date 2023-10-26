from datetime import timedelta


class Event:
    def __init__(
        self,
        title,
        date,
        priority,
        event_type,
        estimated_duration=1,
        deadline=None,
        start_time=None,
        end_time=None,
    ):
        self.title = title
        self.date = date
        self.priority = priority
        self.event_type = event_type
        # Possible Event Types: Homework, Exam, simple task, recurrent task
        self.estimated_duration = estimated_duration
        self.deadline = deadline
        self.start_time = start_time
        self.end_time = end_time


class Calendar:
    def __init__(self):
        self.scheduled_events = []
        self.unscheduled_events = []

    def event_type_processing(self):
        for event in self.events:
            type = event.event_type
            match type:
                case "Task":
                    return
                    # do smth
                case _:
                    return
                    # do smth

    def find_optimal_time_slot(self):
        for event in self.unscheduled_events:
            # do smth
            return

    def add_to_cal(self, event):
        self.unscheduled_events.append(event)

    def remove_from_cal(self, event):
        self.scheduled_events.remove(event)


# [!] To-do next time:
# 1. Mypy
# 2. list out possible occurences for all attributes in event object
# 3. take a crack at some heuristic if possible
