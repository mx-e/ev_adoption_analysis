import pandas as pd
import sqlite3

DATA_DIR =  './data'
VEHICLE_REGISTRATION_DIR = f"{DATA_DIR}/registration/"


data = {2021: pd.read_csv(VEHICLE_REGISTRATION_DIR + '2021-2021.csv', delimiter=';', decimal=',', thousands='.'),
         2020:pd.read_csv(VEHICLE_REGISTRATION_DIR + '2020-2020.csv' , delimiter=';', decimal=',', thousands='.'),
         2019: pd.read_csv(VEHICLE_REGISTRATION_DIR + '2019-2019.csv', delimiter=';' , decimal=',', thousands='.'),
         2018: pd.read_csv(VEHICLE_REGISTRATION_DIR + '2018-2018.csv', delimiter=';', decimal=',', thousands='.' )
         }

connection = sqlite3.connect("./data/ev_adoption.sqlite")
db = connection.cursor()
years = [2018, 2019, 2020, 2021]

for year in years:
    for row in data[year].iterrows():
        county = row[1][0]
        if(isinstance(county, str)):
            county_id, county_name = county.split('  ')
            county_id = county_id.strip(' ')

            petrol, diesel, gas, hybrid_total, hybrid_plug_in, bev, other = row[1][1:]
            insert_object = f"({county_id}, {year}, {int(petrol)}, {int(diesel)}, {int(gas)}, {int(hybrid_total)}, {int(hybrid_plug_in)}, {int(bev)}, {int(other)})"
            db.execute(f'''INSERT INTO vehicle_stock(COUNTY_ID, YEAR, PETROL, DIESEL, GAS, HYBRID_TOTAL, HYBRID_PLUG_IN, BATTERY_ELECTRIC, OTHER)
            VALUES{insert_object}''')
connection.commit()

