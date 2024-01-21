# Making DB columns(공사)
def construct_DB(data):
    class_col = ['_id', 'filename']

    for i in range(1, 46):
        if i < 10:
            class_col.append('class0' + '{}'.format(i))
        else:
            class_col.append('class' + '{}'.format(i))
    class_col.append('BB')
    class_col.append('PO')
    class_col.append('KP')

    construct_DB = pd.DataFrame(columns=class_col)

    # DF에 저장
    for index, row in data.iterrows():

        construct_DB.loc[index, '_id'] = index
        construct_DB.loc[index, 'filename'] = row['filename']

        if row['class'] < 10:

            construct_DB.loc[index, 'class0{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                construct_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                construct_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                construct_DB.loc[index, 'KP'] = row['point']

        else:

            construct_DB.loc[index, 'class{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                construct_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                construct_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                construct_DB.loc[index, 'KP'] = row['point']

        # 빈 값은 0으로 대체
        construct_DB.fillna(0, inplace=True)

    # 데이터 타입 변경
    construct_DB[media_DB.columns.difference(['filename'])] = construct_DB[
        construct_DB.columns.difference(['filename'])].astype('int64')
    # csv 저장
    construct_DB.to_csv('{}.csv'.format(main_path.split('/')[-1]), header=True, encoding='utf-8-sig', index=False)

    return construct_DB


# Making DB columns(화재)
def fire_DB(data):
    class_col = ['_id', 'filename']

    for i in range(1, 11):
        if i < 10:
            class_col.append('class0' + '{}'.format(i))
        else:
            class_col.append('class' + '{}'.format(i))
    class_col.append('BB')
    class_col.append('PO')
    class_col.append('KP')

    fire_DB = pd.DataFrame(columns=class_col)

    # DF에 저장
    for index, row in data.iterrows():

        fire_DB.loc[index, '_id'] = index
        fire_DB.loc[index, 'filename'] = row['filename']

        if row['class'] < 10:

            fire_DB.loc[index, 'class0{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                fire_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                fire_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                fire_DB.loc[index, 'KP'] = row['point']

        else:
            fire_DB.loc[index, 'class{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                fire_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                fire_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                fire_DB.loc[index, 'KP'] = row['point']

        # 빈 값은 0으로 대체
        fire_DB.fillna(0, inplace=True)

    # 데이터 타입 변경
    fire_DB[fire_DB.columns.difference(['filename'])] = fire_DB[fire_DB.columns.difference(['filename'])].astype(
        'int64')
    # csv 저장
    fire_DB.to_csv('{}.csv'.format(main_path.split('/')[-1]), header=True, encoding='utf-8-sig', index=False)

    return fire_DB


# Making DB columns(항공)
def airport_DB(data):
    class_col = ['_id', 'filename']
    for i in range(1, 23):
        if i < 10:
            class_col.append('class0' + '{}'.format(i))
        else:
            class_col.append('class' + '{}'.format(i))
    class_col.append('BB')
    class_col.append('PO')
    class_col.append('KP')

    airport_DB = pd.DataFrame(columns=class_col)

    # DF에 저장
    for index, row in data.iterrows():

        airport_DB.loc[index, '_id'] = index
        airport_DB.loc[index, 'filename'] = row['filename']

        if row['class'] < 10:

            airport_DB.loc[index, 'class0{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                airport_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                airport_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                airport_DB.loc[index, 'KP'] = row['point']

        else:
            airport_DB.loc[index, 'class{}'.format(row['class'])] = row['class_count']

            if row['box'] != 0:
                airport_DB.loc[index, 'BB'] = row['box']
            elif row['polygon'] != 0:
                airport_DB.loc[index, 'PO'] = row['polygon']
            elif row['point'] != 0:
                airport_DB.loc[index, 'KP'] = row['point']

        # 빈 값은 0으로 대체
        airport_DB.fillna(0, inplace=True)
    # 데이터 타입 변경
    airport_DB[airport_DB.columns.difference(['filename'])] = airport_DB[
        media_DB.columns.difference(['filename'])].astype('int64')
    # csv 저장
    airport_DB.to_csv('{}.csv'.format(main_path.split('/')[-1]), header=True, encoding='utf-8-sig', index=False)

    return airport_DB