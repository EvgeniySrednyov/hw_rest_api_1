import requests
from jsonschema import validate

from shemas.create_user_shema import create_user
from shemas.list_users_shema import list_users
from shemas.update_user_shema import update_user

URL = 'https://reqres.in/api'

name = 'Evgeniy'
job = 'engineer'
payload = {"name": name, "job": job}

def test_get_users_list():
    response = requests.get(url=f'{URL}/users', params={"page": 2})
    body = response.json()
    count_users = [element["id"] for element in body["data"]]

    assert response.status_code == 200
    assert len(count_users) == len(set(count_users))
    validate(body, schema=list_users)

def test_create_user():
    response = requests.post(url=f'{URL}/users', data=payload)
    body = response.json()

    validate(body, schema=create_user)
    assert response.status_code == 201
    assert body["name"] == name
    assert body["job"] == job


def test_update_user():
    response = requests.put(url=f'{URL}/users/10', data=payload)
    body = response.json()

    validate(body, schema=update_user)
    assert response.status_code == 200
    assert body["name"] == name
    assert body["job"] == job


def test_delete_non_existent_user():
    response = requests.delete(url=f'{URL}/users/999')

    assert response.status_code == 204


def test_resourse_not_found():
    response = requests.get(url=f'{URL}/unknown/999')

    assert response.status_code == 404


def test_unsuccessful_register():
    response = requests.post(url=f'{URL}/register')

    assert response.status_code == 400


def test_generating_correct_email():
    response = requests.get(url=f'{URL}/users/1')

    body = response.json()
    first_name = body['data']['first_name']
    last_name = body['data']['last_name']
    user_email = f'{first_name.lower()}.{last_name.lower()}@reqres.in'

    assert body['data']['email'] == user_email

