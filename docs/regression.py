#%%
from matplotlib import pyplot as plt
import sys
sys.path.append('./utils/data_utils.py')
from docs.utils.data_utils import *
import statsmodels.api as sm

PETROL_ID = 4
DIESEL_ID = 5
HYBRID_ID = 7
BEV_ID = 8
PLUG_IN_HYBRID_ID = 10

CDU_ID = 12
SPD_ID = 13
GREEN_ID = 14
FDP_ID = 15
LEFT_ID = 16
AFD_ID = 17
OTHERS_ID = 18


#%%

data = remove_outliers(getRawData(year=2021, election_type='FEDERAL'))

X, Y = get_X_all_parties(data), get_Y(data, measure_id=BEV_ID)
print(X.shape, Y.shape)
X = sm.add_constant(X)
mod = sm.OLS(Y, X)
res = mod.fit()
print(res.params)
print(res.summary())

#%%
plt.scatter(X[:,11],Y)
plt.show()

#%%

PARTIES = [CDU_ID, SPD_ID, GREEN_ID, FDP_ID, LEFT_ID, AFD_ID, OTHERS_ID]
YEARS = [2018, 2019, 2020, 2021]

COLORS_SINGLE = ['black', 'red', 'green', 'yellow', 'purple', 'blue', 'grey']
COLORS_ALL = ['lightgrey','lightblue', 'orange', 'violet', 'olive', 'black', 'red', 'green', 'yellow', 'purple', 'blue', 'grey']
LEGEND_ALL = ['constant', 'Pop. Density', '% Academics', 'Income', 'Charging Points', 'CDU/CSU', 'SPD', 'Greens', 'FDP', 'Left', 'AfD', 'other parties']
LEGEND_SINGLE = ['CDU/CSU', 'SPD', 'Greens', 'FDP', 'Left', 'AfD', 'other parties']
#%%

all_party_results = []
for year in YEARS:
    data = remove_outliers(getRawData(year=year, election_type='FEDERAL'))
    X, Y = get_X_all_parties(data), get_Y(data, measure_id=BEV_ID)
    X = sm.add_constant(X)
    mod = sm.OLS(Y, X)
    res = mod.fit()
    all_party_results.append(res.params)

results = np.array(all_party_results)
print(results.shape)

plt.figure(figsize=(8, 8))

for elem in range(results.shape[1]):
    plt.plot(YEARS, results[:, elem], c=COLORS_ALL[elem], label=LEGEND_ALL[elem])

plt.legend(loc=2)
plt.show()

#%%

party_results = np.zeros((len(PARTIES), len(YEARS), 5))

for i, party_id in enumerate(PARTIES):
    for j, year in enumerate(YEARS):
        data = remove_outliers(getRawData(year=year, election_type='FEDERAL'))
        X, Y = get_X_single_party(data, party_id) ,get_Y(data, measure_id=BEV_ID)
        X = sm.add_constant(X)
        mod = sm.OLS(Y, X)
        res = mod.fit()
        party_results[i, j, :] = res.params

plt.figure(figsize=(8, 8))

for elem in range(len(COLORS_SINGLE)):
    plt.plot(YEARS, party_results[elem, :, 0], c='lightgrey', label='constant' if elem == 0 else None)
    plt.plot(YEARS, party_results[elem, :, 1], c='lightblue', label='Pop. Density' if elem == 0 else None)
    plt.plot(YEARS, party_results[elem, :, 2], c='orange', label='% Academics' if elem == 0 else None)
    plt.plot(YEARS, party_results[elem, :, 3], c='violet', label='Income' if elem == 0 else None)
    plt.plot(YEARS, party_results[elem, :, 4], c=COLORS_SINGLE[elem], label=LEGEND_SINGLE[elem])


plt.legend(loc=2)
plt.show()