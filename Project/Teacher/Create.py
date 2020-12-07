from HelperLibrary.StorageFunctions import StorageFunctions


class CreateStore:
    def __init__(self, table_name):
        self.table_name = table_name

    def check_if_student_exist(self, name):
        student_data = StorageFunctions(self.table_name).retrieve(["name"], [name])
        if not student_data:
            return False
        else:
            return True

    def create_student(self, student):
        StorageFunctions(self.table_name).append("(name, age, current_year_group)", [student.name, student.age, student.year_group])
        student_data = StorageFunctions(self.table_name).retrieve(["name"], [student.name])
        student_data = student_data[0]
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [student.summer_mark_sheet.teacher, student.summer_mark_sheet.math_grade, student.summer_mark_sheet.science_grade, student.summer_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Summer"])[0])[0], student.year_group])
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [student.spring_mark_sheet.teacher, student.spring_mark_sheet.math_grade, student.spring_mark_sheet.science_grade, student.spring_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Spring"])[0])[0], student.year_group])
        StorageFunctions("mark_sheets").append("(teacher, math_mark, science_mark, english_mark, student_id, term_id, year_group_id)", [student.autumn_mark_sheet.teacher, student.autumn_mark_sheet.math_grade, student.autumn_mark_sheet.science_grade, student.autumn_mark_sheet.english_grade, student_data[0], (StorageFunctions("terms").retrieve(["term"], ["Autumn"])[0])[0], student.year_group])



class Create:
    def __init__(self, student_table_name="students"):
        self.create_module = CreateStore(student_table_name)

    def create(self, student):
        if not self.create_module.check_if_student_exist(student.name):
            self.create_module.create_student(student)
            return "Student successfully created"
        else:
            return "Student already exists"
