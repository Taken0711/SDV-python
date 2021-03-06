from sdv.helpers.float_helper import FloatHelper
import numpy as np


class IntHelper:

    def __init__(self, sample, column_name):
        self.float_helper = FloatHelper(sample, column_name)

    def gaussian_copula(self, arr):
        return self.float_helper.gaussian_copula(arr)

    def inverse_gaussian_copula(self, arr):
        return self.float_helper.inverse_gaussian_copula(arr)

    def preprocess(self, arr):
        return np.array([int(float(x)) if x else 0 for x in arr])

    def postprocess(self, arr):
        return np.array([int(round(x)) if x else 0 for x in arr])
