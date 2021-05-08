import numpy as np
import matplotlib.pyplot as plt
from distributions import normal_dist_density, cauchy_dist_density, laplace_dist_density, poisson_dist_density, \
    uniform_dist_density, normal_dist_function, cauchy_dist_function, laplace_dist_function, poisson_dist_function, \
    uniform_dist_function
from characteristics import var


def _empiric_func_distribution(x, distr):
    res = x.copy()
    for i in range(len(res)):
        res[i] = 0.0
        for el in distr:
            if el < x[i]:
                res[i] += 1.
        res[i] /= len(distr)
    return res


def _empiric_density_distribution(x, data, mul):
    res = x.copy()
    _h = mul * _bandwidth(data)
    for i in range(len(res)):
        res[i] = 0.0
        for j in range(len(data)):
            res[i] += normal_dist_density((x[i] - data[j]) / _h)
        res[i] /= (len(data) * _h)
    return res


def _bandwidth(x):
    return 1.06 * np.sqrt(var(x)) / (len(x) ** 0.2)


def _draw_density(data, distribution, x, mul):
    y1 = distribution(x)
    y2 = _empiric_density_distribution(x, data, mul)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel('Density')
    plt.xlabel('Argument')
    plt.title(f'N = {len(data)}, h = {mul}$h_n$')


def _draw_func(data, distribution, x):
    y1 = distribution(x)
    y2 = _empiric_func_distribution(x, data)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel('Function of distribution')
    plt.xlabel('Argument')
    plt.title(f'N = {len(data)}')


def do_func_plus_density_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    distrib_f = [normal_dist_function, cauchy_dist_function, laplace_dist_function, poisson_dist_function, uniform_dist_function]
    distrib_d = [normal_dist_density, cauchy_dist_density, laplace_dist_density, poisson_dist_density, uniform_dist_density]
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
            _draw_func(data[j][i], distrib_f[i], edges[i])
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
                _draw_density(data[k][i], distrib_d[i], edges[i], muls[j])
                plt.subplots_adjust(wspace=0.5, hspace=0.5)
                ind += 1
        plt.savefig('plots/lab4/' + names[i] + 'edd.png', format='png')
        plt.show()
