from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 501


def test_get_a_hero():
    response = client.get("/heroes/?name=Lyn&start_date=1970-01-01")
    response_json = response.json()

    assert len(response_json) == 13
    assert response_json[5][1] == "Lyn"
    assert response_json[5][2] == "Bride of the Plains"
    assert response_json[5][3] == "2017-05-30"
    assert response_json[5][4] == "Staff"
    assert response_json[5][5] == "Colorless"
    assert response_json[5][6] == "Infantry"
    assert response_json[5][7] == "Fire Emblem: The Blazing Blade"
    # assert response_json[5][5:] == "Colorless"

    assert response.status_code == 200


def test_fail_get_hero():
    # Name not existing
    response = client.get("/heroes/?name=qsdlkqsdlqksdj&start_date=1970-01-01")
    assert response.status_code == 204

    # Invalid charaacter
    response = client.get("/heroes/?name=Lyn \" Here&start_date=1970-01-01")
    assert response.status_code == 400


def test_delete():
    response = client.delete("/heroes/")
    assert response.status_code == 200


def test_read_all_heroes():
    response = client.patch("/heroes/")
    assert response.status_code == 200


def test_change_my_hero():
    response = client.put("/heroes/my?id=1&lvl=40&fusion=0&draco_flower=0")
    response_json = response.json()

    assert response_json["OK"] == [17, 7, 8, 8, 6, 50, 60, 55, 40, 45, 39, 33, 32, 25, 25]


def test_get_my_heroes():
    response = client.get("/heroes/my")
    response_json = response.json()

    assert len(response_json) == 1


def test_delete_my_hero():
    response = client.delete("/heroes/my", params={"id": 1})
    assert response.status_code == 200
