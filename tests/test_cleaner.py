import pandas as pd

from clean_panda import Cleaner

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}


def test_normalize_text():
    clean = Cleaner(dataframe=df)
    clean.normalize_text(['name', 'sex'])
    assert clean.data.frame['sex'][4] == 'MALE'
    assert clean.data.frame['name'][6] == 'KATE'


def test_remove_features():
    clean = Cleaner(dataframe=df)
    clean.remove_features(['age', 'sex'])
    assert clean.data.frame.columns == ['name']


def test_keep_features():
    clean = Cleaner(dataframe=df)
    clean.keep_features(['sex'])
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
