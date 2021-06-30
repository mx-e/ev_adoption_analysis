import pandas as pd
import sqlite3

density = pd.read_csv("other/pop_density.csv", delimiter=';', decimal=',', thousands=' ')
academics = pd.read_csv("other/percent_academics.csv", delimiter=';', decimal=',', thousands='.')
income = pd.read_csv("other/income_per_capita.csv", delimiter=';', decimal=',', thousands='.')

connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id FROM counties')

counties = db.fetchall()
missing_counties = []
for county in counties:
    stat_id = county[0]
    match_density = density.loc[density['Schlüssel-nummer'] == stat_id]
    if (len(match_density.index) == 0):
        print(f"NO DENSITY MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        pop_density = match_density.iloc(0)[0][-1]
        command = f'''UPDATE counties SET population_density = {pop_density} WHERE statistical_id = {stat_id}'''
        db.execute(command)

    match_academics = academics.loc[academics['krs1214'] == stat_id * 1000]
    if (len(match_academics.index) == 0):
        print(f"NO ACADEMICS MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        academics_share = match_academics.iloc(0)[0][-2]
        command = f'''UPDATE counties SET percent_academics = {academics_share} WHERE statistical_id = {stat_id}'''
        db.execute(command)


    match_income = income.loc[income['STAT_ID'] == stat_id]
    if (len(match_income.index) == 0):
        print(f"NO INCOME MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        income_per_capita = match_income.iloc(0)[0][-4]
        print(income_per_capita)
        command = f'''UPDATE counties SET income_per_capita = {income_per_capita} WHERE statistical_id = {stat_id}'''
        db.execute(command)
connection.commit()


print(missing_counties)