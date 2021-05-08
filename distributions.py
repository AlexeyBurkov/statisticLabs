import numpy as np
import math
import scipy.stats as stats


def normal_dist_density(x):
    shift = 0.
    scale = 1.
    return 1 / (scale * np.sqrt(2 * np.pi)) * np.exp(- (x - shift) * (x - shift) / (2 * scale * scale))


def cauchy_dist_density(x):
    shift = 0.
    scale = 1.
    return 1 / (np.pi * scale) * 1 / (1 + (x - shift) * (x - shift) / (scale * scale))


def laplace_dist_density(x):
    shift = 0.
    scale = np.sqrt(2)
    return scale / 2 * np.exp(-scale * np.abs(x - shift))


def poisson_dist_density(x):
    shift = 10
    res = x.copy()
    for k in range(len(x)):
        res[k] = shift ** x[k] / math.gamma(x[k] + 1) * np.exp(-shift)
    return res


def uniform_dist_density(x):
    half_width = np.sqrt(3)
    res = x.copy()
    for i in range(len(res)):
        if np.abs(res[i]) < half_width:
            res[i] = 1 / (2 * half_width)
        else:
            res[i] = 0
    return res


def normal_dist_function(x):
    return stats.norm.cdf(x)


def cauchy_dist_function(x):
    return stats.cauchy.cdf(x)


def laplace_dist_function(x):
    return stats.laplace.cdf(x, scale=1 / np.sqrt(2))


def poisson_dist_function(x):
    shift = 10
    return stats.poisson.cdf(x, mu=shift)


def uniform_dist_function(x):
    return stats.uniform.cdf(x, loc=-np.sqrt(3), scale=2 * np.sqrt(3))
