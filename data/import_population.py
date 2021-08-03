import pandas as pd
import sqlite3

population = pd.read_csv("other/population.csv", delimiter=';', decimal=',', thousands=' ')

connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id FROM counties')

counties = db.fetchall()
missing_counties = []
years = [2020, 2019, 2018, 2017]

for county in counties:
    stat_id = county[0]
    match_population = population.loc[population['ID'] == stat_id]
    if (len(match_population.index) == 0):
        print(f"NO MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        _, _, pop_2020, pop_2019, pop_2018, pop_2017, area2020, area2019, area2018, area2017 = match_population.iloc(0)[0]
        convert_float = lambda text: float(text.replace(',', '.'))
        pairs = list(zip([pop_2020, pop_2019, pop_2018, pop_2017], list(map(convert_float, [area2020, area2019, area2018, area2017]))))
        for i, year in enumerate(years):
            command = f'''INSERT INTO population (AGS, population, area, year) VALUES ({stat_id},{pairs[i][0]},{pairs[i][1]},{year})'''
            db.execute(command)

connection.commit()