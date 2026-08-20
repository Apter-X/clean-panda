import pytest

from clean_panda import Data

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}

df2 = {'name': ['Diana', 'Clark', 'Kent'],
       'age': [32, 23, 45],
       'sex': ['female', 'male', 'male']}


def test_import_rows():
    data = Data(columns=['name', 'age', 'sex'])
    data.import_rows([('Diana', 32, 'female'), ('Clark', 23, 'male')])
    assert list(data.frame['name']) == ['Diana', 'Clark']
    assert list(data.frame.index) == [0, 1]


def test_repeat_rows():
    data = Data(dataframe=df)
    data.repeat_rows(2)
    assert data.frame.count().values[0] == 14


def test_concat_frames():
    data = Data(dataframe=df)
    data_to_append = Data(dataframe=df2).frame
    data.concat_frames([data_to_append])
    assert data.frame.count().values[0] == 10


def test_concat_frames_keeps_the_given_array_intact():
    data = Data(dataframe=df)
    arr_frames = [Data(dataframe=df2).frame]
    data.concat_frames(arr_frames)
    assert len(arr_frames) == 1


def test_get_first_value():
    data = Data(dataframe=df)
    assert data.get_first_value('age', data.frame.name == 'Jane') == 28


def test_get_rows():
    data = Data(dataframe=df)
    rows = data.get_rows(data.frame.name == 'Kate')
    assert rows['age'].values[0] == data.frame.iloc[6]['age']


def test_get_rows_by_values():
    data = Data(dataframe=df)
    values = data.get_rows_by_values(['male'])
    assert values.values[3][0] == 'Tom'


def test_get_rows_by_values_after_filtering():
    data = Data(dataframe=df)
    data.frame = data.frame[data.frame.age > 30]  # index is no longer 0..n
    values = data.get_rows_by_values(['male'])
    assert list(values['name']) == ['Alex', 'Jon']


def test_get_rows_by_values_does_not_repeat_rows():
    data = Data(dataframe={'name': ['Dean'], 'a': ['x'], 'b': ['x']})
    assert len(data.get_rows_by_values(['x'])) == 1


def test_legacy_names_still_work():
    data = Data(dataframe=df)
    with pytest.warns(DeprecationWarning, match="duplicate_data.*repeat_rows"):
        data.duplicate_data(2)
    assert data.frame.count().values[0] == 14


def test_legacy_names_still_take_their_old_arguments():
    data = Data(dataframe=df)
    with pytest.warns(DeprecationWarning):
        assert list(data.get_filter_by_values(arr_value=['male'])['name']) == ['Dean', 'Alex', 'Jon', 'Tom']
