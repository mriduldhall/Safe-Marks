from HelperLibrary.StorageFunctions import StorageFunctions


class CreateStore:
    def __init__(self, file_path):
        self.storage_file = file_path

    def check_if_student_exist(self, name):
        student_data = StorageFunctions(self.storage_file, name)
        data, location = student_data.retrieve(1)
        if data is None:
            return False
        else:
            return True

    def create_student(self, student):
        student_data = StorageFunctions(self.storage_file, student.singleton + "§" + student.age + "§" + student.year_group + "§" + student.summer_mark_sheet.student + "§" + student.summer_mark_sheet.term + "§" + student.summer_mark_sheet.year_group + "§" + student.summer_mark_sheet.teacher + "§" + str(student.summer_mark_sheet.math_grade) + "§" + str(student.summer_mark_sheet.science_grade) + "§" + str(student.summer_mark_sheet.english_grade) + "§" + student.spring_mark_sheet.student + "§" + student.spring_mark_sheet.term + "§" + student.spring_mark_sheet.year_group + "§" + student.spring_mark_sheet.teacher + "§" + str(student.spring_mark_sheet.math_grade) + "§" + str(student.spring_mark_sheet.science_grade) + "§" + str(student.spring_mark_sheet.english_grade) + "§" + student.autumn_mark_sheet.student + "§" + student.autumn_mark_sheet.term + "§" + student.autumn_mark_sheet.year_group + "§" + student.autumn_mark_sheet.teacher + "§" + str(student.autumn_mark_sheet.math_grade) + "§" + str(student.autumn_mark_sheet.science_grade) + "§" + str(student.autumn_mark_sheet.english_grade) + "§\n")
        student_data.append()


class Create:
    def __init__(self, student_data_storage_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt"):
        self.create_module = CreateStore(student_data_storage_path)

    def create(self, student):
        if not self.create_module.check_if_student_exist(student.singleton):
            self.create_module.create_student(student)
            return "Student successfully created"
        else:
            return "Student already exists"
