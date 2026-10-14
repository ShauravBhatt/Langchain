from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """
class Student:

    def __init__(self, name, age, marks):
        self.name = name
        self.age = age
        self.marks = marks

    def display_details(self):
        print("Student Name:", self.name)
        print("Student Age:", self.age)
        print("Student Marks:", self.marks)

    def calculate_grade(self):
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "D"

    def check_result(self):
        if self.marks >= 40:
            print("Result: Pass")
            print("Grade:", self.calculate_grade())
        else:
            print("Result: Fail")


student = Student("Rahul", 20, 85)

student.display_details()
student.check_result()
"""

splitter = RecursiveCharacterTextSplitter.from_language(
  language = Language.PYTHON,
  chunk_size = 300,
  chunk_overlap = 0
)

chunks = splitter.split_text(text)

print(chunks[0])