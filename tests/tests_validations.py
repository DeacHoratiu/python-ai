import pytest
from pydantic import ValidationError

from lesson_03_data_validation import UserValidator, received_user


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

    with pytest.raises(ValidationError):
        UserValidator.model_validate(received_user, strict=True)

@pytest.mark.parametrize("age",[-1,130,500,1000])
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
            user = UserValidator.model_validate(received_user,strict = True)