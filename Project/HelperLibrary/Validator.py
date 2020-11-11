from enum import Enum


class AllowedValuesReconformation(Enum):
    stop = "0"
    resume = "1"


class Validator:
    def __init__(self, input_name):
        self.type = input_name

    def validate_separator(self, string):
        if "§" in string:
            print("The", self.type, "is not accepted as it contains '§' which is not accepted.\nPlease try again.")
            return 1
        else:
            return 0

    def should_continue(self):
        while True:
            try:
                print("You have entered the", self.type, "section.")
                decision = AllowedValuesReconformation(
                    input("Do you want to continue?\nEnter 1 to continue or 0 to leave."))
            except ValueError:
                print("Enter valid choice (0, 1)")
            else:
                return bool(int(decision.value))
