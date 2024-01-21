import json
import pandas as pd

# Read Excel file and fill null values with 999
schema = pd.read_excel('validate.xlsx').fillna('999')

# Get main keys that have only one level in their hierarchy
main_keys = {x: idx for idx, x in enumerate(schema['항목']) if len(x.split('.')) == 1}

# Initialize JSON schema
test = {
	'$schema': "http://json-schema.org/draft-04/schema#",
	'type': 'object',
	'title': 'Validate',
	'properties': {},
	'required': []
}

# Loop through each main key and its associated sub-keys
for main_key in main_keys.keys():
	if schema.loc[schema['항목'] == main_key, '타입'].values[0] == 'array/object':
		test['required'].append(main_key)
		test['properties'][main_key] = {}
		test['properties'][main_key]['type'] = 'array'
		test['properties'][main_key]['items'] = []
		test['properties'][main_key]['items'].append({'type': 'object', 'properties': {}, 'required':[main_key]})

		enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
		min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
		max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
		etc_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]

		if enum_val != '999':
			test['properties']['items'][main_key].append({main_key : {'type': 'object', 'enum': enum_val}})
		else:
			if min_val != '999':
				test['properties'][main_key].append({main_key : {'minItems' : int(min_val)}})
			if max_val != '999':
				test['properties'][main_key].append({main_key : {'maxItems' : int(max_val)}})
			if etc_val in [1.0, 1, True]:
				test['properties'][main_key].append({main_key : {'uniqueItems' : True}})
		assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'
	else:
		test['properties'][main_key] = {}
		test['required'].append(main_key)

	for sub_key in schema[schema['항목'].str.startswith(main_key + '.')]['항목']:
		# Determine property type
		prop_type = schema.loc[schema['항목'] == sub_key, '타입'].values[0]
		# Skip if sub_key is the same as main_key
		if sub_key == main_key:
			continue
		# string -> 패턴 / 유효값  / 최솟값 / 최댓값                       Done
		# int/number -> 유효값 / 최솟값 / 최댓값 / 기타(배수, 소수점자릿수)
		# boolean -> True / False -> 셀값에 특정값이 들어가면 모두 에러
		# 적용되었습니다 / 형식이 맞지 않습니다. / 어느 부분이 에러인지 전달
		# array -> 유효값 X(확인 필요) / 패턴 X / NULL X / 기타(array중복)
		# object -> 유효값 X(확인 필요) -> required / 최솟값&최댓값 X / 패턴 X / 기타 X / NULL X
		# Add property to JSON schema
		if schema.loc[schema['항목'] == main_key, '타입'].values[0] != 'array/object':
			sub_name = sub_key.split('.')[-1]
			# print(f'if : {sub_name}')
			if prop_type == 'string':
				enum_val = [x.strip() for x in schema.loc[schema['항목'] == sub_key, '유효값'].values[0].split(',')]
				test['properties'][main_key][sub_name] = {'type': 'string'}
				pattern_val = schema.loc[schema['항목'] == sub_key, '패턴'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]

				if enum_val != ['999']:
					test['properties'][main_key][sub_name]['enum'] = enum_val
				elif pattern_val != '999':
					test['properties'][main_key][sub_name]['pattern'] = pattern_val
				else:
					if min_val !='999':
						test['properties'][main_key][sub_name]['minLength'] = int(min_val)
					if max_val !='999':
						test['properties'][main_key][sub_name]['maxLength'] = int(max_val)
				assert schema.loc[schema['항목'] == sub_key, '기타'].values[0] == '999', 'Error'

			elif prop_type == 'integer':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				multiple_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key][sub_name] = {'type': 'integer'}
				if enum_val != '999':
					test['properties'][main_key][sub_name] = {'type': 'integer', 'enum': [int(x) for x in enum_val.split(',')]}
				else:
					if min_val != '999':
						test['properties'][main_key][sub_name]['minimum'] = int(min_val)
					if max_val != '999':
						test['properties'][main_key][sub_name]['maximum'] = int(max_val)
					if multiple_val !='999':
						test['properties'][main_key][sub_name]['multipleOf'] = int(multiple_val)
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'

			elif prop_type == 'number':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				multiple_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key][sub_name] = {'type': 'number'}
				if enum_val != '999':
					test['properties'][main_key][sub_name] = {'type': 'number',
					                                          'enum': [float(x) for x in enum_val.split(',')]}
				else:
					if min_val != '999':
						test['properties'][main_key][sub_name]['minimum'] = float(min_val)
					if max_val != '999':
						test['properties'][main_key][sub_name]['maximum'] = float(max_val)
					if multiple_val != '999':
						test['properties'][main_key][sub_name]['multipleOf'] = float(multiple_val)

			elif prop_type == 'object':
				test['properties'][main_key][sub_name] = {'type': 'object', 'properties': {}}
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				etc_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				if enum_val != '999':
					test['properties'][main_key][sub_name] = {'type': 'object', 'enum': enum_val}
				else:
					if min_val != '999':
						test['properties'][main_key][sub_name]['minItems'] = int(min_val)
					if max_val != '999':
						test['properties'][main_key][sub_name]['maxItems'] = int(max_val)
					if etc_val in [1.0, 1, True]:
						test['properties'][main_key][sub_name]['uniqueItems'] = True
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'

			elif prop_type == 'array':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				etc_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key][sub_name] = {'type': 'array', 'items': []}
				if enum_val != '999':
					test['properties'][main_key][sub_name] = {'type': 'array', 'enum': enum_val}
				else:
					if min_val != '999':
						test['properties'][main_key][sub_name]['minItems'] = int(min_val)
					if max_val != '999':
						test['properties'][main_key][sub_name]['maxItems'] = int(max_val)
					if etc_val in [1.0, 1, True]:
						test['properties'][main_key][sub_name]['uniqueItems'] = True
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'
		else:
			sub_name = sub_key.split('.')[-1]
			# print(f'else : {sub_name}')
			if prop_type == 'string':
				enum_val = [x.strip() for x in schema.loc[schema['항목'] == sub_key, '유효값'].values[0].split(',')]
				pattern_val = schema.loc[schema['항목'] == sub_key, '패턴'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				test['properties'][main_key]['items'].append({sub_name: {'type': 'string'}})

				if enum_val != ['999']:
					test['properties'][main_key]['items'].append({sub_name : {'enum' : enum_val}})
				elif pattern_val != '999':
					test['properties'][main_key]['items'].append({sub_name:{'pattern':pattern_val}})
				else:
					if min_val !='999':
						test['properties'][main_key]['items'].append({sub_name: {'minLength' : int(min_val)}})
					if max_val !='999':
						test['properties'][main_key]['items'].append({sub_name : {'maxLength' : int(max_val)}})
				assert schema.loc[schema['항목'] == sub_key, '기타'].values[0] == '999', 'Error'

			elif prop_type == 'integer':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				multiple_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key]['items'].append({sub_name : {'type': 'integer'}})
				if enum_val != '999':
					if type(enum_val) in (int, float):
						test['properties'][main_key]['items'].append(
							{sub_name: {'type': 'integer', 'enum': int(enum_val)}})
					else:
						test['properties'][main_key]['items'].append({sub_name : {'type': 'integer', 'enum': [int(x) for x in enum_val.split(',')]}})
				else:
					if min_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'minimum' : int(min_val)}})
					if max_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'maximum' : int(max_val)}})
					if multiple_val !='999':
						test['properties'][main_key]['items'].append({sub_name : {'multipleOf' : int(multiple_val)}})
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'

			elif prop_type == 'number':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				multiple_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key]['items'].append({sub_name : {'type': 'number'}})
				if enum_val != '999':
					test['properties'][main_key]['items'].append({sub_name : {'type': 'number',
					                                          'enum': [float(x) for x in enum_val.split(',')]}})
				else:
					if min_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'minimum' : float(min_val)}})
					if max_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'maximum' : float(max_val)}})
					if multiple_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'multipleOf' : float(multiple_val)}})

			elif prop_type == 'object':
				test['properties'][main_key]['items'].append({sub_name : {'type': 'object', 'properties': {}}})
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				etc_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				if enum_val != '999':
					test['properties'][main_key]['items'].append({sub_name : {'type': 'object', 'enum': enum_val}})
				else:
					if min_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'minItems' : int(min_val)}})
					if max_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'maxItems' : int(max_val)}})
					if etc_val in [1.0, 1, True]:
						test['properties'][main_key]['items'].append({sub_name : {'uniqueItems' : True}})
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'

			elif prop_type == 'array':
				enum_val = schema.loc[schema['항목'] == sub_key, '유효값'].values[0]
				min_val = schema.loc[schema['항목'] == sub_key, '최솟값'].values[0]
				max_val = schema.loc[schema['항목'] == sub_key, '최댓값'].values[0]
				etc_val = schema.loc[schema['항목'] == sub_key, '기타'].values[0]
				test['properties'][main_key]['items'].append({sub_name : {'type': 'array', 'items': []}})
				if enum_val != '999':
					test['properties'][main_key]['items'].append({sub_name : {'type': 'array', 'enum': enum_val}})
				else:
					if min_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'minItems' : int(min_val)}})
					if max_val != '999':
						test['properties'][main_key]['items'].append({sub_name : {'maxItems' : int(max_val)}})
					if etc_val in [1.0, 1, True]:
						test['properties'][main_key]['items'].append({sub_name : {'uniqueItems': True}})
				assert schema.loc[schema['항목'] == sub_key, '패턴'].values[0] == '999', 'Error'

print(json.dumps(test, indent=2, ensure_ascii=False))