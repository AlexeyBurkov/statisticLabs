import math
import numpy as np


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


def pearson_correlation(xy):
    m_x = mean(xy[:, 0])
    m_y = mean(xy[:, 1])
    _xy = xy[:, 0].copy()
    for i in range(len(xy)):
        _xy[i] = (xy[i][0] - m_x) * (xy[i][1] - m_y)
    return mean(_xy) / np.sqrt(var(xy[:, 0]) * var(xy[:, 1]))


def quadrant_correlation(xy):
    m_x = med(xy[:, 0])
    m_y = med(xy[:, 1])
    n1, n2, n3, n4 = 0, 0, 0, 0
    for el in xy:
        if el[0] >= m_x:
            if el[1] >= m_y:
                n1 += 1
            else:
                n4 += 1
        else:
            if el[1] >= m_y:
                n2 += 1
            else:
                n3 += 1
    return (n1 + n3 - n2 - n4) / len(xy)


def spearman_correlation(xy):
    x = xy[:, 0].copy()
    y = xy[:, 1].copy()
    x.sort()
    y.sort()
    ranks = xy.copy()
    for i in range(len(ranks)):
        ranks[i][0] = np.where(x == ranks[i][0])[0]
        ranks[i][1] = np.where(y == ranks[i][1])[0]
    return pearson_correlation(ranks)
