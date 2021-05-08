import numpy as np
import matplotlib.pyplot as plt
from distributions import normal_dist_density, cauchy_dist_density, laplace_dist_density, poisson_dist_density, \
    uniform_dist_density


def _draw_hist(data, distribution, edges):
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


def do_hist_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    distributions = [normal_dist_density, cauchy_dist_density, laplace_dist_density, poisson_dist_density,
                     uniform_dist_density]
    edges = [np.linspace(-3, 3, 10), np.linspace(-3, 3, 10), np.linspace(-3, 3, 10),
             np.linspace(5, 15, 11), np.linspace(-5 * np.sqrt(3) / 4, 5 * np.sqrt(3) / 4, 10)]
    quantities = [10, 50, 1000]
    dist_data = []
    for i in range(len(quantities)):
        dist_data.append([np.random.normal(0, 1, quantities[i]), np.random.standard_cauchy(quantities[i]),
                          np.random.laplace(0, 1 / np.sqrt(2), quantities[i]), np.random.poisson(10, quantities[i]),
                          np.random.uniform(-np.sqrt(3), np.sqrt(3), quantities[i])])
    for i in range(len(names)):
        plt.suptitle(names[i])
        for j in range(3):
            plt.subplot(1, 3, j + 1)
            _draw_hist(dist_data[j][i], distributions[i], edges[i])
            plt.subplots_adjust(wspace=1)
        plt.savefig('plots/lab1/' + names[i] + ' Hist.png', format='png')
        plt.show()
