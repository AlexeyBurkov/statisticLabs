import numpy as np
import math as math


def mean(x):
    return sum(x) / len(x)


def med(x):
    if len(x) % 2:
        return x[len(x) // 2 + 1]
    else:
        return (x[len(x) // 2] + x[len(x) // 2 + 1]) / 2


def z_r(x):
    return (x[0] + x[len(x) - 1]) / 2


def z_p(x, p):
    res, i = math.modf(len(x) * p)
    if math.fabs(res) > 0.0:
        return x[int(i) + 1]
    else:
        return x[int(i)]


def z_q(x):
    return (z_p(x, 1 / 4) + z_p(x, 3 / 4)) / 2


def z_tr(x):
    r = len(x) // 4
    return mean(x[r:len(x) - r])


def var(x):
    _x = mean(x)
    x_c = x.copy()
    for i in range(len(x_c)):
        x_c[i] = (x_c[i] - _x) ** 2
    return mean(x_c)


def generate_data(quantities):
    data = []
    for i in range(3):
        data.append([np.random.normal(0, 1, quantities[i]), np.random.standard_cauchy(quantities[i]),
                     np.random.laplace(0, np.sqrt(3), quantities[i]), np.random.poisson(10, quantities[i]),
                     np.random.uniform(-np.sqrt(3), np.sqrt(3), quantities[i])])
    for i in range(3):
        for j in range(5):
            data[i][j].sort()
    return data


def do_research():
    names = ['Normal distribution', 'Cauchy Distribution', 'Laplace Distribution',
             'Poisson Distribution', 'Uniform Distribution']
    character_names = ['Mean', 'Med', 'Zr', 'Zq', 'Ztr']
    character = [mean, med, z_r, z_q, z_tr]
    quantities = [10, 100, 1000]
    results = [[[[] for _ in range(5)] for _ in range(3)] for _ in range(5)]
    for i in range(1000):
        data = generate_data(quantities)
        for j in range(5):  # character
            for k in range(3):  # size
                for m in range(5):  # distribution
                    results[j][k][m].append(character[j](data[k][m]))
    for i in range(5):
        print(names[i])
        for j in range(3):
            print(f"N = {quantities[j]}")
            for k in range(5):
                print("E of", character_names[k], "=", mean(results[k][j][i]))
                print("D of", character_names[k], "=", var(results[k][j][i]))
