import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize

# URL used to access all data
activites_url = "https://ridewithgps.com/users/3350753/trips.json"

access_token = 'INSERT TOKEN HERE'

# API request
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
response = requests.get(activites_url, headers=header, params=param)
activities_data = response.json()
activities_df = pd.DataFrame(activities_data)
activites_df = json_normalize(activities_df)

# Only keeping the columns that are actually useful to my analysis.
cols = ['user_id', 'id', 'created_at', 'distance', 'duration', 'elevation_gain', 'avg_cad', 'max_cad', 'avg_speed',
        'max_speed', 'moving_time', 'avg_watts', 'max_watts', 'calories', 'locality', 
]
activities_df = activities_df[cols]

pd.set_option('display.max_columns', None)
print(activities_df)

# Saving data to .csv file for future analysis.
activities_df.to_csv('ridewithgps_activity_data.csv') 