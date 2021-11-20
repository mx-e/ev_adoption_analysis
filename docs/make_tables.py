import sys, numpy as np
from tabulate import tabulate

sys.path.append('./utils/data_utils.py')
from docs.utils.data_utils import get_legend

def get_stars(p_value):
    if(p_value < 0.01): return '***'
    if(p_value < 0.05): return '**'
    if(p_value < 0.10): return '*'
    return ''

def make_tables(results_list, results_titles, params, n):
    headers_row_1 = ["Adoption Rate"]
    headers_row_2 = [f"(N={n})"]
    r2s = [result.rsquared for result in results_list]
    betas = np.array([results.params for results in results_list])
    p_values = np.array([result.pvalues for result in results_list])
    for i,title in enumerate(results_titles): headers_row_1.append(f"{title}")
    for i,title in enumerate(results_titles): headers_row_2.append(f"R2: {r2s[i]:.3f}")

    headers = headers_row_1
    table = [headers_row_2]
    for j, param in enumerate(params):
       row = [get_legend(param)]
       for i, mu in enumerate(betas):
           row.append(f"{mu[j]:.3f}{get_stars(p_values[i,j])}")
       table.append(row)

    print(tabulate(table, headers=headers, tablefmt='latex'))
    with open('tables.txt', 'w') as file:
        file.write(tabulate(table, headers=headers, tablefmt='latex'))


