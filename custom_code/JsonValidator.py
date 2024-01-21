import json
from json import JSONDecodeError
from jsonschema import validate, ValidationError
import pandas as pd
from glob import glob

# 스키마랑 json파일 넣으면
# 검증 돌아가는 코드

class JSONValidator:
    def __init__(self, schema):
        # self.file = json_file
        self.schema = schema

    def validate_json(self):
        err_file = []
        err = []
        err_path = []
        global decode_num
        decode_num = 0

        for idx, json_file in enumerate(glob('/data2/2022/한자연/가공/한자연/results/Skeleton/skeleton/1/1_01/20220614_113253_0013/*.json', recursive=True)):
            with open(json_file) as f:
                try:
                    json_load = json.load(f)
                    validate(json_load, self.schema)

                except ValidationError as e:
                    err_file.append(json_file.split('\\')[-1])
                    err.append(str(e).split('\n')[0])
                    err_path.append(e.absolute_schema_path)

                except JSONDecodeError as e:
                    err_file.append(str(json_file).split('\\')[-1])
                    err.append(str(e).split(':')[0])
                    err_path.append(str(e).split(':')[-1])
                    decode_num += 1

        err_info = {'file': err_file, 'err': err, 'err_path': err_path}
        return err_info

    def check_err(self, x: list):
        err_dict = {}
        for schema_err in x:
            temp_list = []
            for err in range(len(schema_err)):
                if type(schema_err[err]) == int:
                    continue
                temp_list.append(schema_err[err])
            temp_err = '/'.join(temp_list)
            if temp_err not in err_dict.keys():
                err_dict[temp_err] = 1
            else:
                err_dict[temp_err] += 1
        return err_dict

    def category_err(self):

        validator = JSONValidator(self.schema)
        err_dict = validator.check_err(validator.validate_json()['err_path'])
        err = validator.check_err(validator.validate_json()['err'])

        err_count = dict(
            타입=0,
            범위=0,
            배열=0,
            객체=0,
            패턴=0,
            문법=decode_num)

        type_err = dict(
            string=0,
            integer=0,
            number=0,
            array=0,
            object=0,
            boolean=0,
            null=0)

        range_err = dict(
            maximum=0,
            minimum=0,
            maxLength=0,
            minLength=0,
            enum=0)

        itme_err = dict(
            minItems=0,
            maxItems=0,
            additionalItems=0,
            uniqueItems=0)

        obj_err = dict(
            required=0,
            minProperties=0,
            maxProperties=0)

        for i in err_dict.keys():
            if i.split('/')[-1] == 'type':
                err_count['타입'] += err_dict[i]

            elif i.split('/')[-1] == 'pattern':
                err_count['패턴'] += err_dict[i]

            elif i.split('/')[-1] in ['minimum', 'maximum', 'minLength', 'maxLength', 'enum']:
                err_count['범위'] += err_dict[i]
                range_err[i.split('/')[-1]] += err_dict[i]

            elif i.split('/')[-1] in ['required', 'minProperties', 'maxProperties']:
                err_count['객체'] += err_dict[i]
                obj_err[i.split('/')[-1]] += err_dict[i]

            elif i.split('/')[-1] in ['minItems', 'maxItems', 'additionalItems', 'uniqueItems']:
                err_count['배열'] += err_dict[i]
                itme_err[i.split('/')[-1]] += err_dict[i]

        for i in err:
            i = i.split()[-1].replace("'", '')
            if i in ['integer', 'number', 'string', 'object', 'array', 'boolean', 'null']:
                type_err[i] += 1

        err_count2 = {
            "타입": type_err,
            "범위": range_err,
            "객체": obj_err,
            "배열": itme_err,
            "패턴": {'pattern': err_count["패턴"]},
            "문법": {'decode': decode_num}}

        return err_count2

# total_count = {'전체':idx, '정상': idx - len(err_file), '오류': len(err_file)} # 전체 수량
# 패턴은 없고,
test_schema = {
    # 스키마선언 : 해당 스키마가 단순 json데이터 인지 스키마인지 구분하기 위하여 사용
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    # 유효값
                    "enum": [0, 1]
                },
                "joints":
                    {
                        # array -> list
                        # object -> dict
                        "type": "array",
                        "minItems": 11,
                        "maxItems": 11,
                        "items": [
                            {
                                "type": "array",
                                "items": [
                                    {
                                        "type": "integer"
                                    },
                                    {
                                        "type": "integer"
                                    },
                                    {
                                        "type": "integer",
                                        "maximum": 2,
                                    }
                                ],
                                # multipleOf오류 추가 필요
                                # 위의 요소들 외에 추가적으로 검증이 필요할 경우
                                "additionalItems": False
                            },
                            {
                                "type": "array",
                                "items": [
                                    {
                                        "type": "integer"
                                    },
                                    {
                                        "type": "integer"
                                    },
                                    {
                                        "type": "integer"
                                    }
                                ]
                            }
                        ]
                    }
            },
            "required": ["id", "joints"]
        }
    ]
}

test = JSONValidator(test_schema)

# 오류 파일 리스트
df_test = test.validate_json()
df_err = pd.DataFrame(df_test)

# 오류 종류 세분화 df
df_test = test.category_err()
df = pd.DataFrame.from_dict(df_test, orient="index").stack().to_frame().reset_index()
df.columns = ['오류', '세부', '수량']
df = df[df['수량'] > 0]
df.reset_index(inplace=True, drop=True)


print(df)



