# Clean Panda
 An object-oriented program which allows you to clean the pandas dataframe in an intuitive and easy way.
 
#### Installation

```shell
$ pip install clean-panda
```

Requires Python 3.7+ and pandas. Tested from pandas 1.5 up to pandas 3.0.

## Basic Usage

```python
from clean_panda import Cleaner

df = {'name': ['Olivia', 'Dean', 'Alex', 'Jon', 'Tom', 'Jane', 'Kate'],
      'age': [32, 23, 45, 35, 20, 28, 55],
      'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female']}

clean = Cleaner(df)
print(clean.data.frame)
```

```shell
     name  age     sex
0  Olivia   32  female
1    Dean   23    male
2    Alex   45    male
3     Jon   35    male
4     Tom   20    male
5    Jane   28  female
6    Kate   55  female
```

```python
clean.normalize_text(['name', 'sex'])
print(clean.data.frame)
```

```shell
     name  age     sex
0  OLIVIA   32  FEMALE
1    DEAN   23    MALE
2    ALEX   45    MALE
3     JON   35    MALE
4     TOM   20    MALE
5    JANE   28  FEMALE
6    KATE   55  FEMALE
```

```python
clean.keep_by_condition(clean.data.frame.age > 30)
print(clean.data.frame)
```

```shell
     name  age     sex
0  OLIVIA   32  FEMALE
2    ALEX   45    MALE
3     JON   35    MALE
6    KATE   55  FEMALE
```

`clean.data.frame` is a plain `pandas.DataFrame`, so every pandas method stays
available at any moment. The dataframe can also be named explicitly, and its
columns given aside:

```python
clean = Cleaner(dataframe=df)
clean = Cleaner(dataframe=rows, columns=['name', 'age', 'sex'])
```

## Interface

    ├── Cleaner
        ├── normalize_text
        ├── remove_features
        ├── keep_features
        ├── remove_duplicates
        ├── remove_na
        ├── replace_str
        ├── replace_values
        ├── rename_column
        ├── sort_data
        ├── convert
        ├── apply_row_rule
        ├── apply_rule_out
        ├── apply_rule
        ├── merge_data
        ├── remove_by_condition
        ├── keep_by_condition
        ├── keep_what_is_in
        ├── round_data
        ├── operator_feat
        ├── map_data
        ├── get_cluster_by_label
        ├── remove_by_cluster
        ├── Data
            ├── get_fetch
            ├── import_csv
            ├── import_json
            ├── duplicate_data
            ├── append_data
            ├── export_to_csv
            ├── export_to_json
            ├── export_to_xlsx
            ├── get_value
            ├── get_rows
            ├── get_filter_by_values
            ├── Frame //pandas methods
            │   ├── ...
    
## Tests

```shell
$ pip install -r requirements.txt
$ pytest tests
```

## License

MIT License
