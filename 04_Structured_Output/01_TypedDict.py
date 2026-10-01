from typing import TypedDict


# Defines the structure of a Person dictionary.
class Person(TypedDict):
    name: str
    age: int


# Must follow the Person structure.
new_person: Person = {
    "name": "shaurav",
    "age": 35
}

print(new_person)


"""
CONCEPT:
TypedDict defines the expected structure of a dictionary.

Person:
- name -> str
- age  -> int

This idea is useful for structured LLM output,
where we define the format we want from the model.
"""