"""Mutant GB4: najgorsza kartkówka nie jest pomijana"""
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
            grade = self._grades.get((student, name), 2.0)
            entries.append((grade, weight, kind))
        quizzes = [e for e in entries if e[2] == "quiz"]
        total = sum(g * w for g, w, _ in entries) / sum(w for _, w, _ in entries)
        return round(total, 2)
