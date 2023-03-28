import pandas as pd
import numpy as np
import time
from cassandra.cluster import Cluster
import datetime


def get_session(cluster):
    try:
        return cluster.connect()
    except:
        return None


print("Starting ELT Process")
# Configuration de la connexion à Cassandra
cluster = Cluster(['cassandra'])
session = None
while (not session):
    time.sleep(10)
    session = get_session(cluster)

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS mykeyspace 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
""")
session.execute("USE mykeyspace")
session.execute("""
    CREATE TABLE IF NOT EXISTS mytable (
        id int PRIMARY KEY,
        Province_State text,
        Country_Region text,
        Lat float,
        Long float,
        date text,
        confirmed_cases int,
        recovered_cases int,
        death_cases int
    );
""")


"""
First File Proccessing
"""


confirmed_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
confirmed_global_df = pd.read_csv(confirmed_global_url)


# Define the columns to use for pivoting
id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']
value_vars = confirmed_global_df.columns[4:]

# Pivot the dataframe
confirmed_global_df_pivot = pd.melt(confirmed_global_df, id_vars=id_vars,
                                    value_vars=value_vars, var_name='Date', value_name='confirmed_cases')


"""
Second File Proccessing
"""

recovered_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
recovered_global_df = pd.read_csv(recovered_global_url)


# Define the columns to use for pivoting
id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']
value_vars = recovered_global_df.columns[4:]

# Pivot the dataframe
recovered_global_df_pivot = pd.melt(recovered_global_df, id_vars=id_vars,
                                    value_vars=value_vars, var_name='Date', value_name='recovered_cases')


"""
Third File Proccessing
"""


deaths_global_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
deaths_global_df = pd.read_csv(deaths_global_url)

# Define the columns to use for pivoting
id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']
value_vars = deaths_global_df.columns[4:]

# Pivot the dataframe
deaths_global_df_pivot = pd.melt(deaths_global_df, id_vars=id_vars,
                                 value_vars=value_vars, var_name='Date', value_name='death_cases')


# Merge the dataframes on the common columns
df_merged = confirmed_global_df_pivot.merge(recovered_global_df_pivot, on=[
                                            'Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])
df_merged = df_merged.merge(deaths_global_df_pivot, on=[
                            'Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])

df_clean = df_merged

df_clean['Province/State'] = df_clean['Province/State'].replace(
    np.nan, '', regex=True)
df_clean['Country/Region'] = df_clean['Country/Region'].replace(
    np.nan, '', regex=True)
df_clean['Lat'] = df_clean['Lat'].replace(np.nan, 0.0, regex=True)
df_clean['Long'] = df_clean['Long'].replace(np.nan, 0.0, regex=True)
df_clean['Date'] = df_clean['Date'].replace(np.nan, '', regex=True)


print("Starting insertion into cassandra")

# Envoi des données sur Cassandra
for i, row in df_clean.iterrows():
    print('adding data: ',i)
    session.execute(
        """
        INSERT INTO mytable (id, Province_State, Country_Region, Lat, Long, date, confirmed_cases, recovered_cases, death_cases) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (i, row['Province/State'], row['Country/Region'], row['Lat'], row['Long'],
            row['Date'], row['confirmed_cases'], row['recovered_cases'], row['death_cases'])
    )

# Fermeture de la connexion à Cassandra
cluster.shutdown()


print("Ending ELT Process")
