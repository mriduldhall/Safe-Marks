class CLI:
    def __init__(self, student, admin, archive):
        self.student = student
        self.admin = admin
        self.archive = archive

    def initiate(self):
        exit_condition = False
        save_needed = False
        valid_input = False
        while (exit_condition is False) or (valid_input is False):
            save_needed = True
            if (self.admin is False) and (self.archive is False):
                student_menu_choice = input(
                    "Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to leave this menu:")
                student_menu_dict = self.student.student_menu_dict
            elif (self.admin is True) and (self.archive is False):
                student_menu_choice = input(
                    "Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to edit student details, 6 to remove student from school(archive), 7 to permanently delete student 8 to leave this menu:")
                student_menu_dict = self.student.admin_student_menu_dict
            elif (self.admin is False) and (self.archive is True):
                student_menu_choice = input(
                    "Enter 1 to get student details, 2 to get mark sheet details, 3 to get marks and 4 to exit this menu:")
                student_menu_dict = self.student.archive_student_menu_dict
            else:
                student_menu_choice = input(
                    "Enter 1 to get student details, 2 to get mark sheet details, 3 to get marks, 4 to delete student and 5 to exit this menu:")
                student_menu_dict = self.student.admin_archive_student_menu_dict
            if student_menu_choice == str(len(student_menu_dict) + 1):
                exit_condition = True
                valid_input = True
            elif (student_menu_choice == str(len(student_menu_dict))) and (self.admin is True):
                student_menu_dict[student_menu_choice]()
                exit_condition = True
                valid_input = True
                save_needed = False
            elif (student_menu_choice > str(len(student_menu_dict) + 1)) or student_menu_choice < "1":
                print("Please enter a valid choice!")
                valid_input = False
                exit_condition = False
            else:
                student_menu_dict[student_menu_choice]()
                exit_condition = False
                valid_input = True
            if student_menu_choice in student_menu_dict.keys():
                if student_menu_dict[student_menu_choice] == self.student.student_controller.archive:
                    self.archive = True
        if (save_needed is True) and (self.archive is False):
            self.student.student_controller.save_student_data()
