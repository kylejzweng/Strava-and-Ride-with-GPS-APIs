import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd

# Authentication URL 
auth_url = "https://www.strava.com/oauth/token"

# URL used to access all the data.
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "INSERT CLIENT ID",
    'client_secret': 'INSERT CLIENT SECRET',
    'refresh_token': 'INSERT REFRESH TOKEN',
    'grant_type': "refresh_token",
    'f': 'json'
}

# Requesting an access token.
print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

# Using acquired access token for API request.
print("Requesting pages (200 activities per full page)...")
activities_df = pd.DataFrame()
page = 1
page_non_empty = True
while page_non_empty: 
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': page}
    my_activities = requests.get(activites_url, headers=header, params=param).json()
    activities_df = pd.concat([activities_df, pd.DataFrame([my_activities])], ignore_index=True)
    activities_df = activities_df._append(my_activities, ignore_index=True)
    page_non_empty = bool(my_activities)
    print(page)
    page = page + 1 

print("\n", len(activities_df), "activities downloaded")

# Only keeping columns I actually need for my analysis.
cols = ['name', 'upload_id', 'type', 'start_date_local', 'distance', 'moving_time', 
        'elapsed_time', 'total_elevation_gain', 'average_speed', 'max_speed', 
        'achievement_count', 'average_cadence', 'average_watts', 'average_heartrate'
       ]

activities_df = activities_df[cols]

print(activities_df)

# Saving data to .csv file for future analysis.
activities_df.to_csv('strava_activities_data.csv') 
