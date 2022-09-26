import pickle
import pandas as pd
from pprint import pprint
import os

pickle_off = open("reports/response-100000-200000.pkl", "rb")
response = pickle.load(pickle_off)

# pprint(response)

report = response.get('reports')[0]

column_header = report.get('columnHeader')
data = report.get('data')

# pprint(column_header)
# pprint(data)

dimensions = column_header.get('dimensions')

dimension_values = []

pvt_header_entries = column_header['metricHeader']['pivotHeaders'][0]['pivotHeaderEntries']

for pvt_header_entry in pvt_header_entries:
    # print(pvt_header_entry.get('dimensionValues'))
    dimension_values.append(pvt_header_entry.get('dimensionValues')[0])

df = pd.DataFrame(columns=sorted(dimension_values))
# df = pd.DataFrame(columns=[dimensions[0]]+dimension_values)
# df.set_index(dimensions[0])
# print(df)


root, folders, files = next(os.walk("reports"))
# print(root, folders, files)

for file in files:
    pickle_off = open(os.path.join(root, file), "rb")
    response = pickle.load(pickle_off)

    report = response.get('reports')[0]

    data = report.get('data')

    rows = data.get('rows')

    for row in rows:
        dimension = row['dimensions']
        value = row['metrics'][0]['values'][0]
        df.loc[dimension[0], dimension[1]] = value
        # print(dimension)

# print(dimensions)
print(df.head().to_string())

print("saving to csv...")
df.to_csv('final_consolidated_report.csv')
