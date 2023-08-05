from dataclasses import dataclass, field, fields


@dataclass
class Person:
    id: int
    name: str
    age: int

@dataclass
class Contact(Person):
    address: str
    phone: str

james = Contact(123, "James", 39, "London", None)
james_new = Contact(123, "James", 40, "London", "1234567890")

def diff(old, new):
    diff = {}
    for field in fields(old):
        if getattr(old, field.name) != getattr(new, field.name):
            diff[field.name] = getattr(new, field.name)
    return diff

print(diff(james, james_new))
