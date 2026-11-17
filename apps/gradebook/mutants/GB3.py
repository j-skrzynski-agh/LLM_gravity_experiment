"""Mutant GB3: średnia zwykła zamiast ważonej"""
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
        if len(quizzes) > 1:
            entries.remove(min(quizzes, key=lambda e: e[0]))
        total = sum(g for g, _, _ in entries) / len(entries)
        return round(total, 2)
