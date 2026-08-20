import pandas as pd
import pytest

from clean_panda import Cleaner

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}


def test_normalize_text():
    clean = Cleaner(dataframe=df)
    clean.normalize_text(['name', 'sex'])
    assert clean.data.frame['sex'][4] == 'MALE'
    assert clean.data.frame['name'][6] == 'KATE'


def test_remove_columns():
    clean = Cleaner(dataframe=df)
    clean.remove_columns(['age', 'sex'])
    assert clean.data.frame.columns == ['name']


def test_keep_columns():
    clean = Cleaner(dataframe=df)
    clean.keep_columns(['sex'])
    assert clean.data.frame.columns == ['sex']


def test_dataframe_given_positionally():
    clean = Cleaner(df)
    assert clean.data.frame['name'][0] == 'Olivia'


def test_data_given_positionally():
    data = Cleaner(dataframe=df).data
    clean = Cleaner(data)
    assert clean.data is data


def test_normalize_text_keeps_null():
    clean = Cleaner({'name': ['Olivia', None], 'age': [32, 23]})
    clean.normalize_text(['name'])
    assert clean.data.frame['name'][0] == 'OLIVIA'
    assert pd.isna(clean.data.frame['name'][1])


def test_replace_str_keeps_null():
    clean = Cleaner({'name': ['Ol-ivia', None], 'age': [32, 23]})
    clean.replace_str(['name'], ['-'], '')
    assert clean.data.frame['name'][0] == 'Olivia'
    assert pd.isna(clean.data.frame['name'][1])


def test_remove_null_rows():
    clean = Cleaner({'name': ['Olivia', None], 'age': [32, 23]})
    clean.remove_null_rows()
    assert list(clean.data.frame['name']) == ['Olivia']


def test_remove_by_condition_after_keep():
    clean = Cleaner(df)
    clean.keep_by_condition(clean.data.frame.age > 30)
    clean.remove_by_condition(clean.data.frame.sex == 'male')
    assert list(clean.data.frame['name']) == ['Olivia', 'Kate']


def test_rename_columns():
    clean = Cleaner(df)
    clean.rename_columns({'sex': 'gender'})
    assert list(clean.data.frame.columns) == ['name', 'age', 'gender']


def test_sort_rows():
    clean = Cleaner(df)
    clean.sort_rows('age')
    assert list(clean.data.frame['name'])[0] == 'Kate'


def test_convert_type():
    clean = Cleaner(df)
    clean.convert_type(['age'], str)
    assert clean.data.frame['age'][0] == '32'


def test_add_column_from_row():
    clean = Cleaner(df)
    clean.add_column_from_row('summary', lambda row: '{} is {}'.format(row['name'], row['age']))
    assert clean.data.frame['summary'][0] == 'Olivia is 32'


def test_add_column_from_column():
    clean = Cleaner(df)
    clean.add_column_from_column('age', lambda age: age * 2, 'double')
    assert clean.data.frame['double'][0] == 64


def test_apply_to_columns():
    clean = Cleaner(df)
    clean.apply_to_columns(['name'], lambda name: name.lower())
    assert clean.data.frame['name'][0] == 'olivia'


def test_keep_by_values():
    clean = Cleaner(df)
    clean.keep_by_values(['female'], ['sex'])
    assert list(clean.data.frame['name']) == ['Olivia', 'Jane', 'Kate']


def test_round_columns():
    clean = Cleaner({'name': ['Olivia'], 'score': [3.14159]})
    clean.round_columns(['score'], 2)
    assert clean.data.frame['score'][0] == 3.14


def test_add_column_from_operation_with_column():
    clean = Cleaner(df)
    clean.add_column_from_operation('age', 'age', 'add', 'double')
    assert clean.data.frame['double'][0] == 64


def test_add_column_from_operation_with_value():
    clean = Cleaner(df)
    clean.add_column_from_operation('age', 2, 'mul', 'double')
    assert clean.data.frame['double'][0] == 64


def test_add_column_from_operation_invalid_operation():
    clean = Cleaner(df)
    with pytest.raises(ValueError):
        clean.add_column_from_operation('age', 2, 'pow', 'oops')


def test_replace_by_mapping():
    clean = Cleaner(df)
    mapper = pd.DataFrame({'old': ['female'], 'new': ['F']})
    clean.replace_by_mapping(mapper, 'sex')
    assert clean.data.frame['sex'][0] == 'F'


def test_get_rows_with_group_size():
    clean = Cleaner(df)
    rows = clean.get_rows_with_group_size(['sex'])
    assert list(rows[rows['sex'] == 'female']['nb']) == [3, 3, 3]


def test_remove_small_groups():
    clean = Cleaner(df)
    clean.remove_small_groups(['sex'], 3)
    assert list(clean.data.frame['sex'].unique()) == ['male']


def test_legacy_names_still_work():
    clean = Cleaner(df)
    with pytest.warns(DeprecationWarning):
        clean.remove_features(['sex'])
    assert list(clean.data.frame.columns) == ['name', 'age']


def test_legacy_names_still_take_their_old_arguments():
    clean = Cleaner(df)
    with pytest.warns(DeprecationWarning):
        clean.operator_feat(a='age', b=2, operation='mul', new_label='double')
    assert clean.data.frame['double'][0] == 64


def test_legacy_names_still_take_the_arguments_they_lost():
    clean = Cleaner(df)
    with pytest.warns(DeprecationWarning):
        clean.keep_features(['sex'], axis=1, inplace=True)
    assert clean.data.frame.columns == ['sex']


def test_legacy_name_tells_which_one_to_use():
    clean = Cleaner(df)
    with pytest.warns(DeprecationWarning, match="remove_by_cluster.*remove_small_groups"):
        clean.remove_by_cluster(['sex'], min_model=3)
    assert list(clean.data.frame['sex'].unique()) == ['male']
