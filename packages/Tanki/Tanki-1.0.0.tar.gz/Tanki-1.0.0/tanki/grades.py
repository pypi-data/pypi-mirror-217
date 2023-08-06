from .grade_details import GradeDetails

class Grades:
    def __init__(self, data: dict):
        self.mk1: GradeDetails = GradeDetails(None)
        self.mk2: GradeDetails = GradeDetails(None)
        self.mk3: GradeDetails = GradeDetails(None)
        self.mk4: GradeDetails = GradeDetails(None)
        self.mk5: GradeDetails = GradeDetails(None)
        self.mk6: GradeDetails = GradeDetails(None)
        self.mk7: GradeDetails = GradeDetails(None)

        for grade in data:
            setattr(self, f'mk{grade["grade"]+1}', GradeDetails(grade))