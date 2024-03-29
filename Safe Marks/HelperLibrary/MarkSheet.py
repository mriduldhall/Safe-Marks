class MarkSheet:
    def __init__(self, student, term, year_group, math_grade=0, science_grade=0, english_grade=0):
        self.student = student
        self.term = term
        self.year_group = year_group
        self.math_grade = math_grade
        self.science_grade = science_grade
        self.english_grade = english_grade

    def edit_mark_sheet(self):
        continuation_check = True
        while continuation_check:
            subject_list = ["math", "science", "english"]
            choice = input("Enter 1 if you would like to edit math grade, 2 to edit science grade, 3 to edit english grade and 4 to stop editing the mark sheet")
            if (choice > str(len(subject_list)+1)) or (choice < "1"):
                print("Enter valid choice!")
            elif choice == str(len(subject_list)+1):
                continuation_check = False
            else:
                print("Current", subject_list[int(choice)-1], "grade is", getattr(self, subject_list[int(choice)-1] + "_grade"))
                print("Enter new", subject_list[int(choice)-1], "grade:", end='')
                setattr(self, (subject_list[int(choice)-1] + "_grade"), input())
        self.get_marks()

    def get_details(self):
        print("Student name =", self.student)
        print("Term =", self.term)
        print("Year group =", self.year_group)

    def get_marks(self):
        print("Maths marks =", self.math_grade)
        print("English marks =", self.science_grade)
        print("Science marks =", self.english_grade)
