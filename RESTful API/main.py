from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str


with open('people.json', 'r') as f:
    people = json.load(f)['People']
print(people)

@app.get("/person/{person_id}", status_code=200)
def get_person(person_id: int):
    person = [person for person in people if person['id'] == person_id]
    return person if person else {}


@app.delete("/deletePerson/{person_id}", status_code=204)
def delete_person(person_id: int):
    if people[person_id]:
        del people[person_id]
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else:
        return HTTPException(status_code=404, detail=f"person with id {person_id} does not exist")
    return {"Succes": "Person deleted"}


@app.post('/addPerson', status_code=201)
def add_person(person: Person):
    person_id = max([person['id'] for person in people]) + 1
    new_person = {
        "id": person_id,
        "name": person.name.title(),
        "age": person.age,
        "gender": person.gender
    }

    people.append(new_person)

    with open('people.json', 'w') as f:
        json.dump(people, f)

    return new_person


@app.put('/editPerson', status_code=204)
def edit_person(person: Person):
    if people[person.id]:
        people[person.id].name = person.name.title()
        people[person.id].age = person.age
        people[person.id].gender = person.gender
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else:
        return HTTPException(status_code=404, detail=f"person with id {person.id} does not exist")
    return person


@app.get("/search", status_code=200)
def search_person(age: Optional[int] = Query(None, title="Age", description="The age to filter for"),
                  name: Optional[str] = Query(None, title="Name", description="The name to filter for")):
    people1 = [person for person in people if person['age'] == age]

    if name is None:
        if age is None:
            return people
        else:
            return people1
    else:
        if age is None:
            people2 = [person for person in people if name.lower() in person['name'].lower()]
            if age is None:
                return people2
            else:
                combined = [person for person in people1 if person in people2]
                return combined


@app.get('/')
def api_home():
    return {"Message": "Welcome to My People Management RESTful API!"}

