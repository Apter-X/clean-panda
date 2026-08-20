import numpy as np
import pandas as pd


class Data:
    def __init__(self, dataframe=None, columns=None):
        self.frame = pd.DataFrame(dataframe, columns=columns)

    def get_fetch(self, fetched_data):
        """ Get dataframe from a database """
        for row in fetched_data:
            self.frame.loc[len(self.frame.index)] = row

    def import_csv(self, path, low_memory=False):
        """ Set dataframe from a csv file """
        self.frame = pd.read_csv(path, low_memory=low_memory)
        return self.frame

    def import_json(self, path):
        """ Set dataframe from a json file """
        self.frame = pd.read_json(path, )
        return self.frame

    def duplicate_data(self, n):
        """ Duplicate data existing in the dataframe """
        duplicate = [pd.DataFrame()]
        while n > 0:
            duplicate.append(self.frame)
            n -= 1
        self.frame = pd.concat(duplicate)

    def append_data(self, arr_data):
        """ Concatenate the existing data with the array of dataframe """
        arr_data.append(self.frame)
        self.frame = pd.concat(arr_data)

    def export_to_csv(self, path, encoding='utf-8', index=False):
        """ Export the dataframe as a csv file """
        self.frame.to_csv(path, encoding=encoding, index=index)

    def export_to_json(self, path):
        """ Export the dataframe as a json file """
        self.frame.to_json(path)

    def export_to_xlsx(self, path):
        """ Export the dataframe as a xlsx file """
        self.frame.to_excel(path)

    def get_value(self, of, where):
        row = self.frame.loc[where]
        row_index = row[of].index[0]
        value = self.frame[of][row_index]
        return value

    def get_rows(self, where):
        row = self.frame.loc[where]
        return row

    def get_filter_by_values(self, arr_value):
        matched = self.frame.iloc[:, 1:].isin(arr_value).any(axis=1)
        return self.frame[matched]
