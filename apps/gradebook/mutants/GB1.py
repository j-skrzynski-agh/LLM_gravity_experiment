"""Mutant GB1: brak sprawdzania skali ocen"""
class Gradebook:
    def __init__(self) -> None:
        self._assignments = {}    # name -> (weight, kind)
        self._grades = {}         # (student, assignment) -> grade

    def add_assignment(self, name, weight, kind="homework"):
        self._assignments[name] = (weight, kind)

    def record(self, student, assignment, grade):
        self._grades[(student, assignment)] = grade

    def average(self, student):
        entries = []
        for name, (weight, kind) in self._assignments.items():
            grade = self._grades.get((student, name), 2.0)
            entries.append((grade, weight, kind))
        quizzes = [e for e in entries if e[2] == "quiz"]
        if len(quizzes) > 1:
            entries.remove(min(quizzes, key=lambda e: e[0]))
        total = sum(g * w for g, w, _ in entries) / sum(w for _, w, _ in entries)
        return round(total, 2)
