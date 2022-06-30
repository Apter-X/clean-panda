from clean_panda import Data

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}

df2 = {'name': ['Diana', 'Clark', 'Kent'],
       'age': [32, 23, 45],
       'sex': ['female', 'male', 'male']}


def test_duplicate_data():
    data = Data(dataframe=df)
    data.duplicate_data(2)
    assert data.frame.count().values[0] == 14


def test_append_data():
    data = Data(dataframe=df)
    data_to_append = Data(dataframe=df2).frame
    data.append_data([data_to_append])
    assert data.frame.count().values[0] == 10


def test_get_value():
    data = Data(dataframe=df)
    assert data.get_value('age', data.frame.name == 'Jane') == 28
