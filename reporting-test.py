from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pickle

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'credentials.json'
VIEW_ID = '96754763'

credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
# Build the service object.
analyticsreporting = build('analyticsreporting', 'v4', credentials=credentials)

response = analyticsreporting.reports().batchGet(
  body={
    "reportRequests":[
    {
      "viewId":VIEW_ID,
      "dateRanges":[
        {
          "startDate":"2017-01-01",
          "endDate":"2022-09-20"
        }],
      "metrics":[
        {
          "expression":"ga:pageviews"
        }],
      "dimensions": [
        {
          "name":"ga:pagePath"
        },{
          "name":"ga:yearWeek"
        }],
      "dimensionFilterClauses": [
        {
          "filters": [
            {
              "dimensionName": "ga:pagePath",
              "not": True,
              "expressions": [
                "\?(.*)$"
              ]
            }
          ]
        }
      ],
      "orderBys": [
        {
          "fieldName": "ga:yearWeek"
        }
      ],
      "pivots": [
        {
          "dimensions": [
            {
              "name": "ga:yearWeek"
            }
          ],
          "metrics": [
            {
              "expression": "ga:pageviews"
            }
          ],
          "maxGroupCount": 500
        }
      ],
      "hideTotals": True,
      "pageSize": 100,
      }]
  }
).execute()


def printResults(response):
  for report in response.get("reports", []):
    columnHeader = report.get("columnHeader", {})
    dimensionHeaders = columnHeader.get("dimensions", [])
    metricHeaders = columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])
    rows = report.get("data", {}).get("rows", [])
    # print(len(rows))
    # continue

    for row in rows:
      dimensions = row.get("dimensions", [])
      dateRangeValues = row.get("metrics", [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ": " + dimension)

      for i, values in enumerate(dateRangeValues):
        print("    Date range index: " + str(i))
        for metric, value in zip(metricHeaders, values.get("values")):
          print("    "  + metric.get("name") + ": " + value)

# printResults(response)
pprint(response)

with open('response.pkl', 'wb') as fh:
  pickle.dump(response, fh)
