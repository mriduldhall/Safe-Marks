from enum import Enum
from MarkSheet import _MarkSheet
from StorageFunctions import StorageFunctions


class AllowedMarkSheetChoice(Enum):
    Summer = '1'
    Spring = '2'
    Autumn = '3'


class Student:
    def __init__(self, name, age, year_group):
        self.name = name
        self.age = age
        self.year_group = year_group
        self.summer_mark_sheet = _MarkSheet(self.name, "Summer", self.year_group, "Test")
        self.spring_mark_sheet = _MarkSheet(self.name, "Spring", self.year_group, "Test")
        self.autumn_mark_sheet = _MarkSheet(self.name, "Spring", self.year_group, "Test")
        self.studentmenu_dict = {'1': Student.editmarksheet, '2': Student.getstudentdetails, '3': Student.getmarksheetdetails, '4': Student.getmarksheetmarks, '5': Student.deletestudent}

    @classmethod
    def recreatestudent(cls, name):
        student_data, location = sortbyname(name)
        student = Student(student_data.split('§')[0], student_data.split('§')[1], student_data.split('§')[2])
        student.summer_mark_sheet = _MarkSheet(student_data.split('§')[3], student_data.split('§')[4], student_data.split('§')[5], student_data.split('§')[6], student_data.split('§')[7], student_data.split('§')[8], student_data.split('§')[9])
        student.spring_mark_sheet = _MarkSheet(student_data.split('§')[10], student_data.split('§')[11], student_data.split('§')[12], student_data.split('§')[13], student_data.split('§')[14], student_data.split('§')[15], student_data.split('§')[16])
        student.autumn_mark_sheet = _MarkSheet(student_data.split('§')[17], student_data.split('§')[18], student_data.split('§')[19], student_data.split('§')[20], student_data.split('§')[21], student_data.split('§')[22], student_data.split('§')[23])
        return student

    def editmarksheet(self):
        mark_sheet_choice = _choosemarksheet("edit")
        self.__getattribute__(mark_sheet_choice.lower() + "_mark_sheet").editmarksheet()

    def savestudentdata(self):
        DataStorage = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", self.name + "§" + self.age + "§" + self.year_group + "§" + self.summer_mark_sheet.student + "§" + self.summer_mark_sheet.term + "§" + self.summer_mark_sheet.year_group + "§" + self.summer_mark_sheet.teacher + "§" + str(self.summer_mark_sheet.math_grade) + "§" + str(self.summer_mark_sheet.science_grade) + "§" + str(self.summer_mark_sheet.english_grade) + "§" + self.spring_mark_sheet.student + "§" + self.spring_mark_sheet.term + "§" + self.spring_mark_sheet.year_group + "§" + self.spring_mark_sheet.teacher + "§" + str(self.spring_mark_sheet.math_grade) + "§" + str(self.spring_mark_sheet.science_grade) + "§" + str(self.spring_mark_sheet.english_grade) + "§" + self.autumn_mark_sheet.student + "§" + self.autumn_mark_sheet.term + "§" + self.autumn_mark_sheet.year_group + "§" + self.autumn_mark_sheet.teacher + "§" + str(self.autumn_mark_sheet.math_grade) + "§" + str(self.autumn_mark_sheet.science_grade) + "§" + str(self.autumn_mark_sheet.english_grade) + "§\n")
        DataStorage.append()

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

    @staticmethod
    def savedata(student):
        data, location = sortbyname(student.name)
        DataUpdate = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", student.name + "§" + student.age + "§" + student.year_group + "§" + student.summer_mark_sheet.student + "§" + student.summer_mark_sheet.term + "§" + student.summer_mark_sheet.year_group + "§" + student.summer_mark_sheet.teacher + "§" + str(student.summer_mark_sheet.math_grade) + "§" + str(student.summer_mark_sheet.science_grade) + "§" + str(student.summer_mark_sheet.english_grade) + "§" + student.spring_mark_sheet.student + "§" + student.spring_mark_sheet.term + "§" + student.spring_mark_sheet.year_group + "§" + student.spring_mark_sheet.teacher + "§" + str(student.spring_mark_sheet.math_grade) + "§" + str(student.spring_mark_sheet.science_grade) + "§" + str(student.spring_mark_sheet.english_grade) + "§" + student.autumn_mark_sheet.student + "§" + student.autumn_mark_sheet.term + "§" + student.autumn_mark_sheet.year_group + "§" + student.autumn_mark_sheet.teacher + "§" + str(student.autumn_mark_sheet.math_grade) + "§" + str(student.autumn_mark_sheet.science_grade) + "§" + str(student.autumn_mark_sheet.english_grade) + "§\n")
        DataUpdate.update(location)

    def deletestudent(self):
        data, location = sortbyname(self.name)
        Delete = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", "")
        Delete.update(location)
        print(self.name, "successfully deleted!")
        return True, False


def sortbyname(name):
    name = name.lower()
    name = name.capitalize()
    SearchingName = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", name)
    data, location = SearchingName.retrieve(1)
    return data, location


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


if __name__ == "__main__":
    # current_student = _Student("Mridul", "14", "10")
    # get_student_details(current_student)
    # current_student.editmarksheet()
    # get_mark_sheet_details(current_student)
    # get_mark_sheet_marks(current_student)
    # print(sortbyname("Mridul"))
    # del current_student
    # _Student.recreatestudent()
    file = open("Text Files/Student.txt", "r+")
    file.truncate(0)
    file.close()
    student1 = Student("Nitin", "41", "12")
    student2 = Student("Upma", "43", "11")
    student3 = Student("Mridul", "14", "10")
    student1.savestudentdata()
    student2.savestudentdata()
    student3.savestudentdata()
    del student1, student2, student3
    student_obj = Student.recreatestudent(input("Enter student name:"))
    Student.savedata(student_obj)
