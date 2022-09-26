import pandas as pd
import datetime

df = pd.read_csv("final_consolidated_report.csv")

print(df.head())

def getDateRangeFromWeek(year_week):

    p_year = year_week[0:4]
    p_week = year_week[-2:]

    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)

    return firstdayofweek, lastdayofweek


# iterating the columns
for idx, col in enumerate(df.columns):

    if idx is not 0:
        firstdate, lastdate = getDateRangeFromWeek(col)

        firstdate = firstdate.strftime("%d%b")
        lastdate = lastdate.strftime("%d%b'%y")

        new_name = f'{firstdate}-{lastdate}'
        # print(f'{firstdate} to {lastdate}')

        df.rename(columns={col: new_name}, inplace=True)

print(df.head())

print("saving to csv...")
df.to_csv('renamed_final_consolidated_report.csv')
