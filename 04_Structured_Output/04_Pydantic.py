from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Pydantic model defines the data structure + validation rules.
class Student(BaseModel):
    name: str
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(ge=0, le=10, default=5)


new_student = {
    "name": "Shaurav",
    "age": 12,
    "email": "shaurav12@gmail.com",
    "cgpa": 9.1,
    "description": "A decimal value representing the cgpa of the student",
}

# Pydantic validates the data and creates a Student object.
student = Student(**new_student)

print(student)

new_student1 = {"name": 22}

# student1 = Student(**new_student1)  # Validation error:
                                      # email is required.


new_student2 = {
    "name": "Shaurav",
    "email": "abc@gmail"
}

# student2 = Student(**new_student2)  # Validation error:
                                      # invalid email format.


# Convert the Pydantic model into a dictionary.
student = dict(student)

print(student["email"])


"""
CONCEPT:

Pydantic = structure + validation.

- BaseModel -> defines the schema.
- EmailStr -> validates email format.
- Optional[int] = None -> age can be missing.
- Field(ge=0, le=10) -> CGPA must be 0 to 10.

This is useful for LLM structured output because
the LLM's output can be validated against the schema.
"""