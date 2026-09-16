from pydantic import BaseModel, ValidationError, Field
from lesson_02_classes_objects import User
from typing import Literal

#mostenire. inheritance

class Address(BaseModel):
    city: str
    street: str

class UserValidator(BaseModel):
    name: str= Field(min_length=2,max_length=10)
    age: int= Field(ge=0,le=120, default=18)
    nationality: Literal["Romanian","Moldovean"]
    external: Literal[True] | None
    address: Address

received_user = {
    "name": "Vlad",
    "age": 22,
    "nationality": "Romanian",
    "external": True,
    "address":{
        "city": "Brasso",
        "street": "Intoarsa"
    }
}
if __name__ == "__main__":
        validate_user = UserValidator(**received_user)
        print(validate_user)
        print(received_user["name"])
        print("==================Validations==================")

        #try-cath

        try:
            validate_user = UserValidator.model_validate(received_user, strict=True)
            print(validate_user)
        except ValidationError as e:
            print(e)
            print(e.errors())
        finally:
            print("am terminat cu validarea")