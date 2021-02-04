from Interface.StudentCommandLineInterface import CLI
from HelperLibrary.StorageFunctions import StorageFunctions
from HelperLibrary.MarkSheet import MarkSheet

from datetime import datetime


class StudentController:
    def __init__(self, student, table_name):
        self.student = student
        self.table_name = table_name

    def retrievedata(self):
        self.student.name = (self.student.name.lower()).capitalize()
        student_data = StorageFunctions("students").retrieve(["name"], [self.student.name])
        student_data = list(student_data[0])
        student_id = student_data[0]
        year_group_id = student_data[3]
        del student_data[0]
        term_id_list = StorageFunctions("terms").list("id")
        for term_id in term_id_list:
            mark_sheet_data = StorageFunctions("mark_sheets").retrieve(["student_id", "term_id", "year_group_id"], [student_id, term_id, year_group_id])
            term_data = StorageFunctions("terms").retrieve(["id"], [term_id])
            term = [(term_data[0])[1]]
            student_data = student_data + term + list((mark_sheet_data[0])[1:5])
        return student_data

    def validate_if_student_exists(self):
        student_data = StorageFunctions(self.table_name).retrieve(["name"], [self.student.name])
        if not student_data:
            return False
        else:
            return True

    def list_students(self):
        list_of_students = StorageFunctions(self.table_name).list("name")
        print("List of students:")
        counter = 1
        for student_name in sorted(list_of_students):
            print(counter, ":", student_name, end="\n")
            counter += 1

    def create_student(self):
        StorageFunctions(self.table_name).append("(name, age, current_year_group, date_of_birth, address, father_name, mother_name)", [self.student.name, self.student.age, self.student.year_group, self.student.date_of_birth, self.student.address, self.student.father_name, self.student.mother_name])
        student_data = StorageFunctions(self.table_name).retrieve(["name"], [self.student.name])
        student_data = student_data[0]
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.summer_mark_sheet.teacher, self.student.summer_mark_sheet.math_grade, self.student.summer_mark_sheet.science_grade, self.student.summer_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Summer"])[0])[0], self.student.year_group])
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.spring_mark_sheet.teacher, self.student.spring_mark_sheet.math_grade, self.student.spring_mark_sheet.science_grade, self.student.spring_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Spring"])[0])[0], self.student.year_group])
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.autumn_mark_sheet.teacher, self.student.autumn_mark_sheet.math_grade, self.student.autumn_mark_sheet.science_grade, self.student.autumn_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Autumn"])[0])[0], self.student.year_group])

    def validate_student_details(self):
        if self.student.age < 1:
            return False, "Invalid age!"
        elif self.student.year_group < 1:
            self.student.year_group = 1
            return True, "Age too low!\nSetting year group to 1"
        elif self.student.year_group > 13:
            self.student.year_group = 13
            return True, "Age too high!\nSetting year group to 13"
        else:
            return True, None

    @staticmethod
    def _choosemarksheet(activity):
        mark_sheet_choice_dictionary = {'1': 'Summer', '2': 'Spring', '3': 'Autumn'}
        while True:
            print("Enter 1 to", activity, "the summer term mark sheet, 2 for spring term mark sheet and 3 for autumn term mark sheet", end='')
            mark_sheet_choice = mark_sheet_choice_dictionary.get(input())
            if not mark_sheet_choice:
                print("Please enter a valid choice")
            else:
                return mark_sheet_choice

    def editmarksheet(self):
        mark_sheet_choice = self._choosemarksheet("edit")
        self.student.__getattribute__(mark_sheet_choice.lower() + "_mark_sheet").editmarksheet()

    def getstudentdetails(self):
        print("Student name:", self.student.name)
        print("Student age:", self.student.age)
        print("Student year group:", self.student.year_group)

    def getmarksheetdetails(self):
        mark_sheet_choice = self._choosemarksheet("get details of")
        MarkSheet.getdetails(getattr(self.student, mark_sheet_choice.lower() + "_mark_sheet"))

    def getmarksheetmarks(self):
        mark_sheet_choice = self._choosemarksheet("get marks of")
        MarkSheet.getmarks(getattr(self.student, mark_sheet_choice.lower() + "_mark_sheet"))

    def savestudentdata(self):
        student_data = StorageFunctions("students").retrieve(["name"], [self.student.name])
        student_id = (student_data[0])[0]
        StorageFunctions("students").update(["name", "age"], [self.student.name, self.student.age], student_id)
        term_id_list = StorageFunctions("terms").list("id")
        for term_id in term_id_list:
            mark_sheet_data = StorageFunctions("mark_sheets").retrieve(["student_id", "term_id", "year_group_id"], [student_id, term_id, self.student.year_group])
            mark_sheet_id = (mark_sheet_data[0])[0]
            term_data = StorageFunctions("terms").retrieve(["id"], [term_id])
            term = (term_data[0])[1]
            StorageFunctions("mark_sheets").update(["teacher", "math_mark", "science_mark", "english_mark"], [getattr(self.student, term.lower() + "_mark_sheet").teacher, getattr(self.student, term.lower() + "_mark_sheet").math_grade, getattr(self.student, term.lower() + "_mark_sheet").science_grade, getattr(self.student, term.lower() + "_mark_sheet").english_grade], mark_sheet_id)

    def deletestudent(self):
        student_data = StorageFunctions("students").retrieve(["name"], [self.student.name])
        student_id = (student_data[0])[0]
        StorageFunctions("mark_sheets").delete(student_id, "student_id")
        StorageFunctions("students").delete(student_id)


