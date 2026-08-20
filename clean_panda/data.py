import numpy as np
import pandas as pd

from clean_panda._legacy import attach_legacy_names


class Data:
    def __init__(self, dataframe=None, columns=None):
        self.frame = pd.DataFrame(dataframe, columns=columns)

    def import_rows(self, rows):
        """ Add rows fetched from a database to the dataframe """
        fetched = pd.DataFrame(list(rows), columns=self.frame.columns)
        self.frame = pd.concat([self.frame, fetched], ignore_index=True)

    def import_csv(self, path, low_memory=False):
        """ Set dataframe from a csv file """
        self.frame = pd.read_csv(path, low_memory=low_memory)
        return self.frame

    def import_json(self, path):
        """ Set dataframe from a json file """
        self.frame = pd.read_json(path)
        return self.frame

    def repeat_rows(self, times):
        """ Repeat every row of the dataframe a number of times """
        self.frame = pd.concat([self.frame] * times)

    def concat_frames(self, arr_frames):
        """ Concatenate the existing data with the array of dataframe """
        self.frame = pd.concat(list(arr_frames) + [self.frame])

    def export_to_csv(self, path, encoding='utf-8', index=False):
        """ Export the dataframe as a csv file """
        self.frame.to_csv(path, encoding=encoding, index=index)

    def export_to_json(self, path):
        """ Export the dataframe as a json file """
        self.frame.to_json(path)

    def export_to_xlsx(self, path):
        """ Export the dataframe as a xlsx file """
        self.frame.to_excel(path)

    def get_first_value(self, of, where):
        """ Get the value of a column on the first row matching the condition """
        return self.frame.loc[where, of].iloc[0]

    def get_rows(self, where):
        """ Get every rows matching the condition """
        return self.frame.loc[where]

    def get_rows_by_values(self, arr_values):
        """ Get every rows holding one of the values, the first column aside """
        matched = self.frame.iloc[:, 1:].isin(arr_values).any(axis=1)
        return self.frame[matched]


LEGACY_NAMES = {
    "get_fetch": "import_rows",
    "duplicate_data": "repeat_rows",
    "append_data": "concat_frames",
    "get_value": "get_first_value",
    "get_filter_by_values": "get_rows_by_values",
}

LEGACY_ARGUMENTS = {
    "get_fetch": {"fetched_data": "rows"},
    "duplicate_data": {"n": "times"},
    "append_data": {"arr_data": "arr_frames"},
    "get_filter_by_values": {"arr_value": "arr_values"},
}

attach_legacy_names(Data, LEGACY_NAMES, LEGACY_ARGUMENTS)
