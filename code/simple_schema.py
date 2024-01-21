import json
from jsonschema import Draft7Validator, validators
import pandas as pd


# Load the JSON file
with open('/home/ms/Downloads/N_C_B_210928_01_000000.json', 'r') as f:
    data = json.load(f)

# Define a function to generate a schema based on the provided data
def generate_schema(data):
    # Define a validator for the draft-7 JSON schema
    validator = Draft7Validator

    # Define a function to recursively walk through the JSON data and generate the schema
    def walk(json_data, validator_class):
        if isinstance(json_data, dict):
            # Generate a schema for each property in the object
            properties = {}
            for key, value in json_data.items():
                properties[key] = walk(value, validator_class)
            return {"type": "object", "properties": properties, "required": list(json_data.keys())}
        elif isinstance(json_data, list):
            # Generate a schema for each item in the array
            items = []
            for item in json_data:
                items.append(walk(item, validator_class))
            return {"type": "array", "items": items}
        else:
            # Generate a schema based on the data type of the value
            if isinstance(json_data, bool):
                return {"type": "boolean"}
            elif isinstance(json_data, int):
                return {"type": "integer"}
            elif isinstance(json_data, float):
                return {"type": "number"}
            elif isinstance(json_data, str):
                return {"type": "string"}
            elif json_data is None:
                return {"type": "null"}
            else:
                raise Exception("Unsupported data type: {}".format(type(json_data)))

    # Use the walk function to generate the schema
    schema = walk(data, validator)

    # Use the validator to check the schema
    validator.check_schema(schema)

    # Return the schema
    return schema


if __name__ =='__main__':
    # Generate the schema for the provided JSON data
    schema = generate_schema(data)

# df = pd.json_normalize(schema).transpose()
# print(df)
# df.to_excel('test_test.xlsx')
