import pandas as pd
import sqlite3

DATA_DIR = './data'
VOTES_DIR = f"{DATA_DIR}/votes/"

df = pd.read_csv(VOTES_DIR + 'votes.csv', delimiter=';', decimal=',', thousands='.')

connection = sqlite3.connect("./data/ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id FROM counties')

counties = db.fetchall()
missing_counties = []
for county in counties:
        match = df.loc[df['Statistical Id'] == county[0]]
        if len(match.index) == 0:
                print(f"NO MATCH FOR {county[0]}")
                missing_counties.append(county[0])
        else:
                date, stat_id, name, voters, participation, total_votes, cdu_csu, spd, greens, fdp, left, afd, others = match.iloc(0)[0]
                date = str(date)
                year_string = f"{date[-4:]}"
                insert_object = f"({stat_id}, {year_string}, {int(voters)}, {int(total_votes)}, {str(participation).replace(',','.')}, {int(cdu_csu)}, {int(spd)}, {int(greens)}, {int(fdp)}, {int(left)}, {int(afd)}, {int(others)})"
                print(insert_object)
                db.execute(f'''INSERT INTO votes(COUNTY_ID, VOTE_YEAR, VOTERS, TOTAL_VOTES, PARTICIPATION, CDU_CSU, SPD, GREENS, FDP, THE_LEFT, AFD, OTHER_PARTIES)
                           VALUES{insert_object}''')

connection.commit()
print(missing_counties)
