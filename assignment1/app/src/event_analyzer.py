class EventAnalyzer:
    def __init__(self, events):
        self.events = events

    def get_joiners_multiple_meetings_method(self):
        multiple_meetings_joiners = set()
        all_joiners = set()

        for event in self.events:
            event_joiners = set(joiner.name for joiner in event.joiners)
            multiple_meetings_joiners.update(all_joiners.intersection(event_joiners))
            all_joiners.update(event_joiners)
        return list(multiple_meetings_joiners)
