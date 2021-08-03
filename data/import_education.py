import pandas as pd
import sqlite3

education = pd.read_csv("other/education.csv", delimiter=';', decimal=',', thousands='.')

connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id FROM counties')

counties = db.fetchall()
missing_counties = []
years = [2020, 2019, 2018, 2017]

for county in counties:
    stat_id = county[0]
    match_education = education.loc[education['ID'] == stat_id]
    if (len(match_education.index) == 0):
        print(f"NO MATCH FOR {stat_id}")
        missing_counties.append(stat_id)
    else:
        _, _, total_2017, voc_2017, acad_2017, total_2018, voc_2018, acad_2018, total_2019, voc_2019, acad_2019, total_2020, voc_2020, acad_2020 = match_education.iloc(0)[0]
        convert_float = lambda text: float(text.replace(',', '.'))
        pairs = list(zip([total_2020, total_2019, total_2018, total_2017],[voc_2020, voc_2019, voc_2018, voc_2017],[acad_2020, acad_2019, acad_2018, acad_2017]))
        for i, year in enumerate(years):
            command = f'''INSERT INTO education (AGS, total_workforce, vocation_workforce, academic_workforce, year) VALUES ({stat_id}, {pairs[i][0]}, {pairs[i][1]}, {pairs[i][2]}, {year})'''
            db.execute(command)

connection.commit()