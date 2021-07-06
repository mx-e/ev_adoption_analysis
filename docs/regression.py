#%%
from matplotlib import pyplot as plt
import sys
sys.path.append('./utils/data_utils.py')
from docs.utils.data_utils import *
import statsmodels.api as sm


#%%
WORKING_SET_1 = [ INCOME_ID, CHARGERS_ID, GREEN_ID, AFD_ID, OTHERS_ID]
WORKING_SET_2 = [DENSITY_ID, ACADEMICS_ID, INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID ]
WORKING_SET_3 = [DENSITY_ID , INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, AFD_ID ]

STAND_SET_1=[ACADEMICS_ID, INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID ]



FULL_SET = [DENSITY_ID, ACADEMICS_ID, INCOME_ID, CHARGERS_ID, CDU_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID, AFD_ID, OTHERS_ID ]
YEARS = [2018, 2019, 2020, 2021]
PARAMS =[ INCOME_ID, CHARGERS_ID, GREEN_ID, AFD_ID, OTHERS_ID]
estimates = []
conf_widths = []
for year in YEARS:
    data = remove_outliers(getRawData(year=year, election_type='FEDERAL'))
    X, Y = get_X_custom(pre_process(data), PARAMS, standardize=True), get_Y(data, measure_id=BEV_ID, standardize=True)
    mod = sm.OLS(Y, X)
    res = mod.fit()
    estimates.append(res.params)
    conf =  res.conf_int(alpha=0.05, cols=None)
    conf_w = abs(res.params - conf[:, 0])
    conf_widths.append(conf_w)

results = np.array(estimates)
conf_widths = np.array(conf_widths)

plt.figure(figsize=(8, 8))

for i, id in enumerate(PARAMS):
    plt.errorbar(YEARS, results[:, i], yerr=conf_widths[:, i], c=get_color(id), label=get_legend(id), alpha=1, capsize=4)

plt.legend(loc=2)
plt.show()
#%%

PARAMS = [DENSITY_ID, ACADEMICS_ID, INCOME_ID, CHARGERS_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID ]
YEAR = 2018

data = remove_outliers(getRawData(year=YEAR, election_type='FEDERAL'))
X, Y = get_X_custom(pre_process(data), PARAMS, standardize=True), get_Y(data, measure_id=BEV_ID, standardize=True)
mod = sm.OLS(Y, X)
res = mod.fit()
print(res.summary(yname='BEV',xname=list(map(get_legend, PARAMS))))