import json
import pandas as pd


def check_avaiable_value(schema_df, value_key):
	enum_val = schema_df.loc[schema_df['항목'] == value_key, '유효값'].values[0]
	pattern_val = schema_df.loc[schema_df['항목'] == value_key, '패턴'].values[0]
	null_val = schema_df.loc[schema_df['항목'] == value_key, 'Null 여부'].values[0]
	min_val = schema_df.loc[schema_df['항목'] == value_key, '최솟값'].values[0]
	max_val = schema_df.loc[schema_df['항목'] == value_key, '최댓값'].values[0]
	multiple_val = schema_df.loc[schema_df['항목'] == value_key, '기타'].values[0]
	return enum_val, pattern_val, null_val, min_val, max_val, multiple_val


def get_all_keys(d):
	keys = []
	for k, v in d.items():
		keys.append(k)
		if isinstance(v, dict):
			keys.extend(get_all_keys(v))
	return keys


def update_value(d, target_key, new_value):
	for k, v in d.items():
		if k == target_key:
			old_value = d[k]
			if 'properties' in list(old_value.keys()):
				d[k]['properties'].update(new_value)
				d[k]['required'].append(list(new_value.keys())[0])
			elif 'items' in list(old_value.keys()):
				d[k]['items']['properties'].update(new_value)
				if 'properties' in old_value['items'].keys():
					d[k]['items']['required'].append(list(new_value.keys())[0])
		elif isinstance(v, dict):
			update_value(v, target_key, new_value)


def individual_type(main_key, main_prop_type, schema, sub_key=None, sub_prop_type=None, df=None):
	# check_avaiable_value(schema, df, prop_type, sub_key)
	if sub_key is None:
		schema['required'].append(main_key)
		if main_prop_type == 'array/object':
			schema["properties"][main_key] = {"type": "array",
			                                  "items": {"type": "object", "properties": {}, "required": []}}
			enum_val, pattern_val, null_val, min_val, max_val, multiple_val = check_avaiable_value(df, main_key)
			if null_val != '999':
				schema["properties"][main_key]['items']['type'] = ["array", "null"]
			if enum_val != '999':
				schema["properties"][main_key]['items'].update({'enum': enum_val})
			else:
				if max_val != '999':
					schema["properties"][main_key]['items'].update({'maxProperties': int(max_val)})
				if min_val != '999':
					schema["properties"][main_key]['items'].update({'minProperties': int(min_val)})
			return schema

		elif main_prop_type == 'array':
			schema["properties"][main_key] = {"type": "array", "items": {}}
			enum_val, pattern_val, null_val, min_val, max_val, multiple_val = check_avaiable_value(df, main_key)
			if null_val != '999':
				schema["properties"][main_key]['type'] = ["array", "null"]
			if enum_val != '999':
				schema["properties"][main_key].update({'enum': enum_val})
			else:
				if max_val != '999':
					schema["properties"][main_key].update({'maxItems': int(max_val)})
				if min_val != '999':
					schema["properties"][main_key].update({'minItems': int(min_val)})
				if multiple_val != '999':
					schema["properties"][main_key].update({'uniqueItems': True})

			return schema

		elif main_prop_type == 'object':
			schema["properties"][main_key] = {"type": "object", "properties": {}, "required": []}
			enum_val, pattern_val, null_val, min_val, max_val, multiple_val = check_avaiable_value(df, main_key)
			if null_val != '999':
				schema["properties"][main_key]['type'] = ["object", "null"]
			if enum_val != '999':
				schema["properties"][main_key].update({'enum': enum_val})
			else:
				if max_val != '999':
					schema["properties"][main_key].update({'maxProperties': int(max_val)})
				if min_val != '999':
					schema["properties"][main_key].update({'minProperties': int(min_val)})

			return schema

		else:
			schema["properties"][main_key] = {"type": change_type(main_prop_type)}
			enum_val, pattern_val, null_val, min_val, max_val, multiple_val = check_avaiable_value(df, main_key)
			if null_val != '999':
				schema["properties"][main_key]['type'] = [change_type(main_prop_type), "null"]
			if change_type(main_prop_type) == 'string':
				if enum_val != '999':
					enum_val = [x.strip() for x in str(enum_val).split('|')]
					schema["properties"][main_key].update({'enum': enum_val})
				elif pattern_val != '999':
					schema["properties"][main_key].update({'pattern': pattern_val})
				else:
					if max_val != '999':
						schema["properties"][main_key].update({'maxLength': max_val})
					if min_val != '999':
						schema["properties"][main_key].update({'minLength': min_val})
			elif change_type(main_prop_type) in ['integer', 'number']:
				if enum_val != '999':
					enum_val = [int(x) if change_type(main_prop_type) == 'integer' else float(x) for x in
					            str(enum_val).split('|')]
					schema["properties"][main_key].update({'enum': enum_val})
				else:
					if max_val != '999':
						schema["properties"][main_key].update({'maximum': int(max_val)})
					if min_val != '999':
						schema["properties"][main_key].update({'minimum': int(min_val)})
					if multiple_val != '999':
						multiple_val = [int(x) if change_type(main_prop_type) == 'integer' else float(x) for x in
						                str(multiple_val).split('|')]
						schema["properties"][main_key].update({'multipleOf': multiple_val})
			return schema
	else:
		sub_name = sub_key.split('.')[-1]
		temp_name = sub_key.split('.')[-2]
		value_list = list(check_avaiable_value(df, sub_key))
		sub_schema = type_value(sub_name, sub_prop_type, value_list)
		update_value(schema, temp_name, sub_schema)

	return schema


