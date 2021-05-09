import matplotlib.patches
import numpy as np
import matplotlib.pyplot as plt
from characteristics import pearson_correlation, spearman_correlation, quadrant_correlation, mean, var


def generate_data(quantities, rho):
    res = []
    for r in rho:
        res.append([np.random.multivariate_normal([0., 0.], [[1., r], [r, 1.]], n) for n in quantities])
    res.append([0.9 * np.random.multivariate_normal([0., 0.], [[1., 0.9], [0.9, 1.]], n) +
                0.1 * np.random.multivariate_normal([0., 0.], [[100., -90], [-90, 100.]], n)
                for n in quantities])
    return res


def do_correlation_research():
    rho = [0., 0.5, 0.9]
    quantities = [20, 60, 100]
    repeat = 1000
    characteristics = [pearson_correlation, quadrant_correlation, spearman_correlation]
    char_names = ['Pearson', 'Quadrant', 'Spearman']
    data = [[[[] for _ in range(len(characteristics))] for _ in range(len(quantities))] for _ in range(len(rho) + 1)]
    for i in range(repeat):
        temp_data = generate_data(quantities, rho)
        for j in range(len(characteristics)):
            for k in range(len(rho) + 1):
                for m in range(len(quantities)):
                    data[k][m][j].append(characteristics[j](temp_data[k][m]))
    for i in range(len(characteristics)):
        print(char_names[i])
        for k in range(len(rho)):
            for m in range(len(quantities)):
                temp = data[k][m][i].copy()
                for s in range(len(temp)):
                    temp[s] **= 2
                print(f'\trho = {rho[k]}, size = {quantities[m]}\n\t\tE = {mean(data[k][m][i])}\n'
                      f'\t\tE^2 = {mean(temp)}\n\t\tD = {var(data[k][m][i])}')
        for m in range(len(quantities)):
            temp = data[len(rho)][m][i].copy()
            for s in range(len(temp)):
                temp[s] **= 2
            print(f'\tmix, size = {quantities[m]}\n\t\tE = {mean(data[len(rho)][m][i])}\n'
                  f'\t\tE^2 = {mean(temp)}\n\t\tD = {var(data[len(rho)][m][i])}')


def draw_ellipse(x_0, y_0, h, w, angle, name, ax):
    ax.add_artist(matplotlib.patches.Ellipse((x_0, y_0), w, h, angle, facecolor='none', edgecolor='red'))
    ax.set_title(name)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_ylim(-5, 5)
    ax.set_xlim(-5, 5)


def do_ellipse_research():
    rho = [0., 0.5, 0.9]
    quantities = [20, 60, 100]
    names = ['Normal distribution, $\\rho$ = 0', 'Normal distribution, $\\rho$ = 0.5',
             'Normal distribution, $\\rho$ = 0.9', 'Mix of normal distributions']
    fnames = ['Normal distribution, r = 0', 'Normal distribution, r = 0.5',
              'Normal distribution, r = 0.9', 'Mix of normal distributions']
    data = generate_data(quantities, rho)
    for i in range(len(data)):
        _, axs = plt.subplots(1, len(quantities), figsize=(12, 4), dpi=100)
        plt.subplots_adjust(wspace=0.5)
        plt.suptitle(names[i])
        for j in range(len(quantities)):
            x_arr = data[i][j][:, 0].copy()
            y_arr = data[i][j][:, 1].copy()
            axs[j].scatter(x_arr, y_arr, s=3)
            d_x = var(x_arr)
            d_y = var(y_arr)
            r = pearson_correlation(data[i][j])
            angle_a = np.arctan(2 * r * np.sqrt(d_x * d_y) / (d_x - d_y)) / 2
            d_w = d_x * (np.cos(angle_a) ** 2) + r * np.sqrt(d_x * d_y) * np.sin(2 * angle_a) + \
                  d_y * (np.sin(angle_a) ** 2)
            d_h = d_x * (np.sin(angle_a) ** 2) - r * np.sqrt(d_x * d_y) * np.sin(2 * angle_a) + \
                  d_y * (np.cos(angle_a) ** 2)
            draw_ellipse(mean(x_arr), mean(y_arr), 6 * np.sqrt(d_h), 6 * np.sqrt(d_w), angle_a * 180 / np.pi,
                         f'size = {quantities[j]}', axs[j])
        plt.savefig('plots/lab5/' + fnames[i] + '.png', format='png')
        plt.show()
