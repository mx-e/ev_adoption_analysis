#%%
from matplotlib import pyplot as plt
import sys
import numpy as np
sys.path.append('./utils/data_utils.py')
from docs.utils.data_utils import *
from docs.make_tables import *
from docs.make_img import *
import statsmodels.api as sm
from scipy.stats.mstats import zscore


#%%
WORKING_SET_1 = [ INCOME_ID, CHARGERS_ID, GREEN_ID, AFD_ID, OTHERS_ID]
WORKING_SET_2 = [DENSITY_ID, ACADEMICS_ID, INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID ]
WORKING_SET_3 = [DENSITY_ID , INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, AFD_ID ]

STAND_SET_1=[ACADEMICS_ID, INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID ]

FULL_SET = [DENSITY_ID, ACADEMICS_ID, INCOME_ID, CHARGERS_ID, CDU_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID, AFD_ID, OTHERS_ID ]
YEARS = [2017, 2018, 2019, 2020]
PARAMS =[INCOME_ID, ACADEMICS_ID, DENSITY_ID, CHARGERS_ID, GREEN_ID, FDP_ID, LEFT_ID, AFD_ID ]
estimates = []
conf_widths = []
results_list = []
results_list_stand = []
for year in YEARS:
    data = remove_outliers(getRawData(year=year, election_type='FEDERAL'))
    X, Y = get_X_custom(pre_process(data), PARAMS, standardize=False), get_Y(data, measure_id=BEV_ID, standardize=False)
    X_s, Y_s = get_X_custom(pre_process(data), PARAMS, standardize=True), get_Y(data, measure_id=BEV_ID, standardize=True)
    n, _ = X.shape
    X = sm.add_constant(X)
    mod = sm.OLS(Y, X)
    res = mod.fit()
    results_list.append(res)

    mod_s = sm.OLS(Y_s, X_s)
    res_s = mod_s.fit()
    results_list_stand.append(res_s)
    print(res.summary(yname=get_legend(BEV_ID), xname=[0] + [get_legend(id) for id in PARAMS]))

#make_img(results_list_stand, YEARS, PARAMS)
PARAMS = [0] + PARAMS
make_tables(results_list, YEARS, PARAMS, n)



#%%
data = remove_outliers(getRawData(year=2019, election_type='FEDERAL'))
evs = get_Y(data, measure_id=BEV_ID, standardize=False)
print( evs.mean(), evs.std(), evs.max(), evs.argmax())
print(data[evs.argmax()])

#%%

def make_descriptive_img(Y, party_strengths, years, params):
    fig = go.Figure()
    mean = Y.mean(axis=1)
    strongest_party = party_strengths.argmax(axis=1)
    legend = [ f"best res for {get_legend(param)}" for param in params]
    print(mean)
    for j, county_y in enumerate(Y.T):

        color = get_color(params[strongest_party[j]])
        name = legend[strongest_party[j]]

        fig.add_trace(go.Scatter(x=years, y=Y[:, j],
                                 mode='lines',
                                 opacity=0.3 if color != '#FFED00' else 0.55,
                                 line=dict(color=color, width=2),
                                 name=name,
                                 showlegend=bool(np.argwhere(strongest_party == strongest_party[j])[0,0] == j)
                                 )
                      )
    fig.add_trace(go.Scatter(x=years, y=mean, mode='lines+markers', opacity=0.9, name='mean', line=dict(color='red', width=3)))
    fig.update_layout(
        margin=dict(l=10, r=20, t=10, b=10),
        height=600,
        width=800,
        yaxis_title='EVs per thousand cars (log)',
        yaxis=dict(type='log'),
        xaxis = dict(
            range=[2017, 2020],
            title = 'year',
            tickmode = 'array',
            tickvals = years
            )
        )
    fig.write_image("./img/descriptive.pdf")



YEARS = [2017, 2018, 2019, 2020]
party_params = [LEFT_ID, GREEN_ID, FDP_ID, AFD_ID]
data = [remove_outliers(getRawData(year=year, election_type='FEDERAL')) for year in YEARS]
evs = [get_Y(datum, measure_id=BEV_ID, standardize=False) for datum in data]
party_strengths = get_X_custom(pre_process(data[0]),party_params, standardize=True)
make_descriptive_img(np.array(evs), np.array(party_strengths), np.array(YEARS), party_params)

