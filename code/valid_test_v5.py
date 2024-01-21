import json

import pandas as pd


def check_avaiable_value(sub_schema, main_schema, prop_type, value_key):
	enum_val = main_schema.loc[main_schema['항목'] == value_key, '유효값'].values[0]
	pattern_val = main_schema.loc[main_schema['항목'] == value_key, '패턴'].values[0]
	null_val = main_schema.loc[main_schema['항목'] == value_key, 'Null 여부'].values[0]
	min_val = main_schema.loc[main_schema['항목'] == value_key, '최솟값'].values[0]
	max_val = main_schema.loc[main_schema['항목'] == value_key, '최댓값'].values[0]
	multiple_val = main_schema.loc[main_schema['항목'] == value_key, '기타'].values[0]

	if enum_val != '999':
		sub_schema['enum'] = [int(x) if prop_type in ('integer', 'number') else x.strip() for x in
		                      str(enum_val).split(',')]
	elif pattern_val != '999':
		sub_schema['pattern'] = pattern_val
	else:
		if min_val != '999':
			if prop_type in ['integer', 'number']:
				sub_schema['minimum'] = int(min_val)
			elif prop_type == 'array':
				sub_schema['minItems'] = int(min_val)
			elif prop_type == 'string':
				sub_schema['minLength'] = int(min_val)
			elif prop_type == 'object':
				sub_schema['minProperties'] = int(min_val)
		if max_val != '999':
			if prop_type in ['integer', 'number']:
				sub_schema['maximum'] = int(max_val)
			elif prop_type == 'array':
				sub_schema['maxItems'] = int(max_val)
			elif prop_type == 'string':
				sub_schema['maxLength'] = int(max_val)
			elif prop_type == 'object':
				sub_schema['maxProperties'] = int(max_val)
		if multiple_val != '999' and prop_type in ['integer', 'number']:
			sub_schema['multipleOf'] = int(multiple_val)

	if null_val == True:
		sub_schema['type'].append('null')

	return sub_schema


def generate_json_schema(file_path):
	# Read Excel file and fill null values with 999
	schema = pd.read_excel(file_path).fillna('999')

	# Initialize JSON schema
	json_schema = {
		'$schema': "http://json-schema.org/draft-7/schema#",
		'type': 'object',
		'title': 'Validate',
		'properties': {},
		'required': []
	}

	# Loop through each main key and its associated sub-keys
	for main_key in schema.loc[schema['항목'].str.count('\.') == 0, '항목']:
		if schema.loc[schema['항목'] == main_key, '타입'].values[0] == 'array/object':
			json_schema['required'].append(main_key)
			json_schema['properties'][main_key] = {
				'type': 'array',
				'items': {
					'type': 'object',
					'properties': {},
					'required': [main_key]
				}
			}

			for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
				prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
				sub_name = sub_key.split('.')[-1]
				sub_schema = {'type': prop_type}

				if prop_type == 'object':
					sub_schema['properties'] = {}
					sub_schema['required'] = [sub_name]

					sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
					json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema

				elif prop_type == 'array/object':
					sub_schema['type'] = 'array'
					sub_schema['items'] = {'type': 'object',
					                       'properties': {},
					                       'required': [sub_name]
					                       }

					sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
					json_schema['properties'][main_key]['items']['properties']['items']['properties'][
						sub_name] = sub_schema

				elif prop_type == 'array':
					sub_schema['items'] = {}

					sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
					json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema

				elif prop_type in ('integer', 'number', 'string', '999'):
					temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}
					sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)
					json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema


		else:
			json_schema['required'].append(main_key)
			main_prop_type = schema.loc[schema['항목'] == main_key, '타입'].values[0]

			if main_prop_type in ('integer', 'number', 'string', '999'):
				temp_schema = {'type': 'string'} if main_prop_type in ('999') else {'type': main_prop_type}
				sub_schema = check_avaiable_value(temp_schema, schema, main_prop_type, main_key)

				json_schema['properties'][main_key] = sub_schema
			else:
				json_schema['properties'][main_key] = {'type': 'object',
				                                       'properties': {}} if main_prop_type == 'object' else {
					'type': 'array', 'items': {}}
				main_prop_type = json_schema['properties'][main_key]['type']
				for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
					prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
					sub_schema = {'type': prop_type}
					sub_name = sub_key.split('.')[-1]
					if main_prop_type == 'object':
						if prop_type == 'object':
							sub_schema['properties'] = {}
							sub_schema['required'] = [sub_name]

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)

						elif prop_type == 'array/object':
							sub_schema['type'] = 'array'
							sub_schema['items'] = {'type': 'object',
							                       'properties': {},
							                       'required': [sub_name]
							                       }

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
						elif prop_type == 'array':
							sub_schema['items'] = {}

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
						elif prop_type in ('integer', 'number', 'string', '999'):
							temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}

							sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)

						json_schema['properties'][main_key]['properties'][sub_name] = sub_schema
					else:
						if prop_type == 'object':
							sub_schema['properties'] = {}
							sub_schema['required'] = [sub_name]

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)

						elif prop_type == 'array/object':
							sub_schema['type'] = 'array'
							sub_schema['items'] = {'type': 'object',
							                       'properties': {},
							                       'required': [sub_name]
							                       }

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
						elif prop_type == 'array':
							sub_schema['items'] = {}

							sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
						elif prop_type in ('integer', 'number', 'string', '999'):
							temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}

							sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)

						json_schema['properties'][main_key]['items'][sub_name] = sub_schema

	return json_schema


if __name__ == '__main__':
	schema = generate_json_schema('validate.xlsx')
	print(json.dumps(schema, indent=2, ensure_ascii=False))
