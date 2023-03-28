import pandas as pd
from cassandra.cluster import Cluster
from elasticsearch import Elasticsearch, helpers
import os, uuid


elastic = Elasticsearch('elasticsearch:9200', http_auth=('elastic', 'secret'))


print("Starting Indexation Process")
# Configuration de la connexion à Cassandra
cluster = Cluster(['cassandra'])
session = cluster.connect()

# Select data from a table
result_set = session.execute("SELECT * FROM mykeyspace.mytable ;")


reformat_objects = []
# Loop over the result set and print each row
for row in result_set:
    if row.id == 23:
        continue
    single_object = {
        "id": row.id,
    "confirmed_cases" : row.confirmed_cases,
    "country_region" : row.country_region,
    "date" : row.date,
    "death_cases" : row.death_cases,
    "lat" : row.lat,
    "long" : row.long,
    "province_state" : row.province_state,
    "recovered_cases" : row.recovered_cases
    }
    reformat_objects.append(single_object)

try:
    # make the bulk call, and get a response
    #response = helpers.bulk(elastic, bulk_json_data("coachs.json", "abdata", "coach"))

    response = helpers.bulk(elastic, reformat_objects, index='covid', doc_type='samples')
    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)

# Close the Cassandra session and cluster connection
cluster.shutdown()


print("Ending Indexation Process")





 




