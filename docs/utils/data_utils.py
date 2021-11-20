import sqlite3
import numpy as np
import plotly.express as px



TOTAL_VOTES_ID = 15
CDU_ID = 16
SPD_ID = 17
GREEN_ID = 18
FDP_ID = 19
LEFT_ID = 20
AFD_ID = 21
OTHERS_ID = 22

AREA_ID = 2
POPULATION_ID = 3
DENSITY_ID = 3

TOTAL_WORKFORCE_ID = 4
ACADEMICS_ID = 5

INCOME_ID = 6
CHARGERS_ID = 7

PETROL_ID = 8
BEV_ID = 12
HYBRID_ID = 11
OTHER_ID = 13
PLUG_IN_ID = 14

PLOTLY_COLORS = px.colors.qualitative.D3

COLORS = {
    CDU_ID: '#000000',
    SPD_ID: '#EB001F',
    GREEN_ID: '#64A12D',
    FDP_ID: '#FFED00',
    LEFT_ID: '#BE3075',
    AFD_ID: '#009EE0',
    OTHERS_ID: 'grey',
    DENSITY_ID: PLOTLY_COLORS[5],
    ACADEMICS_ID: PLOTLY_COLORS[1],
    INCOME_ID: PLOTLY_COLORS[4],
    CHARGERS_ID: PLOTLY_COLORS[3]
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
    ACADEMICS_ID: 'Education',
    INCOME_ID: 'Income',
    CHARGERS_ID: 'Charging'
}

get_color = lambda id: COLORS.get(id, 'lightgrey')
get_legend = lambda id: LEGEND.get(id, 'constant')

def getRawData(year, election_type='FEDERAL'):
    connection = sqlite3.connect("../data/ev_adoption.sqlite")
    db = connection.cursor()
    vehicle_year = year+1
    income_year = min(year, 2018)
    db.execute(f'''SELECT statistical_id, e.year, p.area, p.population,  e.total_workforce, e.academic_workforce, income_per_capita, coalesce(sum(cp.no_chargers), 0), petrol, diesel, gas, hybrid_total, battery_electric, other, hybrid_plug_in, total_votes, cdu_csu, spd, greens, fdp, the_left, afd, other_parties FROM counties
    JOIN vehicle_stock vs on counties.statistical_id = vs.county_id
    JOIN votes v on counties.statistical_id = v.county_id
    JOIN education e on counties.statistical_id = e.AGS
    JOIN income i on counties.statistical_id = i.AGS
    JOIN population p on counties.statistical_id = p.AGS
    LEFT JOIN charging_points cp on counties.statistical_id = cp.AGS
    WHERE vs.year = {vehicle_year} AND vote_type = 'FEDERAL' AND e.year = {year}  AND i.year = {income_year} AND p.year = {year}
    GROUP BY statistical_id''')
    data = np.array(db.fetchall(), dtype=np.float64)
    return data

# OUTLIERS
#BMW/MINI
# München, Stadt(9162)
#VW
# Wolfsburg (3103)
# Braunschweig(3101)
#RENAULT/NISSAN
# Köln, Stadt(5315)
#AUDI
# Ingolstadt (9161)
#MERCEDES
# Stuttgart (8111)
#SMART
# Boeblingen (8115)
#OPEL/PEUGEOT
# Gross-Gerau (6433)
#KIA
# Frankfurt a. Main (6412)
#HYUNDAI
# Offenbach a. Main (6413)
#SKODA
# Darmstadt (6411)

# Trier(7211)

outlier_ids = np.array([9162, 3103, 3101, 5315, 9161, 8111, 8115, 6433, 6412, 6413, 6411, 7211, 16055 ], dtype=np.float64)

def remove_outliers(data):
    ids = data[:, 0]
    inlier_ids = []
    for i, id in enumerate(ids):
        if (id not in outlier_ids):
            inlier_ids.append(i)
    return data[inlier_ids]

def pre_process(data):
    votes = data[:, CDU_ID:(OTHERS_ID + 1)].copy()
    total_votes = data[:, TOTAL_VOTES_ID].copy()
    votes = (votes.T / np.tile(total_votes, (votes.shape[1], 1))).T

    chargers = data[:, CHARGERS_ID].copy()
    total_cars = data[:, 4:10].copy().sum(axis=1)
    chargers = (chargers / total_cars)

    area = data[:, AREA_ID].copy()
    population = data[:, POPULATION_ID].copy()
    density = population / area

    total_workforce = data[:, TOTAL_WORKFORCE_ID].copy()
    academics = data[:, ACADEMICS_ID].copy()

    academics_share = academics / total_workforce


    pre_processed_data = data.copy()
    pre_processed_data[:, DENSITY_ID] = density / 1000.
    pre_processed_data[:, ACADEMICS_ID] = academics_share * 100
    pre_processed_data[:, CDU_ID:(OTHERS_ID + 1)] = votes * 100
    pre_processed_data[:, CHARGERS_ID] = chargers * 1000.
    pre_processed_data[:, INCOME_ID] /= 10000.

    return pre_processed_data

def get_X_custom(data, paramIds, standardize=False):
    X = data[:, paramIds]
    if standardize:
        X -= X.mean(axis=0)
        X /= X.std(axis=0)
    return X

def get_Y(data, measure_id, standardize=False):
    total_cars = data[:, PETROL_ID:(OTHER_ID+1)].sum(axis=1).copy()
    Y = data[:, measure_id] / total_cars * 1000
    if standardize:
        Y -= Y.mean(axis=0)
        Y /= Y.std(axis=0)
    return Y