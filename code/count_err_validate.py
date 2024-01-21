from load_json_to_schema import *
from load_schema import *
from jsonschema import validate, ValidationError, SchemaError
from glob import glob
from tqdm import tqdm


def check_err(x: list):
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


def category_err(err_info):
    err_dict = check_err(err_info['err_path'])
    err = check_err(err_info['err'])

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

## make validate.xlsx
# schema = Make_Schema()
# schema.json_file = '/home/ms/Downloads/열매_궤양병/HF01_01FT_000002.json'
# df = schema.process_df()

schema = generate_json_schema('validate.xlsx')

err_file = []
err = []
err_path = []
decode_num = 0


for j_file in tqdm(glob('/home/ms/Downloads/열매_궤양병/*.json')):
    # Load the JSON data to be validated
    with open(j_file, 'r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
            validate(data, schema)

        except ValidationError as e:
            err_file.append(j_file.split('/')[-1])
            err.append(str(e).split('\n')[0])
            err_path.append(e.absolute_schema_path)

        except JSONDecodeError as e:
            err_file.append(str(j_file).split('\\')[-1])
            err.append(str(e).split(':')[0])
            err_path.append(str(e).split(':')[-1])
            decode_num += 1
        except SchemaError as e:
            # Handle schema errors
            print('Schema error:')
            err_file.append(j_file.split('/')[-1])
            err.append(str(e).split('\n')[0])
            err_path.append(e.absolute_schema_path)
err_info = {'file': err_file, 'err': err, 'err_path': err_path}

print(err_info)

# 전체 오류 카운팅(위치포함)
err_count_df = pd.DataFrame.from_dict(err_info)
err_count_df.columns = ['오류', '세부', '수량']

# 세부 오류 카운팅(위치 불포함)
df = category_err(err_info)
df = pd.DataFrame.from_dict(df, orient="index").stack().to_frame().reset_index()
df.columns = ['오류', '세부', '수량']
df.reset_index(inplace=True, drop=True)
df = df.astype({'수량':'int32'})
groups = df.groupby('오류')

for name, group in groups:
    print(f"Group {name} 오류 :")
    print(group)
