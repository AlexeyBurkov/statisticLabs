import numpy as np
import matplotlib.pyplot as plt


def _distribution_boxplot(distributions, sizes, name):
    labels = [f'n = {sizes[i]}' for i in range(len(sizes))]
    plt.boxplot(distributions, labels=labels)
    plt.ylabel('Value')
    plt.title(name)
    plt.savefig('plots/lab3/' + name + ' Boxplot.png', format='png')
    plt.show()


def _generate_data(quantities):
    return [[np.random.normal(0, 1, i) for i in quantities],
            [np.random.standard_cauchy(i) for i in quantities],
            [np.random.laplace(0, np.sqrt(3), i) for i in quantities],
            [np.random.poisson(10, i) for i in quantities],
            [np.random.uniform(-np.sqrt(3), np.sqrt(3), i) for i in quantities]]


def do_boxplot_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    quantities = [20, 100]
    samples = 1000
    data = _generate_data(quantities)
    for i in range(len(data)):
        _distribution_boxplot(data[i], quantities, names[i])
    outliers = [[0 for _ in range(len(quantities))] for _ in range(len(names))]
    for _ in range(samples):
        data = _generate_data(quantities)
        for j in range(len(data)):
            for k in range(len(data[j])):
                left = np.quantile(data[j][k], 0.25) - 1.5 * (
                        np.quantile(data[j][k], 0.75) - np.quantile(data[j][k], 0.25))
                right = np.quantile(data[j][k], 0.75) + 1.5 * (
                        np.quantile(data[j][k], 0.75) - np.quantile(data[j][k], 0.25))
                for el in data[j][k]:
                    if el < left or el > right:
                        outliers[j][k] += 1
    for j in range(len(outliers)):
        for k in range(len(outliers[j])):
            outliers[j][k] /= samples
            outliers[j][k] /= quantities[k]
    print(outliers)
