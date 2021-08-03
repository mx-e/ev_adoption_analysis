import pandas as pd
import sqlite3

income = pd.read_csv("other/income.csv", delimiter=';', decimal=',', thousands=' ')

connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id FROM counties')

counties = db.fetchall()
missing_counties = []
years = [2020, 2019, 2018, 2017]

for county in counties:
    stat_id = county[0]
    match_population = income.loc[income['ID'] == stat_id]
    if (len(match_population.index) != 2):
        print(f"NO MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        for i, row in match_population.iterrows():
            year, _, _, _, income_per_capita  = row.iloc(0)
            command = f'''INSERT INTO income (AGS, income_per_capita, year) VALUES ({stat_id}, {income_per_capita}, {year})'''
            db.execute(command)

connection.commit()

