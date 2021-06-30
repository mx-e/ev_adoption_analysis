import pandas as pd
import sqlite3
from data.other.plz_util import *

connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id, name FROM counties')

counties = db.fetchall()

def tr_lk(lk):
    lk_tr = lk.replace('Landkreis', '').replace('Stadtkreis', '').replace('Kreis', '').replace('Kreisfreie Stadt','').upper().replace('FREIE STADT', '').replace('REGIONALVERBAND', '').replace('REGION', '').strip()
    return lk_tr

def tr_lk_more(lk_tr):
    lk_tr_more = lk_tr.replace('Ö', 'OE').replace('Ü', 'UE').replace('Ä', 'AE').strip()
    return lk_tr_more

def rm_ws(str):
    return str.replace(' ', '').replace('-', '')


hardcoded_lk = {
    'MECKLENBURGISCHE SEENPLATTE':13071,
    'FRANKFURT (ODER)': 12053,
    'NEUSTADT A.D. AISCH-BAD WINDSHEIM':9575,
    'WUNSIEDEL I. FICHTELGEBIRGE': 9479,
    'RHEIN- NEUSS': 5162,
    'NEUSTADT AN DER WEINSTRASSE': 7316,
    'ST. WENDEL': 10046,
    'FREIBURG IM BREISGAU': 8311,
    'MUELHEIM AN DER RUHR': 5117,
    'ALTENKIRCHEN (WESTERWALD)': 7132,
    'SAECHSISCHE SCHWEIZ-OSTERZGEBIRGE': 14521
}

def ags_from_lk(lk):
    lk_tr = tr_lk(lk)
    for ags, name in counties:
        if(lk_tr in name):
            return ags
    lk_tr2 = tr_lk_more(lk_tr)
    for ags, name in counties:
        if (lk_tr2 in name):
            return ags
    if (hardcoded_lk.get(lk_tr2, None)):
        return hardcoded_lk.get(lk_tr2)
    lk_tr2_nws = rm_ws(lk_tr2)
    for ags, name in counties:
        if (lk_tr2_nws in rm_ws(name)):
            return ags
    return None

charging_points = pd.read_csv("other/charging_points.csv", delimiter=';', decimal=',', thousands=' ')
plz_data = load_plz_ags_mapping()

print(plz_data)

accounted = 0
non_accounted = 0

for row in charging_points.iterrows():
    plz = row[1][2][:5]
    ort = row[1][2][6:]
    lk = row[1][4]
    ort = ort.strip()
    ags = ags_from_plz(plz_data, ort)
    no_chargers = row[1][10]
    if(ags == None):
        ags = ags_from_lk(lk)
    if(ags == None):
        ags = ags_from_ort(plz_data, ort)
    if(ags == None):
        non_accounted += no_chargers
        print(ort)
    else:
        accounted += no_chargers

    ags = int(ags)
    plz = int(plz)
    ort = ort.strip()
    operator = row[1][0].strip()
    address = row[1][1].replace("'", '').strip()
    online_since = int(row[1][7].split('.')[-1])
    no_chargers = int(row[1][10])
    total_output = int(row[1][8])
    type = row[1][9]
    insert_object = f"({ags}, '{address}', {plz}, '{ort}', {online_since}, {total_output}, {no_chargers}, '{type}', '{operator}')"
    try:
        db.execute(f'''insert into charging_points (AGS, address, plz, town, online_since, total_output, no_chargers, type, operator)
                    VALUES{insert_object}''')
    except:
        print(insert_object)
connection.commit()
