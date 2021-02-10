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
            student_data = student_data + term + list((mark_sheet_data[0])[1:4])
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
        StorageFunctions("mark_sheets").append("(math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.summer_mark_sheet.math_grade, self.student.summer_mark_sheet.science_grade, self.student.summer_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Summer"])[0])[0], self.student.year_group])
        StorageFunctions("mark_sheets").append("(math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.spring_mark_sheet.math_grade, self.student.spring_mark_sheet.science_grade, self.student.spring_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Spring"])[0])[0], self.student.year_group])
        StorageFunctions("mark_sheets").append("(math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [self.student.autumn_mark_sheet.math_grade, self.student.autumn_mark_sheet.science_grade, self.student.autumn_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Autumn"])[0])[0], self.student.year_group])

    def create_mark_sheets(self):
        student_id = StorageFunctions("students").retrieve(["name"], [self.student.name])[0][0]
        term_id_list = StorageFunctions("terms").list("id")
        term_name_list = StorageFunctions("terms").list("term")
        for term_id in term_id_list:
            mark_sheets_data = StorageFunctions("mark_sheets").retrieve(["student_id", "term_id", "year_group_id"], [student_id, term_id, self.student.year_group])
            if not mark_sheets_data:
                StorageFunctions("mark_sheets").append("(math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [0, 0, 0, student_id, term_id, self.student.year_group])
                self.student.__setattr__(term_name_list[term_id_list.index(term_id)].lower() + "_mark_sheet", MarkSheet(self.student.name, term_name_list[term_id_list.index(term_id)].lower(), self.student.year_group))

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

    def getstudentdetails(self):
        print("Student name:", self.student.name)
        print("Student age:", self.student.age)
        print("Student year group:", self.student.year_group)
        print("Student date of birth:", self.student.date_of_birth)
        print("Student address:", self.student.address)
        print("Student father's name:", self.student.father_name)
        print("Student mother's name:", self.student.mother_name)

    def getmarksheetdetails(self):
        mark_sheet_choice = self._choosemarksheet("get details of")
        MarkSheet.getdetails(getattr(self.student, mark_sheet_choice.lower() + "_mark_sheet"))

    def getmarksheetmarks(self):
        mark_sheet_choice = self._choosemarksheet("get marks of")
        MarkSheet.getmarks(getattr(self.student, mark_sheet_choice.lower() + "_mark_sheet"))

    def editmarksheet(self):
        mark_sheet_choice = self._choosemarksheet("edit")
        self.student.__getattribute__(mark_sheet_choice.lower() + "_mark_sheet").editmarksheet()

    def edit_student_details(self):
        attributes = {
            '1': self.edit_name,
            '2': self.edit_year_group,
            '3': self.edit_date_of_birth,
            '4': self.edit_address,
            '5': self.edit_father_name,
            '6': self.edit_mother_name,
        }
        exit_initiated = False
        while not exit_initiated:
            edit_option = input("Enter 1 to edit name, 2 to edit year group, 3 to edit date of birth, 4 to edit address, 5 to edit father name, 6 to edit mother name and 7 to exit:")
            if edit_option == str(len(attributes) + 1):
                exit_initiated = True
            elif (edit_option > str(len(attributes) + 1)) or (edit_option < '1'):
                print("Please enter a valid choice!")
            else:
                attributes.get(edit_option)()

    def edit_name(self):
        valid_name = False
        while not valid_name:
            original_name = self.student.name
            print("Student's current name is", self.student.name)
            self.student.name = input("Enter new name for student:")
            if not self.validate_if_student_exists():
                valid_name = True
                self.savestudentdata(original_name)
            else:
                print("Student already exists!")
                self.student.name = original_name

    def edit_year_group(self):
        print("Student's current year group is", self.student.year_group)
        self.student.year_group = int(input("Enter new year group for student:"))
        self.create_mark_sheets()

    def edit_date_of_birth(self):
        print("Student's current date of birth is", self.student.date_of_birth)
        birth_year = int(input("Enter new year of birth:"))
        birth_month = int(input("Enter new month of birth:"))
        birth_date = int(input("Enter new date of birth:"))
        self.student.date_of_birth = datetime(birth_year, birth_month, birth_date)
        self.student.age = self.student.calculate_age()

    def edit_address(self):
        print("Student's current address is", self.student.address)
        self.student.address = input("Enter new address of student:")

    def edit_father_name(self):
        print("Student's father's current name is", self.student.father_name)
        self.student.father_name = input("Enter new name for student's father:")

    def edit_mother_name(self):
        print("Student's father's current name is", self.student.mother_name)
        self.student.mother_name = input("Enter new name for student's mother:")

    def savestudentdata(self, old_name=None, save_mark_sheet_data=True):
        if not old_name:
            student_data = StorageFunctions("students").retrieve(["name"], [self.student.name])
        else:
            student_data = StorageFunctions("students").retrieve(["name"], [old_name])
        student_id = (student_data[0])[0]
        StorageFunctions("students").update(["name", "age", "current_year_group", "date_of_birth", "address", "father_name", "mother_name"], [self.student.name, self.student.age, self.student.year_group, self.student.date_of_birth, self.student.address, self.student.father_name, self.student.mother_name], student_id)
        if save_mark_sheet_data:
            term_id_list = StorageFunctions("terms").list("id")
            for term_id in term_id_list:
                mark_sheet_data = StorageFunctions("mark_sheets").retrieve(["student_id", "term_id", "year_group_id"], [student_id, term_id, self.student.year_group])
                mark_sheet_id = (mark_sheet_data[0])[0]
                term_data = StorageFunctions("terms").retrieve(["id"], [term_id])
                term = (term_data[0])[1]
                StorageFunctions("mark_sheets").update(["math_mark", "science_mark", "english_mark"], [getattr(self.student, term.lower() + "_mark_sheet").math_grade, getattr(self.student, term.lower() + "_mark_sheet").science_grade, getattr(self.student, term.lower() + "_mark_sheet").english_grade], mark_sheet_id)

    def deletestudent(self):
        student_data = StorageFunctions("students").retrieve(["name"], [self.student.name])
        student_id = (student_data[0])[0]
        StorageFunctions("mark_sheets").delete(student_id, "student_id")
        StorageFunctions("students").delete(student_id)


class Student:
    def __init__(self, name, date_of_birth, address, father_name, mother_name, table_name="students"):
        self.name = name
        self.date_of_birth = date_of_birth
        if self.date_of_birth is not None:
            self.age = self.calculate_age()
            self.year_group = (StorageFunctions("year_groups").retrieve(["year_group"], [self.age-4])[0])[0]
        else:
            self.age = None
            self.year_group = None
        self.address = address
        self.father_name = father_name
        self.mother_name = mother_name
        self.summer_mark_sheet = MarkSheet(self.name, "Summer", self.year_group)
        self.spring_mark_sheet = MarkSheet(self.name, "Spring", self.year_group)
        self.autumn_mark_sheet = MarkSheet(self.name, "Spring", self.year_group)
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
                                        '5': self.student_controller.edit_student_details,
                                        '6': self.delete,
                                        }

    def recreatestudent(self):
        student_data = self.student_controller.retrievedata()
        self.name = student_data[0]
        self.age = student_data[1]
        self.year_group = student_data[2]
        self.date_of_birth = student_data[3]
        self.address = student_data[4]
        self.father_name = student_data[5]
        self.mother_name = student_data[6]
        self.summer_mark_sheet.student = self.name
        self.summer_mark_sheet.term = student_data[7]
        self.summer_mark_sheet.year_group = self.year_group
        self.summer_mark_sheet.math_grade = student_data[8]
        self.summer_mark_sheet.science_grade = student_data[9]
        self.summer_mark_sheet.english_grade = student_data[10]
        self.spring_mark_sheet.student = self.name
        self.spring_mark_sheet.term = student_data[11]
        self.spring_mark_sheet.year_group = self.year_group
        self.spring_mark_sheet.math_grade = student_data[12]
        self.spring_mark_sheet.science_grade = student_data[13]
        self.spring_mark_sheet.english_grade = student_data[14]
        self.autumn_mark_sheet.student = self.name
        self.autumn_mark_sheet.term = student_data[15]
        self.autumn_mark_sheet.year_group = self.year_group
        self.autumn_mark_sheet.math_grade = student_data[16]
        self.autumn_mark_sheet.science_grade = student_data[17]
        self.autumn_mark_sheet.english_grade = student_data[18]

    def calculate_age(self):
        current_date = datetime.now()
        age = current_date.year - self.date_of_birth.year
        if current_date.month < self.date_of_birth.month:
            age -= 1
        elif current_date.day < self.date_of_birth.day:
            age -= 1
        return age

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
