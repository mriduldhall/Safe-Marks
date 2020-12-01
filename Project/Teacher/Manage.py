# TODO Move manage and create into a new class called Student that has these methods and is supported by
# TODO student module class that can be used to validate student exists, save data etc. Support CRUD

from HelperLibrary.StorageFunctions import StorageFunctions
from HelperLibrary.Student import Student
from Interface.StudentCommandLineInterface import CLI


class ManageStore:
    def __init__(self, student_file_path):
        self.student_file = student_file_path

    def validate_if_student_exists(self, name):
        student_data = StorageFunctions(self.student_file, name)
        data, location = student_data.retrieve(1)
        if data is None:
            return False
        else:
            return True

    def list_students(self):
        student_data = StorageFunctions(self.student_file, None)
        list_of_students = student_data.list(1)
        print("List of students:")
        counter = 1
        for student_name in sorted(list_of_students):
            print(counter, ":", student_name, end="\n")
            counter += 1


class Manage:
    def __init__(self, student_data_storage_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt"):
        self.manage_module = ManageStore(student_data_storage_path)

    def manage(self):
        choice_list_of_students = bool(int(input("Enter 1 to get a list of all students and 0 to continue without a list of students:")))
        if choice_list_of_students:
            self.manage_module.list_students()
        name = input("Enter student name to manage student:").capitalize()
        if self.manage_module.validate_if_student_exists(name):
            student = Student.recreatestudent(name)
            CLI(student).initiate()
            return "Exiting..."
        else:
            return "Student does not exist"
