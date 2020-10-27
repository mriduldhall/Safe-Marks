class _MarkSheet:
    def __init__(self, student, term, year_group, teacher, math_grade=0, science_grade=0, english_grade=0):
        self.student = student
        self.term = term
        self.year_group = year_group
        self.teacher = teacher
        self.math_grade = math_grade
        self.science_grade = science_grade
        self.english_grade = english_grade

    def editmarksheet(self):

        def stop():
            return False

        continuation_check = True
        while continuation_check:
            marksheeteditingvariables = {'1': "math_grade", '2': "science_grade", '3': "english_grade", '4': stop}
            marksheeteditingstrings = {'1': "math", '2': "science", '3': "english"}
            choice = input("Enter 1 if you would like to edit math grade, 2 to edit science grade, 3 to edit english grade and 4 to stop editing the mark sheet")
            try:
                continuation_check = marksheeteditingvariables[choice]()
            except TypeError:
                print("Current", marksheeteditingstrings[choice], "grade is", getattr(self, marksheeteditingvariables[choice]))
                print("Enter new", marksheeteditingstrings[choice], "grade:", end='')
                new_grade = input()
                setattr(self, marksheeteditingvariables[choice], new_grade)

    def getdetails(self):
        print("Student name =", self.student)
        print("Term =", self.term)
        print("Year group =", self.year_group)
        print("Teacher name =", self.teacher)

    def getmarks(self):
        print("Maths marks =", self.math_grade)
        print("English marks =", self.science_grade)
        print("Science marks =", self.english_grade)


if __name__ == "__main__":
    mark_sheet = _MarkSheet("Mridul", "Summer term", "9", "Test")
    mark_sheet.editmarksheet()
    mark_sheet.getdetails()
    mark_sheet.getmarks()
