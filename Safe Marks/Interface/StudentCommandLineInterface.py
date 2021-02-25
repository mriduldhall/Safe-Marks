class CLI:
    def __init__(self, student, admin, archive):
        self.student = student
        self.admin = admin
        self.archive = archive
        self.menu_choice = None
        self.menu_dict = None

    def initiate(self):
        exit_condition = False
        save_needed = False
        valid_input = False
        while (exit_condition is False) or (valid_input is False):
            save_needed = True
            self.find_student_menu()
            if self.menu_choice == str(len(self.menu_dict) + 1):
                exit_condition = True
                valid_input = True
            elif (self.menu_choice == str(len(self.menu_dict))) and (self.admin is True):
                if self.menu_dict[self.menu_choice]():
                    exit_condition = True
                    valid_input = True
                    save_needed = False
                else:
                    exit_condition = False
                    valid_input = True
            elif (self.menu_choice > str(len(self.menu_dict) + 1)) or self.menu_choice < "1":
                print("Please enter a valid choice!")
                valid_input = False
                exit_condition = False
            else:
                self.menu_dict[self.menu_choice]()
                exit_condition = False
                valid_input = True
            self.check_special_conditions()
        if (save_needed is True) and (self.archive is False):
            self.student.student_controller.save_student_data()

    def find_student_menu(self):
        if (self.admin is False) and (self.archive is False):
            self.menu_choice = input(
                "Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to get all student data and 6 to leave this menu:")
            self.menu_dict = self.student.student_menu_dict
        elif (self.admin is True) and (self.archive is False):
            self.menu_choice = input(
                "Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to edit student details, 6 to get all student data, 7 to remove student from school(archive), 8 to permanently delete student and 9 to leave this menu:")
            self.menu_dict = self.student.admin_student_menu_dict
        elif (self.admin is False) and (self.archive is True):
            self.menu_choice = input(
                "Enter 1 to get student details, 2 to get mark sheet details, 3 to get marks, 4 to get all student data and 5 to exit this menu:")
            self.menu_dict = self.student.archive_student_menu_dict
        else:
            self.menu_choice = input(
                "Enter 1 to get student details, 2 to get mark sheet details, 3 to get marks, 4 to get all student data, 5 to delete student and 6 to exit this menu:")
            self.menu_dict = self.student.admin_archive_student_menu_dict

    def check_special_conditions(self):
        if self.menu_choice in self.menu_dict.keys():
            if self.menu_dict[self.menu_choice] == self.student.student_controller.archive:
                self.archive = True
