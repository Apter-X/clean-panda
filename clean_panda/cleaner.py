import operator
import unicodedata

from clean_panda._legacy import attach_legacy_names
from clean_panda.data import Data, np


class Cleaner:
    def __init__(self, data=None, dataframe=None, columns=None):
        if isinstance(data, Data):
            self.data = data
        elif data is not None:
            self.data = Data(data, columns=columns)  # dataframe given positionally
        else:
            self.data = Data(dataframe, columns=columns)

    def normalize_text(self, arr_labels, unicode="NFC"):
        """ Normalize and uppercase a textual column or multiple columns """
        for label in arr_labels:
            self.data.frame[label] = self.data.frame[label].map(
                lambda x: unicodedata.normalize(unicode, x).upper() if isinstance(x, str) else x)

    def remove_columns(self, arr_labels):
        """ Remove a column or multiple columns """
        self.data.frame = self.data.frame.drop(arr_labels, axis=1)

    def keep_columns(self, arr_labels):
        """ Keep only the columns given, remove every other one """
        self.data.frame = self.data.frame.drop(self.data.frame.columns.difference(arr_labels), axis=1)

    def remove_duplicates(self, arr_labels, keep="first"):
        """ Remove duplicates and keep by default the first one """
        self.data.frame = self.data.frame.drop_duplicates(subset=arr_labels, keep=keep)

    def remove_null_rows(self):
        """ Remove every rows with a null value """
        self.data.frame = self.data.frame.dropna()

    def replace_str(self, arr_labels, arr_str, new_str):
        """ Replace string or multiple strings with a new string """
        for label in arr_labels:
            for old_str in arr_str:
                self.data.frame[label] = self.data.frame[label].map(
                    lambda x: x.replace(old_str, new_str) if isinstance(x, str) else x)

    def replace_values(self, arr_values, new_value):
        """ Replace value or multiple values with a new value """
        for value in arr_values:
            self.data.frame.replace({value: new_value}, inplace=True)

    def rename_columns(self, obj_names):
        """ Rename a column or multiple columns """
        self.data.frame.rename(columns=obj_names, inplace=True)

    def sort_rows(self, by, ascending=False):
        """ Sort the rows ascending or descending based on one column """
        self.data.frame = self.data.frame.sort_values(by=by, ascending=ascending)

    def convert_type(self, arr_labels, new_type):
        """ Convert a column or multiple columns to a specific data type """
        for label in arr_labels:
            self.data.frame[label] = self.data.frame[label].astype(new_type)

    def add_column_from_row(self, new_label, rule):
        """ Build a new column by applying a rule to every whole row """
        self.data.frame[new_label] = self.data.frame.apply(rule, axis=1)

    def add_column_from_column(self, label, rule, new_label):
        """ Build a new column by applying a rule to an existing one """
        self.data.frame[new_label] = self.data.frame[label].apply(rule)

    def apply_to_columns(self, arr_labels, rule):
        """ Apply a rule to a column or multiple columns, in place """
        for label in arr_labels:
            self.data.frame[label] = self.data.frame[label].apply(rule)

    def merge_data(self, new_data, on, how="outer"):
        """ Merge another dataframe on a common column """
        self.data.frame = self.data.frame.merge(new_data, on=on, how=how)

    def remove_by_condition(self, condition):
        """ Remove every rows matching the condition """
        self.data.frame = self.data.frame.drop(self.data.frame[condition].index)

    def keep_by_condition(self, condition):
        """ Keep only the rows matching the condition """
        self.data.frame = self.data.frame[condition]

    def keep_by_values(self, arr_values, arr_labels):
        """ Keep only the rows holding one of the values, for every column given """
        for label in arr_labels:
            self.data.frame = self.data.frame[self.data.frame[label].isin(arr_values)]

    def round_columns(self, arr_labels, decimals=None):
        """ Round a numeric column or multiple columns """
        for label in arr_labels:
            self.data.frame[label] = round(self.data.frame[label], decimals)

    def add_column_from_operation(self, label, other, operation, new_label):
        """ Build a new column from a column and another column or a value """
        operations = {
            "add": operator.add,
            "sub": operator.sub,
            "mul": operator.mul,
            "div": operator.truediv
        }
        function = operations.get(operation)
        if function is None:
            raise ValueError("Invalid operation '{}', expected one of: {}".format(
                operation, ", ".join(operations)))
        try:
            right = self.data.frame[other]
        except (KeyError, TypeError):
            right = other  # other is a plain value, not a column label
        self.data.frame[new_label] = function(self.data.frame[label], right)

    def replace_by_mapping(self, mapper, label_1, label_2=None):
        """ Replace values of one or two columns following a mapping dataframe """
        mapper = mapper.astype(str)  # stringify <null> data to compare "=="
        if label_2:
            for old_1, old_2, new_1, new_2 in zip(mapper[mapper.columns[0]], mapper[mapper.columns[1]],
                                                  mapper[mapper.columns[2]], mapper[mapper.columns[3]]):
                self.data.frame.loc[(self.data.frame[label_1] == old_1)
                                    & (self.data.frame[label_2] == old_2), label_1] = new_1
                self.data.frame.loc[(self.data.frame[label_1] == new_1)
                                    & (self.data.frame[label_2] == old_2), label_2] = new_2
        else:
            for old, new in zip(mapper[mapper.columns[0]], mapper[mapper.columns[1]]):
                self.data.frame.loc[(self.data.frame[label_1] == old), label_1] = new
        self.replace_values(['nan'], np.nan)  # reestablish stringified nan to <null>

    def get_rows_with_group_size(self, arr_labels):
        """ Get the dataframe with a 'nb' column counting the rows of every group """
        sizes = self.data.frame.groupby(arr_labels).size().reset_index(name='nb')
        return self.data.frame.merge(sizes, on=arr_labels)

    def remove_small_groups(self, arr_labels, min_size):
        """ Remove the rows belonging to a group holding min_size rows or less """
        self.data.frame = self.get_rows_with_group_size(arr_labels)
        self.data.frame = self.data.frame[self.data.frame['nb'] > min_size]
        self.data.frame = self.data.frame.drop(['nb'], axis=1)


LEGACY_NAMES = {
    "remove_features": "remove_columns",
    "keep_features": "keep_columns",
    "remove_na": "remove_null_rows",
    "rename_column": "rename_columns",
    "sort_data": "sort_rows",
    "convert": "convert_type",
    "apply_row_rule": "add_column_from_row",
    "apply_rule_out": "add_column_from_column",
    "apply_rule": "apply_to_columns",
    "keep_what_is_in": "keep_by_values",
    "round_data": "round_columns",
    "operator_feat": "add_column_from_operation",
    "map_data": "replace_by_mapping",
    "get_cluster_by_label": "get_rows_with_group_size",
    "remove_by_cluster": "remove_small_groups",
}

LEGACY_ARGUMENTS = {
    "apply_rule": {"arr_label": "arr_labels"},
    "keep_what_is_in": {"arr_label": "arr_labels"},
    "round_data": {"by": "decimals"},
    "operator_feat": {"a": "label", "b": "other"},
    "get_cluster_by_label": {"arr_label": "arr_labels"},
    "remove_by_cluster": {"arr_label": "arr_labels", "min_model": "min_size"},
}

attach_legacy_names(Cleaner, LEGACY_NAMES, LEGACY_ARGUMENTS)
