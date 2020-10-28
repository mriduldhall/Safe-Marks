from enum import Enum
from Student import Student
from StorageFunctions import StorageFunctions


class AllowedValuesMainMenu(Enum):
    create = 'c'
    manage = 'm'
    settings = 's'
    logout = 'l'


def create():
    continuation_check = bool(int(input("You have entered the create section. Enter 1 to continue and 0 to leave.")))
    while continuation_check is True:
        name = input("Enter student's name:").capitalize()
        age = input("Enter student's age:")
        year_group = input("Enter student's year group:")
        student_exist_check = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", name)
        data = student_exist_check.retrieve(1)
        if data is None:
            student = Student(name, age, year_group)
            student.savestudentdata()
            student.getstudentdetails()
            del student
        else:
            print("Student already exists! Please go to manage.")
        continuation_check = bool(int(input("Enter 1 to create another student and 0 to head back to main menu.")))
    return True


def manage():
    def menu(student):
        save_needed = False
        student_menu_choice = input("Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to delete student 6 to leave this menu:")
        if student_menu_choice == str(len(student.studentmenu_dict)+1):
            exit_condition = True
            valid_input = True
        elif student_menu_choice == str(len(student.studentmenu_dict)):
            student.studentmenu_dict[student_menu_choice](student)
            exit_condition = True
            valid_input = True
        elif (student_menu_choice > str(len(student.studentmenu_dict)+1)) or student_menu_choice < "1":
            print("Please enter a valid choice!")
            valid_input = False
            exit_condition = False
        else:
            student.studentmenu_dict[student_menu_choice](student)
            exit_condition = False
            valid_input = True
            save_needed = True
        return valid_input, exit_condition, save_needed

    def managecontrol(student):
        exit_condition = False
        save_needed = False
        valid_input = False
        while (exit_condition is False) or (valid_input is False):
            valid_input, exit_condition, save_needed = menu(student)
        if save_needed is True:
            student.savedata(student)

    def validatename():
        getstudentlist()
        student_to_retrieve = input("Enter student name to manage student:").capitalize()
        valid_name = checkifstudentexists(student_to_retrieve)
        if valid_name is True:
            student = Student.recreatestudent(student_to_retrieve)
            managecontrol(student)
        else:
            print("Student does not exist! Please create student first in create menu.")
        new_user_check = bool(int(input("Enter 1 to enter another name and work on another student or 0 to leave.")))
        return new_user_check

    def checkifstudentexists(name):
        exist_check = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", name)
        result = exist_check.retrieve(1)
        if result is None:
            result = False
        else:
            result = True
        return result

    def getstudentlist():
        choice_list_of_students = bool(int(input("Enter 1 to get a list of all students and 0 to continue without a list of students:")))
        if choice_list_of_students is True:
            get_student_list = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/Student.txt", None)
            list_of_students = get_student_list.list(1)
            print("List of students:")
            counter = 1
            for student_name in sorted(list_of_students):
                print(counter, ":", student_name, end="\n")
                counter += 1

    continuation_check = bool(int(input("You have entered the manage section. Enter 1 to continue and 0 to leave.")))
    if continuation_check is True:
        try_again = True
        while try_again is True:
            try_again = validatename()
    return True


def settings():
    print("I am in settings")
    return True


def logout():
    print("Logging out...\nRedirecting to main page...")
    return False


def mainmenu():
    mainmenudictionary = {'c': create, 'm': manage, 's': settings, 'l': logout}
    exit_control = True
    while exit_control:
        try:
            print("---Home Screen---")
            main_menu_choice = AllowedValuesMainMenu(input("Enter c to create new students, m to manage students and their mark sheets, s for settings and l to logout"))
        except ValueError:
            print("Enter valid choice c, m, s, l)")
        else:
            exit_control = mainmenudictionary[main_menu_choice.value]()


if __name__ == "__main__":
    mainmenu()
