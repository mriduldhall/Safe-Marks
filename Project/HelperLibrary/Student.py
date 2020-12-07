from enum import Enum

from HelperLibrary.MarkSheet import _MarkSheet
from HelperLibrary.StorageFunctions import StorageFunctions


class AllowedMarkSheetChoice(Enum):
    Summer = '1'
    Spring = '2'
    Autumn = '3'


class Student:
    def __init__(self, name, age, year_group, teacher):
        self.name = name
        self.age = age
        self.year_group = year_group
        self.summer_mark_sheet = _MarkSheet(self.name, "Summer", self.year_group, teacher)
        self.spring_mark_sheet = _MarkSheet(self.name, "Spring", self.year_group, teacher)
        self.autumn_mark_sheet = _MarkSheet(self.name, "Spring", self.year_group, teacher)
        self.studentmenu_dict = {'1': Student.editmarksheet, '2': Student.getstudentdetails, '3': Student.getmarksheetdetails, '4': Student.getmarksheetmarks, '5': Student.deletestudent}

    @classmethod
    def recreatestudent(cls, name):
        student_data = retrievedata(name)
        student = Student(student_data[0], student_data[1], student_data[2], student_data[4])
        student.summer_mark_sheet = _MarkSheet(student.name, student_data[3], student.year_group, student_data[4], student_data[5], student_data[6], student_data[7])
        student.spring_mark_sheet = _MarkSheet(student.name, student_data[8], student.year_group, student_data[9], student_data[10], student_data[11], student_data[12])
        student.autumn_mark_sheet = _MarkSheet(student.name, student_data[13], student.year_group, student_data[14], student_data[15], student_data[16], student_data[17])
        return student

    def editmarksheet(self):
        mark_sheet_choice = _choosemarksheet("edit")
        self.__getattribute__(mark_sheet_choice.lower() + "_mark_sheet").editmarksheet()

    def savestudentdata(self):
        student_data = StorageFunctions("students").retrieve(["name"], [self.name])
        student_id = (student_data[0])[0]
        StorageFunctions("students").update(["name", "age"], [self.name, self.age], student_id)
        term_id_list = StorageFunctions("terms").list("id")
        for term_id in term_id_list:
            mark_sheet_data = StorageFunctions("mark_sheets").retrieve(["student_id", "term_id", "year_group_id"], [student_id, term_id, self.year_group])
            mark_sheet_id = (mark_sheet_data[0])[0]
            term_data = StorageFunctions("terms").retrieve(["id"], [term_id])
            term = (term_data[0])[1]
            StorageFunctions("mark_sheets").update(["teacher", "math_mark", "science_mark", "english_mark"], [getattr(self, term.lower() + "_mark_sheet").teacher, getattr(self, term.lower() + "_mark_sheet").math_grade, getattr(self, term.lower() + "_mark_sheet").science_grade, getattr(self, term.lower() + "_mark_sheet").english_grade], mark_sheet_id)

    def getstudentdetails(self):
        print("Student name:", self.name)
        print("Student age:", self.age)
        print("Student year group:", self.year_group)

    def getmarksheetdetails(self):
        mark_sheet_choice = _choosemarksheet("get details of")
        _MarkSheet.getdetails(getattr(self, mark_sheet_choice.lower() + "_mark_sheet"))

    def getmarksheetmarks(self):
        mark_sheet_choice = _choosemarksheet("get marks of")
        _MarkSheet.getmarks(getattr(self, mark_sheet_choice.lower() + "_mark_sheet"))

    def deletestudent(self):
        student_data = StorageFunctions("students").retrieve(["name"], [self.name])
        student_id = (student_data[0])[0]
        StorageFunctions("mark_sheets").delete(student_id, "student_id")
        StorageFunctions("students").delete(student_id)


def retrievedata(name):
    name = (name.lower()).capitalize()
    student_data = StorageFunctions("students").retrieve(["name"], [name])
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
    print(student_data)
    return student_data


def _choosemarksheet(activity):
    while True:
        try:
            mark_sheet_choice_dictionary = {'1': 'Summer', '2': 'Spring', '3': 'Autumn'}
            print("Enter 1 to", activity, "the summer term mark sheet, 2 for spring term mark sheet and 3 for autumn term mark sheet", end='')
            mark_sheet_choice = AllowedMarkSheetChoice(input())
        except ValueError:
            print("Please enter a valid choice")
        else:
            return mark_sheet_choice_dictionary[getattr(mark_sheet_choice, "value")]
