# Ride with GPS All Activity Analysis

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting to display all columns in pandas dataframe.
pd.set_option('display.max_columns', None)

#Import strava .csv file.
rwgps_df = pd.read_csv('ridewithgps_activity_data.csv')

#Renaming columns with their correct units of measurement.
rwgps_df = rwgps_df.rename(columns = {'distance':'distance_km',
                                      'duration':'total_duration_sec',
                                      'elevation_gain':'total_elevation_gain_m',
                                      'avg_speed':'avg_speed_km/hr',
                                      'max_speed':'max_speed_km/hr',
                                      'moving_time':'moving_time_sec'})

# Remove time zone information from 'created_at' column.
rwgps_df['created_at'] = rwgps_df['created_at'].str[:-6]

# Convert 'created_at' column to datetime.
rwgps_df['created_at'] = pd.to_datetime(rwgps_df['created_at'], format='%Y-%m-%dT%H:%M:%S')

# Create new column with year, month, and day and then convert to datetime format.
rwgps_df['activity_date'] = rwgps_df['created_at'].dt.strftime('%Y-%m-%d')
rwgps_df['activity_date'] = pd.to_datetime(rwgps_df['activity_date'])

# Distance_km column is in kilometers. Adding column that's miles.
rwgps_df['distance_mi']=rwgps_df['distance_km'].apply(lambda x : x*0.000621371)

# Total duration column is in seconds. Adding column that's hours:minutes:seconds.
rwgps_df['datetime'] = pd.to_datetime(rwgps_df['total_duration_sec'], unit = 's')
rwgps_df['total_time_hr:min:sec'] = rwgps_df['datetime'].dt.strftime('%H:%M:%S')
del rwgps_df['datetime']

# Moving_time_sec column is in seconds. Adding column that's hours:minutes:seconds.
rwgps_df['datetime'] = pd.to_datetime(rwgps_df['moving_time_sec'], unit = 's')
rwgps_df['moving_time_hr:min:sec'] = rwgps_df['datetime'].dt.strftime('%H:%M:%S')
del rwgps_df['datetime']

# Elevation_gain_m is in meters. Adding column that's in ft.
rwgps_df['total_elevation_gain_ft'] = rwgps_df['total_elevation_gain_m'].apply(lambda x : x*3.28084)

# Avg_speed_km/hr is in km/hr. Adding column that's mph.
rwgps_df['avg_speed_mph'] = rwgps_df['avg_speed_km/hr'].apply(lambda x : x*0.621371)

# Max_speed_km/hr is in km/hr. Adding column that's mph.
rwgps_df['max_speed_mph'] = rwgps_df['max_speed_km/hr'].apply(lambda x : x*0.621371)

# Mapping each locality into broader location buckets.
location_mappings = {
    'Laguna Beach': 'Newport Beach',
    'Newport Beach': 'Newport Beach',
    'Newport Center': 'Newport Beach',
    'Orange County': 'Newport Beach',
    'Irvine': 'Newport Beach',
    'Tustin': 'Newport Beach',
    'Portland': 'Portland',
    'Live Oak': 'Santa Cruz',
    'Opal Cliffs/Pleasure Point': 'Santa Cruz',
    'Harrogate': 'Zwift',
    'Innsbruck': 'Zwift',
    'London': 'Zwift',
    'Murivai': 'Zwift',
    'Nea': 'Zwift',
    'noname': 'Zwift',
    'NYC': 'Zwift',
    'Thio': 'Zwift'
}

# Adding column with the broader location buckets.
rwgps_df['broad_location'] = rwgps_df['locality'].map(location_mappings).fillna('Zwift')

# Scatter plot - avg mph and activity date.
sns.set(style='ticks')
sns.scatterplot(x ='activity_date', 
                y = 'avg_speed_mph',
                data = rwgps_df).set_title("Average Speed by Activity Date")
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Average Speed (mph)')
plt.show()

# Scatter plot - avg mph and activity date filtered by before and after moving to Newport Beach.
sns.set(style='ticks')
sns.scatterplot(x ='activity_date', 
                y ='avg_speed_mph', 
                data = rwgps_df, 
                color='blue', 
                label='Newport Beach')

# Filter the dataframe based on the date condition.
before_date = pd.to_datetime('2022-05-20')
filtered_df = rwgps_df[rwgps_df['activity_date'] < before_date]

# Plot the points before the specified date in black.
sns.scatterplot(x = 'activity_date', 
                y = 'avg_speed_mph', 
                data = filtered_df, 
                color = 'black', 
                label = 'Before Newport Beach')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Average Speed (mph)')
plt.title('Average Speed Before and After Moving to Newport Beach')
plt.legend()
plt.show()

# Scatter plot -  avg mph and activity date filtered by broad location.
sns.set(style='ticks')
sns.scatterplot(x='activity_date',
                y = 'avg_speed_mph', 
                hue = 'broad_location',
                data = rwgps_df).set_title("Average Speed by Location")
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Average Speed (mph)')
plt.legend(title = 'Location')
plt.show()

# Creating data frames by broad_location
newportbeach_df = rwgps_df[rwgps_df['broad_location'] == 'Newport Beach']
portland_df = rwgps_df[rwgps_df['broad_location'] == 'Portland']
santacruz_df = rwgps_df[rwgps_df['broad_location'] == 'Santa Cruz']
zwift_df = rwgps_df[rwgps_df['broad_location'] == 'Zwift']

# Average speed and average elevation gain for each broad_location
avg_speed_newportbeach = newportbeach_df['avg_speed_mph'].mean()
avg_elegain_newportbeach = newportbeach_df['total_elevation_gain_ft'].mean()
avg_speed_portland = portland_df['avg_speed_mph'].mean()
avg_elegain_portland = portland_df['total_elevation_gain_ft'].mean()
avg_speed_zwift = zwift_df['avg_speed_mph'].mean()
avg_elegain_zwift = zwift_df['total_elevation_gain_ft'].mean()
avg_speed_santacruz = santacruz_df['avg_speed_mph'].mean()
avg_elegain_santacruz = santacruz_df['total_elevation_gain_ft'].mean()

# Data frame with avg speed and elevation gain for each broad location.
avg_metrics_location_table = pd.DataFrame({
    'Location': ['Newport Beach', 
                 'Portland', 
                 'Zwift', 
                 'Santa Cruz'],
    'Average Speed': [avg_speed_newportbeach, 
                      avg_speed_portland, 
                      avg_speed_zwift, 
                      avg_speed_santacruz],
    'Average Elevation Gain': [avg_elegain_newportbeach, 
                               avg_elegain_portland, 
                               avg_elegain_zwift, 
                               avg_elegain_santacruz],
})

print(avg_metrics_location_table)



