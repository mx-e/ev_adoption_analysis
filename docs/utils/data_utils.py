import sqlite3
import numpy as np


TOTAL_VOTES_ID = 11
CDU_ID = 12
SPD_ID = 13
GREEN_ID = 14
FDP_ID = 15
LEFT_ID = 16
AFD_ID = 17
OTHERS_ID = 18

DENSITY_ID = 1
ACADEMICS_ID = 2
INCOME_ID = 3
CHARGERS_ID =19

BEV_ID = 8
HYBRID_ID = 7
PLUG_IN_ID = 10

COLORS = {
    CDU_ID: 'black',
    SPD_ID: 'red',
    GREEN_ID: 'green',
    FDP_ID: 'yellow',
    LEFT_ID: 'purple',
    AFD_ID: 'blue',
    OTHERS_ID: 'grey',
    DENSITY_ID: 'lightblue',
    ACADEMICS_ID: 'orange',
    INCOME_ID: 'violet',
    CHARGERS_ID: 'olive'
}

LEGEND = {
    CDU_ID: 'CDU/CSU',
    SPD_ID: 'SPD',
    GREEN_ID: 'Greens',
    FDP_ID: 'FDP',
    LEFT_ID: 'Left',
    AFD_ID: 'AfD',
    OTHERS_ID: 'other parties',
    DENSITY_ID: 'Pop. Density',
    ACADEMICS_ID: '% Academics',
    INCOME_ID: 'Income',
    CHARGERS_ID: 'Charging Points'
}

get_color = lambda id: COLORS.get(id, 'lightgrey')
get_legend = lambda id: LEGEND.get(id, 'constant')

def getRawData(year, election_type='FEDERAL'):
    connection = sqlite3.connect("./data/ev_adoption.sqlite")
    db = connection.cursor()
    db.execute(f'''SELECT statistical_id, population_density, percent_academics, income_per_capita, petrol, diesel, gas, hybrid_total, battery_electric, other, hybrid_plug_in, total_votes, cdu_csu, spd, greens, fdp, the_left, afd, other_parties, sum(cp.no_chargers) FROM counties
    JOIN vehicle_stock vs on counties.statistical_id = vs.county_id
    JOIN votes v on counties.statistical_id = v.county_id
    JOIN charging_points cp on counties.statistical_id = cp.AGS
    WHERE year = {year} AND vote_type = '{election_type}' AND cp.online_since < {year}
    GROUP BY counties.statistical_id ''')
    data = np.array(db.fetchall(), dtype=np.float64)
    return data

# OUTLIERS
# München, Stadt(9162)
# Hamburg (2000)
# Main-Taunus-Kreis (6436)
# Hochtaunuskreis (6434)
# Bochum, Stadt (5911)
# Regensburg, Stadt (9362)
# Euskirchen (5366)
#
# Wolfsburg (3103)
# Ingolstadt (9161)
# Stuttgart (8111)
# Heilbronn (8125)
# Boeblingen (8115)
# Koeln, Stadt (5315)
# Guenzburg (9774)
# Gross-Gerau (6433)
#
# Solingen (5122)
# Braunschweig(3101)
#
# Trier(7211)
# Weimar(16055)

outlier_ids = np.array([9162, 2000, 6436, 6434, 5911, 9362, 5366, 3103, 9161, 8111, 8125, 8115, 5315, 9774, 6433, 5122, 3101, 16055], dtype=np.float64)

def remove_outliers(data):
    ids = data[:, 0]
    inlier_ids = []
    for i, id in enumerate(ids):
        if (id not in outlier_ids):
            inlier_ids.append(i)
    return data[inlier_ids]

def pre_process(data):
    votes = data[:, CDU_ID:(OTHERS_ID + 1)]
    total_votes = data[:, TOTAL_VOTES_ID]
    votes = (votes.T / np.tile(total_votes, (votes.shape[1], 1))).T

    chargers = data[:, CHARGERS_ID]
    total_cars = data[:, 4:10].sum(axis=1)
    chargers = (chargers / total_cars)

    pre_processed_data = data.copy()
    pre_processed_data[:, CDU_ID:(OTHERS_ID + 1)] = votes
    pre_processed_data[:, CHARGERS_ID] = chargers

    return pre_processed_data

def get_X_custom(data, paramIds, standardize=False):
    X = data[:, paramIds]
    if standardize:
        X -= X.mean(axis=0)
        X /= X.std(axis=0)
    else:
        X /= X.mean(axis=0)
    return X

def get_Y(data, measure_id, standardize=False):
    total_cars = data[:, 4:10].sum(axis=1)
    Y = data[:, measure_id] / total_cars
    if standardize:
        Y -= Y.mean(axis=0)
        Y /= Y.std(axis=0)
    else:
        Y /= Y.mean()
    return Y