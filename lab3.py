import numpy as np
import matplotlib.pyplot as plt


def distribution_boxplot(distribs, sizes, name):
    labels = [f'n = {sizes[i]}' for i in range(len(sizes))]
    plt.boxplot(distribs, labels=labels)
    plt.ylabel('Value')
    plt.title(name)
    plt.show()


def generate_data(quantities):
    return [[np.random.normal(0, 1, i) for i in quantities],
            [np.random.standard_cauchy(i) for i in quantities],
            [np.random.laplace(0, np.sqrt(3), i) for i in quantities],
            [np.random.poisson(10, i) for i in quantities],
            [np.random.uniform(-np.sqrt(3), np.sqrt(3), i) for i in quantities]]


def do_research():
    names = ['Нормальное распределение', 'Распределение Коши', 'Распределение Лапласа',
             'Распределение Пуассона', 'Равномерное распределение']
    quantities = [20, 100]
    samples = 1000
    data = generate_data(quantities)
    for i in range(len(data)):
        distribution_boxplot(data[i], quantities, names[i])

    outliers = [[0 for _ in range(len(quantities))] for _ in range(len(names))]
    for _ in range(samples):
        data = generate_data(quantities)
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