def type_value(key_name, prop_type, value_list):
	if prop_type == 'object':
		sub_schema = {key_name: {
			'type': 'object',
			'properties': {},
			'required': []
		}}
		if value_list[2] != '999':
			sub_schema[key_name]['type'] = ["object", "null"]
		if value_list[0] != '999':
			sub_schema[key_name].update({'enum': value_list[0]})
		else:
			if value_list[4] != '999':
				sub_schema[key_name].update({'maxProperties': int(value_list[4])})
			if value_list[3] != '999':
				sub_schema[key_name].update({'minProperties': int(value_list[3])})
		return sub_schema

	elif prop_type == 'array':
		try:
			int(value_list[0].split('|')[0].strip())
			ary_type = 'number'
		except:
			ary_type = 'string'
		sub_schema = {key_name: {
			'type': 'array',
			'items': {"type": ary_type}
		}}
		if value_list[2] != '999':
			sub_schema[key_name]['type'] = ["array", "null"]

		if value_list[0] != '999':
			if ary_type == 'number':
				sub_schema[key_name].update({'enum': [[int(x.strip()) for x in value_list[0].split('|')]]})
			else:
				sub_schema[key_name].update({'enum': [[x.strip() for x in value_list[0].split('|')]]})
		else:
			if value_list[4] != '999':
				sub_schema[key_name].update({'maxItems': int(value_list[4])})
			if value_list[3] != '999':
				sub_schema[key_name].update({'minItems': int(value_list[3])})
			if value_list[5] != '999':
				sub_schema[key_name].update({'uniqueItems': True})
		return sub_schema

	elif prop_type == 'array/object':
		sub_schema = {key_name: {
			'type': 'array',
			'items': {
				'type': 'object',
				'properties': {},
				'required': []
			}
		}}
		if value_list[2] != '999':
			sub_schema[key_name]['object']['type'] = ["object", "null"]
		if value_list[0] != '999':
			sub_schema[key_name]['items'].update({'enum': value_list[0]})
		else:
			if value_list[4] != '999':
				sub_schema[key_name]['items'].update({'maxProperties': int(value_list[4])})
			if value_list[3] != '999':
				sub_schema[key_name]['items'].update({'minProperties': int(value_list[3])})
		return sub_schema

	else:
		sub_schema = {key_name: {'type': change_type(prop_type)}}
		if value_list[2] != '999':
			sub_schema[key_name]['type'] = [change_type(prop_type), "null"]
		if change_type(prop_type) == 'string':
			if value_list[0] != '999':
				enum_val = [x.strip() for x in str(value_list[0]).split('|')]
				sub_schema[key_name].update({'enum': enum_val})
			elif value_list[1] != '999':
				sub_schema[key_name].update({'pattern': value_list[1]})
			else:
				if value_list[4] != '999':
					sub_schema[key_name].update({'maxLength': int(value_list[4])})
				if value_list[3] != '999':
					sub_schema[key_name].update({'minLength': int(value_list[3])})
		elif change_type(prop_type) in ['integer', 'number']:
			if value_list[0] != '999':
				enum_val = [int(x) if change_type(prop_type) == 'integer' else float(x) for x in
				            str(value_list[0]).split('|')]
				sub_schema[key_name].update({'enum': enum_val})
			else:
				if value_list[4] != '999':
					sub_schema[key_name].update({'maximum': value_list[4]})
				if value_list[3] != '999':
					sub_schema[key_name].update({'minimum': value_list[3]})
				if value_list[5] != '999':
					multiple_val = [int(x) if change_type(prop_type) == 'integer' else float(x) for x in
					                str(value_list[5]).split('|')]
					sub_schema[key_name].update({'multipleOf': multiple_val})

		return sub_schema


