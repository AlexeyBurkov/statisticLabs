import numpy as np
from scipy import stats
import math as math
import matplotlib.pyplot as plt


def mean(x):
    return sum(x) / len(x)


def var(x):
    _x = mean(x)
    x_c = x.copy()
    for i in range(len(x_c)):
        x_c[i] = (x_c[i] - _x) ** 2
    return mean(x_c)


def normal_dist(x):
    shift = 0.
    scale = 1.
    return 1 / (scale * np.sqrt(2 * np.pi)) * np.exp(- (x - shift) * (x - shift) / (2 * scale * scale))


def cauchy_dist(x):
    shift = 0.
    scale = 1.
    return 1 / (np.pi * scale) * 1 / (1 + (x - shift) * (x - shift) / (scale * scale))


def laplace_dist(x):
    shift = 0.
    scale = np.sqrt(2)
    return scale / 2 * np.exp(-scale * np.abs(x - shift))


def poisson_dist(x):
    shift = 10
    res = x.copy()
    for k in range(len(x)):
        res[k] = shift ** x[k] / math.gamma(x[k] + 1) * np.exp(-shift)
    return res


def uniform_dist(x):
    half_width = np.sqrt(3)
    res = x.copy()
    for i in range(len(res)):
        if np.abs(res[i]) < half_width:
            res[i] = 1 / (2 * half_width)
        else:
            res[i] = 0
    return res


def normal_dist_d(x):
    return stats.norm.cdf(x)


def cauchy_dist_d(x):
    return stats.cauchy.cdf(x)


def laplace_dist_d(x):
    return stats.laplace.cdf(x, scale=1 / np.sqrt(2))


def poisson_dist_d(x):
    shift = 10
    return stats.poisson.cdf(x, mu=shift)


def uniform_dist_d(x):
    return stats.uniform.cdf(x, loc=-np.sqrt(3), scale=2 * np.sqrt(3))


def empiric_func_distribution(x, distr):
    res = x.copy()
    for i in range(len(res)):
        res[i] = 0.0
        for el in distr:
            if el < x[i]:
                res[i] += 1.
        res[i] /= len(distr)
    return res


def empiric_density_distribution(x, data, mul):
    res = x.copy()
    _h = mul * bandwidth(data)
    for i in range(len(res)):
        res[i] = 0.0
        for j in range(len(data)):
            res[i] += normal_dist((x[i] - data[j]) / _h)
        res[i] /= (len(data) * _h)
    return res


def bandwidth(x):
    return 1.06 * np.sqrt(var(x)) / (len(x) ** 0.2)


def draw_density(data, distribution, x, mul):
    y1 = distribution(x)
    y2 = empiric_density_distribution(x, data, mul)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel('Density')
    plt.xlabel('Argument')
    plt.title(f'N = {len(data)}, h = {mul}$h_n$')


def draw_func(data, distribution, x):
    y1 = distribution(x)
    y2 = empiric_func_distribution(x, data)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel('Function of distribution')
    plt.xlabel('Argument')
    plt.title(f'N = {len(data)}')


def do_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    distrib_f = [normal_dist_d, cauchy_dist_d, laplace_dist_d, poisson_dist_d, uniform_dist_d]
    distrib_d = [normal_dist, cauchy_dist, laplace_dist, poisson_dist, uniform_dist]
    edges = [np.linspace(-4, 4, 1600), np.linspace(-4, 4, 1600), np.linspace(-4, 4, 1600),
             np.linspace(6, 14, 1600), np.linspace(-4, 4, 1600)]
    quantities = [20, 60, 100]
    data = []
    for i in range(len(quantities)):
        data.append([np.random.normal(0, 1, quantities[i]), np.random.standard_cauchy(quantities[i]),
                     np.random.laplace(0, 1 / np.sqrt(2), quantities[i]), np.random.poisson(10, quantities[i]),
                     np.random.uniform(-np.sqrt(3), np.sqrt(3), quantities[i])])
    for i in range(len(names)):
        plt.figure(figsize=(10, 4), dpi=120)
        plt.suptitle(names[i])
        for j in range(len(quantities)):
            plt.subplot(1, len(quantities), j + 1)
            draw_func(data[j][i], distrib_f[i], edges[i])
            plt.subplots_adjust(wspace=0.5)
        plt.savefig('plots/lab4/' + names[i] + 'efd.png', format='png')
        plt.show()
    muls = [0.5, 1., 2.]
    for i in range(len(names)):
        plt.figure(figsize=(10, 10), dpi=120)
        plt.suptitle(names[i])
        ind = 1
        for j in range(len(muls)):
            for k in range(len(quantities)):
                plt.subplot(len(muls), len(quantities), ind)
                if i == 1:
                    data[k][i] = data[k][i][(data[k][i] < 4) & (data[k][i] > -4)]
                draw_density(data[k][i], distrib_d[i], edges[i], muls[j])
                plt.subplots_adjust(wspace=0.5, hspace=0.5)
                ind += 1
        plt.savefig('plots/lab4/' + names[i] + 'edd.png', format='png')
        plt.show()
