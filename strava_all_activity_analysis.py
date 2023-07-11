# Strava All Activity Analysis

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting to display all columns.
pd.set_option('display.max_columns', None)

#Import strava csv file.
strava_activities_df = pd.read_csv('strava_activities_data.csv')

#Renaming columns with their units of measurement.
strava_activities_df = strava_activities_df.rename(columns = {'distance':'distance_m',
                                                              'moving_time':'moving_time_sec',
                                                              'elapsed_time':'elapsed_time_sec',
                                                              'total_elevation_gain':'total_elevation_gain_m',
                                                              'average_speed':'average_speed_m/sec',
                                                              'max_speed':'max_speed_m/sec'})

# Change start_date_local to datetime format. Then making new column with only month-day-year.
strava_activities_df['start_date_local'] = pd.to_datetime(strava_activities_df['start_date_local'])
strava_activities_df['activity_date'] = strava_activities_df['start_date_local'].dt.strftime('%Y-%m-%d')
strava_activities_df['activity_date'] = pd.to_datetime(strava_activities_df['activity_date'])

# Distance column is in meters. Adding column that's miles.
strava_activities_df['distance_mi']=strava_activities_df['distance_m'].apply(lambda x : x*0.000621371)

# Moving time column is in seconds. Adding column that's hours:minutes:seconds
strava_activities_df['datetime'] = pd.to_datetime(strava_activities_df['moving_time_sec'], unit = 's')
strava_activities_df['moving_time_hr:min:sec'] = strava_activities_df['datetime'].dt.strftime('%H:%M:%S')
del strava_activities_df['datetime']

# Elapsed time is in seconds. Adding column that's hours:minutes:seconds
strava_activities_df['datetime'] = pd.to_datetime(strava_activities_df['elapsed_time_sec'], unit = 's')
strava_activities_df['elapsed_time_hr:min:sec'] = strava_activities_df['datetime'].dt.strftime('%H:%M:%S')
del strava_activities_df['datetime']

# Total elevation gain is in meters. Adding column that's in ft.
strava_activities_df['total_elevation_gain_ft'] = strava_activities_df['total_elevation_gain_m'].apply(lambda x : x*3.28084)

# Average speed is in m/sec. Adding column that's mph.
strava_activities_df['average_speed_mph'] = strava_activities_df['average_speed_m/sec'].apply(lambda x : x*2.236936)

# Max speed is in m/sec. Adding column that's mph.
strava_activities_df['max_speed_mph'] = strava_activities_df['max_speed_m/sec'].apply(lambda x : x*2.236936)

# Scatter plot - avg mph and activity date
sns.set(style='ticks')
sns.scatterplot(x='activity_date', 
                y = 'average_speed_mph',
                data = strava_activities_df).set_title("Average Speed by Activity Date")
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Average Speed (mph)')
plt.show()

# Scatter plot - avg mph and activity date filtered by before and after moving to Newport Beach.
sns.set(style='ticks')
sns.scatterplot(x='activity_date', 
                y='average_speed_mph', 
                data=strava_activities_df, 
                color='blue', 
                label='Newport Beach')

# Filter the dataframe based on the date condition.
before_date = pd.to_datetime('2022-05-20')
filtered_df = strava_activities_df[strava_activities_df['activity_date'] < before_date]

# Plot the points before the specified date in black.
sns.scatterplot(x='activity_date', 
                y='average_speed_mph', 
                data=filtered_df,
                color='black', 
                label='Before Newport Beach')

plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Average Speed (mph)')
plt.title('Average Speed Before and After Moving to Newport Beach')
plt.legend()
plt.show()

# Scatter plot - avg mph and distance.
sns.set(style='ticks')
sns.scatterplot(x='distance_mi', 
                y = 'average_speed_mph',
                data = strava_activities_df).set_title("Average Speed by Distance")
plt.xticks(rotation=45)
plt.xlabel('Distance (miles)')
plt.ylabel('Average Speed (mph)')
plt.show()