class Student:
    def __init__(self, name, date_of_birth, address, father_name, mother_name, teacher, table_name="students"):
        self.name = name
        self.age = (datetime.now()).year - date_of_birth.year
        self.year_group = self.age - 5
        self.date_of_birth = date_of_birth
        self.address = address
        self.father_name = father_name
        self.mother_name = mother_name
        self.summer_mark_sheet = MarkSheet(self.name, "Summer", self.year_group, teacher)
        self.spring_mark_sheet = MarkSheet(self.name, "Spring", self.year_group, teacher)
        self.autumn_mark_sheet = MarkSheet(self.name, "Spring", self.year_group, teacher)
        self.student_controller = StudentController(self, table_name)
        self.student_menu_dict = {'1': self.student_controller.editmarksheet,
                                  '2': self.student_controller.getstudentdetails,
                                  '3': self.student_controller.getmarksheetdetails,
                                  '4': self.student_controller.getmarksheetmarks,
                                  }
        self.admin_student_menu_dict = {'1': self.student_controller.editmarksheet,
                                        '2': self.student_controller.getstudentdetails,
                                        '3': self.student_controller.getmarksheetdetails,
                                        '4': self.student_controller.getmarksheetmarks,
                                        '5': self.delete,
                                        }

    def recreatestudent(self):
        student_data = self.student_controller.retrievedata()
        self.name = student_data[0]
        self.age = student_data[1]
        self.year_group = student_data[2]
        self.summer_mark_sheet.student = self.name
        self.summer_mark_sheet.term = student_data[3]
        self.summer_mark_sheet.year_group = self.year_group
        self.summer_mark_sheet.teacher = student_data[4]
        self.summer_mark_sheet.math_grade = student_data[5]
        self.summer_mark_sheet.science_grade = student_data[6]
        self.summer_mark_sheet.english_grade = student_data[7]
        self.spring_mark_sheet.student = self.name
        self.spring_mark_sheet.term = student_data[8]
        self.spring_mark_sheet.year_group = self.year_group
        self.spring_mark_sheet.teacher = student_data[9]
        self.spring_mark_sheet.math_grade = student_data[10]
        self.spring_mark_sheet.science_grade = student_data[11]
        self.spring_mark_sheet.english_grade = student_data[12]
        self.autumn_mark_sheet.student = self.name
        self.autumn_mark_sheet.term = student_data[13]
        self.autumn_mark_sheet.year_group = self.year_group
        self.autumn_mark_sheet.teacher = student_data[14]
        self.autumn_mark_sheet.math_grade = student_data[15]
        self.autumn_mark_sheet.science_grade = student_data[16]
        self.autumn_mark_sheet.english_grade = student_data[17]

    def create(self):
        if not self.student_controller.validate_if_student_exists():
            self.student_controller.create_student()
            return "Student successfully created"
        else:
            return "Student already exists"

    def manage(self, admin):
        choice_list_of_students = bool(int(input("Enter 1 to get a list of all students and 0 to continue without a list of students:")))
        if choice_list_of_students:
            self.student_controller.list_students()
        self.name = input("Enter student name to manage student:").capitalize()
        if self.student_controller.validate_if_student_exists():
            self.recreatestudent()
            CLI(self, admin).initiate()
            return "Exiting..."
        else:
            return "Student does not exist"

    def delete(self):
        self.student_controller.deletestudent()
