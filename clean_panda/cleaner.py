import operator
import unicodedata

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
        """ Normalize textual column """
        for n in arr_labels:
            self.data.frame[n] = self.data.frame[n].map(
                lambda x: unicodedata.normalize(unicode, x).upper() if isinstance(x, str) else x)

    def remove_features(self, arr_labels):
        """ Remove irrelevant features """
        self.data.frame = self.data.frame.drop(arr_labels, axis=1)

    def keep_features(self, arr_labels, axis=1, inplace=True):
        """ Keep relevant features """
        self.data.frame.drop(self.data.frame.columns.difference(arr_labels), axis=axis, inplace=inplace)

    def remove_duplicates(self, arr_labels, keep="first"):
        """ Remove duplicates and keep by default the first one """
        self.data.frame = self.data.frame.drop_duplicates(arr_labels, keep=keep)

    def remove_na(self, inplace=True):
        """ Remove every rows with a null value """
        self.data.frame.dropna(inplace=inplace)

    def replace_str(self, arr_labels, arr_str, new_str):
        """ Replace string or multiple strings with a new string """
        for n in arr_labels:
            for s in arr_str:
                self.data.frame[n] = self.data.frame[n].map(
                    lambda x: x.replace(s, new_str) if isinstance(x, str) else x)

    def replace_values(self, arr_values, new_value):
        """ Replace value or multiple values with a new value """
        for v in arr_values:
            self.data.frame.replace({v: new_value}, inplace=True)

    def rename_column(self, obj_names):
        """ Rename a column or multiple columns """
        self.data.frame.rename(columns=obj_names, inplace=True)

    def sort_data(self, by, ascending=False):
        """ Sort dataframe ascending or descending based on one column """
        self.data.frame = self.data.frame.sort_values(by=by, ascending=ascending)

    def convert(self, arr_labels, new_type):
        """ Convert a column or multiple column with a specific data type """
        for n in arr_labels:
            self.data.frame[n] = self.data.frame[n].astype(new_type)

    def apply_row_rule(self, new_label, rule):
        self.data.frame[new_label] = self.data.frame.apply(rule, axis=1)

    def apply_rule_out(self, label, rule, new_label):
        self.data.frame[new_label] = self.data.frame[label].apply(rule)

    def apply_rule(self, arr_label, rule):
        for n in arr_label:
            self.data.frame[n] = self.data.frame[n].apply(rule)

    def merge_data(self, new_data, on, how="outer"):
        self.data.frame = self.data.frame.merge(new_data, on=on, how=how)

    def remove_by_condition(self, condition):
        self.data.frame = self.data.frame.drop(self.data.frame[condition].index)

    def keep_by_condition(self, condition):
        self.data.frame = self.data.frame[condition]

    def keep_what_is_in(self, arr_values, arr_label):
        for label in arr_label:
            self.data.frame = self.data.frame[self.data.frame[label].isin(arr_values)]

    def round_data(self, arr_labels, by=None):
        for n in arr_labels:
            self.data.frame[n] = round(self.data.frame[n], by)

    def operator_feat(self, a, b, operation, new_label):
        switcher = {
            "add": operator.add,
            "sub": operator.sub,
            "mul": operator.mul,
            "div": operator.truediv
        }
        op = switcher.get(operation, "Invalid operator")
        try:
            self.data.frame[new_label] = op(self.data.frame[a], self.data.frame[b])
        except:
            self.data.frame[new_label] = op(self.data.frame[a], b)

    def map_data(self, mapper, label_1, label_2=None):
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

    def get_cluster_by_label(self, arr_label):
        cluster = self.data.frame.groupby(arr_label).size().reset_index(name='nb')
        return self.data.frame.merge(cluster, on=arr_label)

    def remove_by_cluster(self, arr_label, min_model):
        self.data.frame = self.get_cluster_by_label(arr_label)
        self.data.frame = self.data.frame[self.data.frame['nb'] > min_model]
        self.data.frame = self.data.frame.drop(['nb'], axis=1)
