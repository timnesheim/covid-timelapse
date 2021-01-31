#!/usr/bin/env python3.7

import pandas as pd
import numpy as np
import geopandas as gpd
import datetime as dt
import json

# importing and cleaning case data from NYT
def get_case_data():

    df = pd.read_csv('./us-counties.csv')
    df = df[df['county'] != 'Unknown']
    df['deaths'] = df['deaths'].fillna(0)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date

    df.loc[(df['county'] == 'New York City') & (df['fips'].isnull()), 'fips'] = 36061.0
    df.loc[(df['county'] == 'Joplin') & (df['fips'].isnull()), 'fips'] = 29097.0
    df.loc[(df['county'] == 'Kansas City') & (df['fips'].isnull()), 'fips'] = 29037.0

    df[['fips','deaths']] = df[['fips','deaths']].astype(int)
    df['fips'] = df['fips'].astype(str)

    df['fips_updated'] = df['fips'].apply(lambda x: '0' + x if len(x) == 4 else x)

    df['cases_total'] = df['cases'].apply(lambda x: np.cumsum(x)[0])
    df['deaths_total'] = df['deaths'].apply(lambda x: np.cumsum(x)[0])

    df['group_id'] = df.groupby('date').grouper.group_info[0]

    return df

cases_df = get_case_data()








# importing county json info
with open('./counties.json') as f:
    counties = json.load(f)

if __name__ == '__main__':
    get_case_data()