def change_type(prop_type):
	if prop_type in ['string', 'str', '999']:
		return 'string'
	elif prop_type in ['integer', 'int']:
		return 'integer'
	elif prop_type in ['number', 'float']:
		return 'number'
	else:
		return 'boolean'


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
		main_prop_type = schema.loc[schema['항목'] == main_key, '타입'].values[0]
		json_schema = individual_type(main_key, main_prop_type, json_schema, df=schema)

		for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
			prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
			json_schema = individual_type(main_key, main_prop_type, json_schema, sub_key, prop_type, schema)

	return json_schema


# for main_key in schema.loc[schema['항목'].str.count('\.') == 0, '항목']:
# 	main_prop_type = schema.loc[schema['항목'] == main_key, '타입'].values[0]
# 	if main_prop_type == 'array/object':
# 		json_schema['required'].append(main_key)
# 		json_schema['properties'][main_key] = {
# 			'type': 'array',
# 			'items': {
# 					'type': 'object',
# 					'properties': {},
# 					'required': [main_key]
# 				}
# 		}
#
# 		for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
# 			prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
# 			sub_name = sub_key.split('.')[-1]
# 			sub_schema = {'type': prop_type}
#
# 			if prop_type == 'object':
# 				sub_schema['properties'] = {}
# 				sub_schema['required'] = [sub_name]
#
# sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 				json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema
#
# 			elif prop_type == 'array/object':
# 				sub_schema['type'] = 'array'
# 				sub_schema['items'] ={'type': 'object',
# 					 'properties': {},
# 					 'required': [sub_name]
# 					 }
#
# 				sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 				json_schema['properties'][main_key]['items']['properties']['items']['properties'][sub_name] = sub_schema
#
# 			elif prop_type == 'array':
# 				sub_schema['items'] = {}
#
# 				sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 				json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema
#
# 			elif prop_type in ('integer', 'number', 'string', '999'):
# 				temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}
# 				sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)
# 				json_schema['properties'][main_key]['items']['properties'][sub_name] = sub_schema
#
#
# 	else:
# 		json_schema['required'].append(main_key)
#
# 		if main_prop_type in ('integer', 'number', 'string', '999'):
# 			temp_schema = {'type': 'string'} if main_prop_type in ('999') else {'type': main_prop_type}
# 			sub_schema = check_avaiable_value(temp_schema, schema, main_prop_type, main_key)
#
# 			json_schema['properties'][main_key] = sub_schema
# 		else:
# 			json_schema['properties'][main_key] = {'type':'object', 'properties': {}} if main_prop_type=='object' else {'type':'array', 'items' : {}}
# 			main_prop_type = json_schema['properties'][main_key]['type']
# 			for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
# 				prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
# 				sub_schema = {'type': prop_type}
# 				sub_name = sub_key.split('.')[-1]
# 				if main_prop_type =='object':
# 					if prop_type == 'object':
# 						sub_schema['properties'] = {}
# 						sub_schema['required'] = [sub_name]
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
#
# 					elif prop_type == 'array/object':
# 						sub_schema['type'] = 'array'
# 						sub_schema['items'] ={'type': 'object',
# 							 'properties': {},
# 							 'required': [sub_name]
# 							 }
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 					elif prop_type == 'array':
# 						sub_schema['items'] = {}
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 					elif prop_type in ('integer', 'number', 'string', '999'):
# 						temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}
#
# 						sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)
#
# 					json_schema['properties'][main_key]['properties'][sub_name] = sub_schema
# 				else:
# 					if prop_type == 'object':
# 						sub_schema['properties'] = {}
# 						sub_schema['required'] = [sub_name]
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
#
# 					elif prop_type == 'array/object':
# 						sub_schema['type'] = 'array'
# 						sub_schema['items'] = {'type': 'object',
# 							 'properties': {},
# 							 'required': [sub_name]
# 							 }
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 					elif prop_type == 'array':
# 						sub_schema['items'] = {}
#
# 						sub_schema = check_avaiable_value(sub_schema, schema, prop_type, sub_key)
# 					elif prop_type in ('integer', 'number', 'string', '999'):
# 						temp_schema = {'type': 'string'} if prop_type == '999' else {'type': prop_type}
#
# 						sub_schema = check_avaiable_value(temp_schema, schema, prop_type, main_key)
#
# 					json_schema['properties'][main_key]['items'][sub_name] = sub_schema

if __name__ == '__main__':
	schema = generate_json_schema('validate.xlsx')
	print(json.dumps(schema, indent=2, ensure_ascii=False))
