import json
from lesson_03_data_validation import UserValidator

if __name__ == '__main__':
    with open("./user_data.json", "r") as json_file:
        # json.loads() - deserializeaza un string din format JSON in obiect python.
        data = json.load(json_file) # deserializeaza un fisier care contine informatii JSON in obiect python
        validated_user = UserValidator.model_validate(data, strict= True)
        print(validated_user)