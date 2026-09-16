import pytest
from pydantic import ValidationError

from lesson_03_data_validation import UserValidator


def test_simple_case_1():
    var1 = 10
    assert var1 <= 20
    assert var1 == 10


def test_user_validation():
    received_user = {
        "name": "Vicentiu",
        "age": 11,
        "nationality": "Romanian",
        "external": True,
        "address": {
            "city": "Brasso",
            "street": "Intoarsa"
        }
    }

    user = UserValidator.model_validate(received_user, strict=True)

    assert user.name == "Vicentiu"
    assert user.age == 11
    assert user.nationality == "Romanian"
    assert user.external is True
    assert user.address.city == "Brasso"


@pytest.mark.parametrize("age", [-1, 130, 500, 1000])
def test_user_age_validation(age):
    with pytest.raises(ValidationError):
        received_user = {
            "name": "Vlad",
            "age": age,
            "nationality": "Romanian",
            "external": True,
            "address": {
                "city": "Brasso",
                "street": "Intoarsa"
            }
        }

        UserValidator.model_validate(received_user, strict=True)
