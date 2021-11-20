import sqlite3
import pandas as pd

charging_points = pd.read_csv("other/charging_points.csv", delimiter=';', decimal=',', thousands=' ')


def extract_type(str):
    type_descr = str.split(' ')[0]
    return 'STADT' if type_descr == 'Stadtkreis' or type_descr == 'Kreisfreie' else 'LAND'

def extract_name(str):
    name = str.replace('Kreisfreie Stadt ', '').replace('Landkreis ', '').replace('Stadtkreis ', '').replace('Kreis ', '').upper()
    name = name.replace('Ü', 'UE').replace('Ä', 'AE').replace('Ö', 'OE').strip()
    return name

manual_map = {
    'SCHWAEBISCH HALL': 8127,
    'FREIBURG IM BREISGAU': 8311,
    'AMBERG': 9361,
    'KEMPTEN (ALLGAEU)': 9763,
    'WEIDEN I.D. OPF.': 9363,
    'DILLINGEN A.D. DONAU': 9773,
    'MUEHLDORF A. INN': 9183,
    'NEUMARKT I.D. OPF.': 9373,
    'NEUSTADT A.D. AISCH-BAD WINDSHEIM': 9575,
    'WUNSIEDEL I. FICHTELGEBIRGE':9479,
    'MECKLENBURGISCHE SEENPLATTE':13071,
    'NIENBURG (WESER)': 3256,
    'REGION HANNOVER': 3241,
    'NEUSTADT A.D. WALDNAAB': 9374,
    'PFAFFENHOFEN A.D. ILM': 9186,
    'BRANDENBURG AN DER HAVEL':12051,
    'ROTENBURG (WUEMME)' :3357,
    'FRANKFURT (ODER)': 12053,
    'RHEINISCH-BERGISCHER KREIS': 5378,
    'RHEIN-NEUSS': 5162,
    'STAEDTEREGION AACHEN': 5334,
    'MUELHEIM AN DER RUHR': 5117,
    'LANDAU IN DER PFALZ': 7313,
    'NEUSTADT AN DER WEINSTRASSE': 7316,
    'FRANKENTHAL (PFALZ)': 7311,
    'ALTENKIRCHEN (WESTERWALD)': 7132,
    'REGIONALVERBAND SAARBRUECKEN': 10041,
    'SAARPFALZ-KREIS': 10045,
    'SAECHSISCHE SCHWEIZ-OSTERZGEBIRGE': 14628,
    'SAALE-HOLZLAND-KREIS': 16074,
    'LUDWIGSHAFEN AM RHEIN': 7314,
    'ST. WENDEL': 10046,
    'WEIMARER LAND': 16071,
    'OLDENBURG (OLDB)': 3403,
    'OLDENBURG': 3458,
    'TRIER': 7211,
}


connection = sqlite3.connect("ev_adoption.sqlite")
db = connection.cursor()
db.execute('SELECT statistical_id, type, name FROM counties')
counties_data = db.fetchall()
counties = pd.DataFrame(counties_data, columns =['ID', 'TYPE', 'NAME'])
counties['NAME'] = counties['NAME'].apply(lambda str: str.replace(',STADT', '').replace(',LAND', ''))

def find_county(type, name):

    matched = counties.loc[counties['NAME'] == name]
    if(len(matched.index) == 0):
        return None
    elif(len(matched.index) > 1):
        matched = matched.loc[matched['TYPE'] == type]
        if (len(matched.index) != 1):
            return None
        return matched
    else: return matched

unmatched, matched = [], []

for row in charging_points.iterrows():
    kreis = row[1]['Landkreis']
    name, type_desc = extract_name(kreis), extract_type(kreis)
    match = find_county(type_desc, name)
    if(match is None):
        id = manual_map.get(name, None)
        if(id is None):
            unmatched.append((name, type_desc))
            print(name, type_desc, kreis)
        else:
            matched.append(name)
    else:
        id = match.iloc(0)[0]['ID']
        matched.append(name)
    plz = int(row[1][2][:5])
    ort = row[1][2][6:]
    lk = row[1][4]
    ort = ort.strip()
    ags = id
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
        print(insert_object)
        db.execute(f'''insert into charging_points (AGS, address, plz, town, online_since, total_output, no_chargers, type, operator)
                        VALUES{insert_object}''')
    except:
        print(insert_object)

print(len(matched), len(unmatched))
print(unmatched)

connection.commit()
