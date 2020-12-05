from HelperLibrary.StorageFunctions import StorageFunctions
from HelperLibrary.Student import Student
from Interface.StudentCommandLineInterface import CLI


class ManageStore:
    def __init__(self, table_name):
        self.table_name = table_name

    def validate_if_student_exists(self, name):
        student_data = StorageFunctions(self.table_name).retrieve(["name"], [name])
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


class Manage:
    def __init__(self, student_table_name="students"):
        self.manage_module = ManageStore(student_table_name)

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
