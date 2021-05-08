import numpy as np
import math as math
from characteristics import mean, med, z_r, z_q, z_tr, var


def _generate_data(quantities):
    data = []
    for i in range(len(quantities)):
        data.append([np.random.normal(0, 1, quantities[i]), np.random.standard_cauchy(quantities[i]),
                     np.random.laplace(0, np.sqrt(3), quantities[i]), np.random.poisson(10, quantities[i]),
                     np.random.uniform(-np.sqrt(3), np.sqrt(3), quantities[i])])
    for i in range(len(quantities)):
        for j in range(5):
            data[i][j].sort()
    return data


def _count_numbers_after_coma(x):
    r1, r2 = math.modf(x)
    if r2 != 0.0:
        return 3
    res = 0
    r1 *= 10
    while True:
        _, t1 = math.modf(r1)
        if t1 != 0.0:
            break
        res += 1
        r1 *= 10
    return res + 3


def _print_result_as_latex_table(results, quantities, names):
    for i in range(len(names)):
        print('\\begin{table}[H]\n\t\\centering')
        print('\t\\begin{tabular}{||c|p{2.65cm}|p{2.65cm}|p{2.65cm}|p{2.65cm}|p{2.65cm}||}\n\t\\hline')
        print('\t& $\\overline{x}$(\\ref{eq:8}) & $med~x$(\\ref{eq:9}) & $z_R$(\\ref{eq:10}) & $z_Q$(\\ref{eq:11}) & '
              '$z_{tr}$(\\ref{eq:12})\\\\\n\t\\hline')
        for j in range(len(quantities)):
            print('\t$n =', quantities[j], '$& & & & & \\\\\n\t\\hline\n\t$E$', end='')
            if j == 0:
                print('(\\ref{eq:1})', end='')
            e_arr = []
            d_arr = []
            accuracies = []
            for k in range(len(results)):
                e_arr.append(mean(results[k][j][i]))
                d_arr.append(var(results[k][j][i]))
            for k in range(len(results)):
                accuracies.append(max(_count_numbers_after_coma(e_arr[k]), _count_numbers_after_coma(d_arr[k])))
            for k in range(len(results)):
                print(' & $%.*f$' % (accuracies[k], e_arr[k]), end='')
            print(' \\\\\n\t\\hline\n\t$D$', end='')
            if j == 0:
                print('(\\ref{eq:2})', end='')
            for k in range(len(results)):
                print(' & $%.*f$' % (accuracies[k], d_arr[k]), end='')
            print(' \\\\\n\t\\hline\n\t$E\\pm \\sqrt{D}$', end='')
            for k in range(len(results)):
                print(' & $[%.*f,$ $%.*f]$' % (accuracies[k], e_arr[k] - np.sqrt(d_arr[k]),
                                               accuracies[k], e_arr[k] + np.sqrt(d_arr[k])), end='')
            print(' \\\\\n\t\\hline\n\t$\\hat{E}$ & $ $ & $ $ & $ $ & $ $ & $ $ \\\\\n\t\\hline')
        print('\t\\end{tabular}\n\t\\caption{', names[i], '}\n\t\\label{tab:', i + 1, '}\n\\end{table}\n')


def do_characteristics_research():
    names = ['Нормальное распределение', 'Распределение Коши', 'Распределение Лапласа',
             'Распределение Пуассона', 'Равномерное распределение']
    character = [mean, med, z_r, z_q, z_tr]
    quantities = [10, 100, 1000]
    results = [[[[] for _ in range(5)] for _ in range(3)] for _ in range(5)]
    repeat = 1000
    for i in range(repeat):
        data = _generate_data(quantities)
        for j in range(len(character)):
            for k in range(len(quantities)):
                for m in range(len(names)):
                    results[j][k][m].append(character[j](data[k][m]))
    _print_result_as_latex_table(results, quantities, names)
