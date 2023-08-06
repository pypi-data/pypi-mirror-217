# Jsoner

Convenient and fast adding objects to json file

## Installation

`pip install jsoner-lib`

## A simple example
```python
from pydantic import BaseModel


class Dog(BaseModel):
    name: str
    angry: bool


class Cat(BaseModel):
    name: str
    lazy: bool


class Person(BaseModel):
    name: str
    age: str
    animals: list[Cat | Dog] | None

"""
    the so-called imaginary data that you get, for example, when parsing a website
"""
persons = [
    Person(name="Alex", age=40, animals=[Cat(name="Terminator", lazy=False)]),
    Person(name="Victor", age=24, animals=[Dog(name="Barsic", angry=True)]),
    Person(name="Michle", age=59, animals=[Cat(name="Barbon", lazy=True)]),
    Person(name="Tomas", age=42, animals=[Cat(name="Spider", lazy=False)]),
    Person(name="Robert", age=30, animals=[Cat(name="Kraul", lazy=True)]),
    Person(name="Antony", age=29, animals=[Cat(name="Green", lazy=False)])
]

jsn = Jsoner(models=[Person], filename="persons.json")


for psn in persons:
    jsn.append(psn)

jsn.save(indent=4)


## persons.json
"""
[
    {
        "name": "Alex",
        "age": "40",
        "animals": [
            {
                "name": "Terminator",
                "lazy": false
            }
        ]
    },
    {
        "name": "Victor",
        "age": "24",
        "animals": [
            {
                "name": "Barsic",
                "angry": true
            }
        ]
    },
    {
        "name": "Michle",
        "age": "59",
        "animals": [
            {
                "name": "Barbon",
                "lazy": true
            }
        ]
    },
...
...
"""
```

You can find examples in file /example/
