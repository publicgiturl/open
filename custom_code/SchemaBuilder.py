import json
from json import JSONDecodeError

import pandas as pd
from genson import SchemaBuilder
from openpyxl import Workbook

# json에서 json 스키마 출력
# 상세기준으로는 들어가지 않음
### 스키마 생성!
def schema_builder(json_file):
    builder = SchemaBuilder()
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            datastore = json.load(f)
            builder.add_object(datastore)
        except JSONDecodeError as e:
            pass
    schema = builder.to_schema()
    return schema

aa = schema_builder('/home/ms/Downloads/test/080_H00_001_F_0000148.json')
# print((json.dumps(aa, indent=2)))
# print('-'*1000)
aa.pop('$schema')
bb = json.dumps(aa, indent=2)
print(bb)
# cc = pd.read_json(bb)
# print(cc)


# rand_num = [43,34,1,27,17,13,12,18,33,39,4,20,14,26, 2,37]
#
# import random
# for rand in range(5):
#     print(random.sample(rand_num, 6))