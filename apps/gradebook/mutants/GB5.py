"""Mutant GB5: brakujące oceny pomijane"""
class Gradebook:
    def __init__(self) -> None:
        self._assignments = {}    # name -> (weight, kind)
        self._grades = {}         # (student, assignment) -> grade

    def add_assignment(self, name, weight, kind="homework"):
        self._assignments[name] = (weight, kind)

    def record(self, student, assignment, grade):
        if not 2.0 <= grade <= 5.0:
            raise ValueError("grade outside the scale")
        self._grades[(student, assignment)] = grade

    def average(self, student):
        entries = []
        for name, (weight, kind) in self._assignments.items():
            if (student, name) in self._grades:
                entries.append((self._grades[(student, name)], weight, kind))
        quizzes = [e for e in entries if e[2] == "quiz"]
        if len(quizzes) > 1:
            entries.remove(min(quizzes, key=lambda e: e[0]))
        total = sum(g * w for g, w, _ in entries) / sum(w for _, w, _ in entries)
        return round(total, 2)
