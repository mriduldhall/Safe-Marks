from enum import Enum

from HelperLibrary.MarkSheet import _MarkSheet
from HelperLibrary.StorageFunctionsDatabase import StorageFunctions


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
        # student_data = retrievedata(name)
        # student = Student(student_data.split('§')[0], student_data.split('§')[1], student_data.split('§')[2], student_data.split('§')[6])
        # student.summer_mark_sheet = _MarkSheet(student_data.split('§')[3], student_data.split('§')[4], student_data.split('§')[5], student_data.split('§')[6], student_data.split('§')[7], student_data.split('§')[8], student_data.split('§')[9])
        # student.spring_mark_sheet = _MarkSheet(student_data.split('§')[10], student_data.split('§')[11], student_data.split('§')[12], student_data.split('§')[13], student_data.split('§')[14], student_data.split('§')[15], student_data.split('§')[16])
        # student.autumn_mark_sheet = _MarkSheet(student_data.split('§')[17], student_data.split('§')[18], student_data.split('§')[19], student_data.split('§')[20], student_data.split('§')[21], student_data.split('§')[22], student_data.split('§')[23])
        # return student
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
        # DataStorage = StorageFunctionsDatabase("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", self.name + "§" + self.age + "§" + self.year_group + "§" + self.summer_mark_sheet.student + "§" + self.summer_mark_sheet.term + "§" + self.summer_mark_sheet.year_group + "§" + self.summer_mark_sheet.teacher + "§" + str(self.summer_mark_sheet.math_grade) + "§" + str(self.summer_mark_sheet.science_grade) + "§" + str(self.summer_mark_sheet.english_grade) + "§" + self.spring_mark_sheet.student + "§" + self.spring_mark_sheet.term + "§" + self.spring_mark_sheet.year_group + "§" + self.spring_mark_sheet.teacher + "§" + str(self.spring_mark_sheet.math_grade) + "§" + str(self.spring_mark_sheet.science_grade) + "§" + str(self.spring_mark_sheet.english_grade) + "§" + self.autumn_mark_sheet.student + "§" + self.autumn_mark_sheet.term + "§" + self.autumn_mark_sheet.year_group + "§" + self.autumn_mark_sheet.teacher + "§" + str(self.autumn_mark_sheet.math_grade) + "§" + str(self.autumn_mark_sheet.science_grade) + "§" + str(self.autumn_mark_sheet.english_grade) + "§\n")
        # DataStorage.append()

        # StorageFunctionsDatabase("students", [self.name, self.age, self.year_group]).append("(name, age, current_year_group)")
        # student_data = StorageFunctionsDatabase("students", self.name).retrieve("name")
        # StorageFunctionsDatabase("mark_sheets", [self.summer_mark_sheet.teacher, self.summer_mark_sheet.math_grade, self.summer_mark_sheet.science_grade, self.summer_mark_sheet.english_grade, student_data[0], StorageFunctionsDatabase("terms", "Summer").retrieve("term"), self.year_group]).append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)")
        # StorageFunctionsDatabase("mark_sheets", [self.spring_mark_sheet.teacher, self.spring_mark_sheet.math_grade, self.spring_mark_sheet.science_grade, self.spring_mark_sheet.english_grade, student_data[0], StorageFunctionsDatabase("terms", "Spring").retrieve("term"), self.year_group]).append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)")
        # StorageFunctionsDatabase("mark_sheets", [self.autumn_mark_sheet.teacher, self.autumn_mark_sheet.math_grade, self.autumn_mark_sheet.science_grade, self.autumn_mark_sheet.english_grade, student_data[0], StorageFunctionsDatabase("terms", "Autumn").retrieve("term"), self.year_group]).append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)")

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
        # data, location = retrievedata(self.name)
        # Delete = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", "")
        # Delete.update(location)
        # print(self.name, "successfully deleted!")
        # return True, False
        student_data = StorageFunctions("students").retrieve(["name"], [self.name])
        student_id = (student_data[0])[0]
        StorageFunctions("mark_sheets").delete(student_id, "student_id")
        StorageFunctions("students").delete(student_id)


def retrievedata(name):
    # name = name.lower()
    # name = name.capitalize()
    # SearchingName = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", name)
    # data, location = SearchingName.retrieve(1)
    # return data, location

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
