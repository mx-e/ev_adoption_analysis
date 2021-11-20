import plotly, sys
import plotly.graph_objects as go
import numpy as np

sys.path.append('./utils/data_utils.py')
from docs.utils.data_utils import get_legend, get_color

def get_marker_value(p_value):
    if (p_value < 0.01): return 28
    if (p_value < 0.05): return 200
    if (p_value < 0.1): return 0
    return 100

def make_img(results_list, results_titles, params):
    fig = go.Figure()
    betas = np.array([result.params for result in results_list])
    p_values = np.array([result.pvalues for result in results_list])

    for j, id in enumerate(params):
        color = get_color(id)
        legend = get_legend(id)

        fig.add_trace(go.Scatter(x=results_titles, y=betas[:, j],
                                 mode='markers+lines',
                                 marker_symbol = list(map(get_marker_value, p_values[:,j])),
                                 marker_line_color= 'black',
                                 marker_color= color,
                                 marker_line_width=2.2,
                                 opacity=0.9,
                                 marker_size=16,
                                 name= legend,
                                 )
                      )
    fig.update_layout(
        margin=dict(l=10, r=20, t=10, b=10),
        height=600,
        width=800,
        yaxis_title='standardized beta',
        xaxis = dict(
            title = 'year',
            tickmode = 'array',
            tickvals = results_titles
            )
        )


    fig.write_image("./img/fig1.pdf")



