from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

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
          "startDate":"2017-01-08",
          "endDate":"2022-06-30"
        }],
      "metrics":[
        {
          "expression":"ga:pageviews"
        }],
      "dimensions": [
        {
          "name":"ga:pagePath"
        }]
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
