import numpy as np
import math as math
import matplotlib.pyplot as plt


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


def draw_hist(data, name, distribution, edges):
    n, bins, patches = plt.hist(x=data, bins=edges, density=1, color='red')
    x = np.linspace(bins.min(), bins.max(), int(np.ceil((bins.max() - bins.min()) / 0.001)))
    y = distribution(x)
    plt.plot(x, y)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel('Density')
    plt.xlabel('Argument')
    plt.title(f'N = {len(data)}')
    max_density = n.max()
    max_density = max(max_density, y.max())
    plt.ylim(ymax=max_density * 1.01)


def do_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    distrib = [normal_dist, cauchy_dist, laplace_dist, poisson_dist, uniform_dist]
    edges = [np.linspace(-3, 3, 10), np.linspace(-3, 3, 10), np.linspace(-3, 3, 10),
             np.linspace(5, 15, 11), np.linspace(-5*np.sqrt(3)/4, 5*np.sqrt(3)/4, 10)]
    quantities = [10, 50, 1000]
    data = []
    for i in range(3):
        data.append([np.random.normal(0, 1, quantities[i]), np.random.standard_cauchy(quantities[i]),
                     np.random.laplace(0, np.sqrt(3), quantities[i]), np.random.poisson(10, quantities[i]),
                     np.random.uniform(-np.sqrt(3), np.sqrt(3), quantities[i])])
    for i in range(5):
        plt.suptitle(names[i])
        for j in range(3):
            plt.subplot(1, 3, j + 1)
            draw_hist(data[j][i], names[i], distrib[i], edges[i])
            plt.subplots_adjust(wspace=1)
        plt.show()
