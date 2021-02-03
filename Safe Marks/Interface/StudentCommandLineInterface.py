class CLI:
    def __init__(self, student):
        self.student = student

    def initiate(self):
        exit_condition = False
        save_needed = False
        valid_input = False
        while (exit_condition is False) or (valid_input is False):
            save_needed = True
            student_menu_choice = input(
                "Enter 1 to edit marks of the student, 2 to get student details, 3 to get mark sheet details, 4 to get marks, 5 to delete student 6 to leave this menu:")
            if student_menu_choice == str(len(self.student.studentmenu_dict) + 1):
                exit_condition = True
                valid_input = True
            elif student_menu_choice == str(len(self.student.studentmenu_dict)):
                self.student.studentmenu_dict[student_menu_choice]()
                exit_condition = True
                valid_input = True
                save_needed = False
            elif (student_menu_choice > str(len(self.student.studentmenu_dict) + 1)) or student_menu_choice < "1":
                print("Please enter a valid choice!")
                valid_input = False
                exit_condition = False
            else:
                self.student.studentmenu_dict[student_menu_choice]()
                exit_condition = False
                valid_input = True
        if save_needed is True:
            self.student.student_controller.savestudentdata()
