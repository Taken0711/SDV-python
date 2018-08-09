from datetime import datetime
import numpy as np

from sdv.helpers.int_helper import IntHelper


class DateHelper:

    def __init__(self, sample, column_name):
        self.int_helper = IntHelper(list(map(datetime.toordinal, sample)), column_name)

    def gaussian_copula(self, x):
        return self.int_helper.gaussian_copula(x)

    def inverse_gaussian_copula(self, x):
        return self.int_helper.inverse_gaussian_copula(x)

    def preprocess(self, arr):
        return np.array([datetime.toordinal(datetime.strptime(x, "%Y-%m-%d")) for x in arr])

    def postprocess(self, arr):
        return np.array([datetime.strftime(datetime.fromordinal(int(round(x))), "%Y-%m-%d") for x in arr])
