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
        ├── remove_columns
        ├── keep_columns
        ├── remove_duplicates
        ├── remove_null_rows
        ├── replace_str
        ├── replace_values
        ├── rename_columns
        ├── sort_rows
        ├── convert_type
        ├── add_column_from_row
        ├── add_column_from_column
        ├── add_column_from_operation
        ├── apply_to_columns
        ├── merge_data
        ├── remove_by_condition
        ├── keep_by_condition
        ├── keep_by_values
        ├── round_columns
        ├── replace_by_mapping
        ├── get_rows_with_group_size
        ├── remove_small_groups
        ├── Data
            ├── import_rows
            ├── import_csv
            ├── import_json
            ├── repeat_rows
            ├── concat_frames
            ├── export_to_csv
            ├── export_to_json
            ├── export_to_xlsx
            ├── get_first_value
            ├── get_rows
            ├── get_rows_by_values
            ├── Frame //pandas methods
            │   ├── ...

## Renamed methods

Several methods were renamed to say plainly what they do. **The old names still
work**, they only warn once towards their new one, so no existing script breaks:

| Old name | New name |
| --- | --- |
| `remove_features` | `remove_columns` |
| `keep_features` | `keep_columns` |
| `remove_na` | `remove_null_rows` |
| `rename_column` | `rename_columns` |
| `sort_data` | `sort_rows` |
| `convert` | `convert_type` |
| `apply_row_rule` | `add_column_from_row` |
| `apply_rule_out` | `add_column_from_column` |
| `operator_feat` | `add_column_from_operation` |
| `apply_rule` | `apply_to_columns` |
| `keep_what_is_in` | `keep_by_values` |
| `round_data` | `round_columns` |
| `map_data` | `replace_by_mapping` |
| `get_cluster_by_label` | `get_rows_with_group_size` |
| `remove_by_cluster` | `remove_small_groups` |
| `Data.get_fetch` | `Data.import_rows` |
| `Data.duplicate_data` | `Data.repeat_rows` |
| `Data.append_data` | `Data.concat_frames` |
| `Data.get_value` | `Data.get_first_value` |
| `Data.get_filter_by_values` | `Data.get_rows_by_values` |

A few arguments were renamed along the way — `operator_feat(a, b, ...)` became
`add_column_from_operation(label, other, ...)`, `remove_by_cluster(..., min_model)`
became `remove_small_groups(..., min_size)`, `round_data(..., by)` became
`round_columns(..., decimals)`. The old names keep accepting the old arguments.

## Tests

```shell
$ pip install -r requirements.txt
$ pytest tests
```

## License

MIT License
