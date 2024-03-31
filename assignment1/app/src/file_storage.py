import json
import os


class EventFileManager:
    FILE_PATH = r"C:\Users\Harry\Desktop\Python Assignment\assignment1\event.json"

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                events = json.load(file)
        except FileNotFoundError:
            events = []
        return events

    @classmethod
    def write_events_to_file(cls, events):
        try:
            with open(cls.FILE_PATH, 'w') as file:
                json.dump(events, file, indent=4)
        except Exception as e:
            print(f"There was an error writing the file: {e}")




