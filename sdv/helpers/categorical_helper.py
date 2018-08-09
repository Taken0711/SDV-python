import logging
from collections import Counter
from scipy import stats
import random


class CategoricalHelper:
    def __init__(self, sample, column_name):
        self.bounds = {}

        # We analyze frequency of every class and allocate them a range in the [0, 1) segment,
        # as described in the Synthetic Data Vault Paper
        counter = Counter(sample)
        cumulative_probability = 0
        for clazz, nb in counter.most_common():
            p = nb / len(sample)
            self.bounds[clazz] = (cumulative_probability, cumulative_probability + p)
            cumulative_probability += p
        logging.debug("Range for %s are %s" % (column_name, str(self.bounds)))

    def draw_for_class(self, clazz):
        # Draw a float in the range allocated to the class
        bounds = self.bounds[clazz]
        mean = bounds[0] + (bounds[1] - bounds[0]) / 2
        variance = (bounds[1] - bounds[0]) / 6
        # Because python, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html
        normalised_min = (bounds[0] - mean) / variance
        normalised_max = (bounds[1] - mean) / variance
        return stats.truncnorm.rvs(normalised_min, normalised_max, loc=mean, scale=variance)

    def draw_a_class(self):
        return self.postprocess(random.random())

    def gaussian_copula(self, x):
        return stats.norm.ppf(stats.uniform.cdf(x))

    def inverse_gaussian_copula(self, x):
        return stats.norm.cdf(x)

    def preprocess(self, x):
        return self.draw_for_class(x)

    def postprocess(self, x):
        for clazz, bounds in self.bounds.items():
            if bounds[0] <= x < bounds[1]:
                return clazz
        raise RuntimeError('No corresponding class found')