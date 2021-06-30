
#%%
import pandas as pd
def load_plz_ags_mapping():
    with open('/Users/maxi/WORKSPACE/EV_ADOPTION_ANALYSIS/data/other/GV100AD_311219.txt') as f:
        lines = f.readlines()

    plz=[]
    ags=[]
    unique=[]
    gemeinde=[]
    gemeindeverband=[]
    for line in lines:
        plz.append(line[165:170])
        ags.append(line[10:16])
        unique.append(line[170:175])
        gemeinde.append(line[22:72])
        gemeindeverband.append(line[72:122])

    data = {"PLZ": plz, 'AGS': ags, 'unique': unique, 'gemeinde':gemeinde, 'gemeindeverband':gemeindeverband}
    df = pd.DataFrame(data)
    print(df["gemeinde"])
    return df


def ags_from_plz(data, plz):
    filtered_data = data.loc[data['PLZ'] == plz]
    if (filtered_data.shape[0] == 0):
        return None
    return filtered_data.iloc[0][1]

def ags_from_ort(data, ort):
    filtered_data = data[data['gemeinde'].str.contains(ort)]
    if (filtered_data.shape[0] == 0):
        filtered_data = data[data['gemeindeverband'].str.contains(ort)]
    ort_transformed = ort.split('-')[0].strip()
    if (filtered_data.shape[0] == 0):
        filtered_data = data[data['gemeinde'].str.contains(ort_transformed)]
    if (filtered_data.shape[0] == 0):
        filtered_data = data[data['gemeindeverband'].str.contains(ort_transformed)]
    if (filtered_data.shape[0] == 0):
        return None
    return filtered_data.iloc[0][1]