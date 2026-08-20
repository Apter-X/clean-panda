from clean_panda import Data

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}

df2 = {'name': ['Diana', 'Clark', 'Kent'],
       'age': [32, 23, 45],
       'sex': ['female', 'male', 'male']}


def test_get_fetch():
    data = Data(columns=['name', 'age', 'sex'])
    data.get_fetch([('Diana', 32, 'female'), ('Clark', 23, 'male')])
    assert list(data.frame['name']) == ['Diana', 'Clark']
    assert list(data.frame.index) == [0, 1]


def test_duplicate_data():
    data = Data(dataframe=df)
    data.duplicate_data(2)
    assert data.frame.count().values[0] == 14


def test_append_data():
    data = Data(dataframe=df)
    data_to_append = Data(dataframe=df2).frame
    data.append_data([data_to_append])
    assert data.frame.count().values[0] == 10


def test_append_data_keeps_the_given_array_intact():
    data = Data(dataframe=df)
    arr_data = [Data(dataframe=df2).frame]
    data.append_data(arr_data)
    assert len(arr_data) == 1


def test_get_value():
    data = Data(dataframe=df)
    assert data.get_value('age', data.frame.name == 'Jane') == 28


def test_get_rows():
    data = Data(dataframe=df)
    rows = data.get_rows(data.frame.name == 'Kate')
    assert rows['age'].values[0] == data.frame.iloc[6]['age']


def test_get_filter_by_values():
    data = Data(dataframe=df)
    values = data.get_filter_by_values(['male'])
    assert values.values[3][0] == 'Tom'


def test_get_filter_by_values_after_filtering():
    data = Data(dataframe=df)
    data.frame = data.frame[data.frame.age > 30]  # index is no longer 0..n
    values = data.get_filter_by_values(['male'])
    assert list(values['name']) == ['Alex', 'Jon']


def test_get_filter_by_values_does_not_repeat_rows():
    data = Data(dataframe={'name': ['Dean'], 'a': ['x'], 'b': ['x']})
    assert len(data.get_filter_by_values(['x'])) == 1
