"""Mutant PL3: wygrywa opcja z ostatniego głosu"""
class Poll:
    def __init__(self, question: str) -> None:
        self.question = question
        self._options = []
        self._votes = {}          # voter -> option

    def add_option(self, option):
        self._options.append(option)

    def vote(self, voter, option):
        if option not in self._options:
            raise ValueError("unknown option")
        if voter in self._votes:
            raise ValueError("already voted")
        self._votes[voter] = option

    def winner(self):
        if len(self._votes) < 3:
            return None
        counts = {o: 0 for o in self._options}
        for o in self._votes.values():
            counts[o] += 1
        return list(self._votes.values())[-1]
