import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import date
import seaborn as sns
import mplcursors

# Request API, clean the data, make a graph.
def segment(segment_id, segment_title):
    
    # Authentication URL 
    auth_url = "https://www.strava.com/oauth/token"

    # URL used to access all the data.
    activites_url = "https://www.strava.com/api/v3/segment_efforts"

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
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'segment_id': segment_id, 'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    data_df = json_normalize(my_dataset)

    # Only keeping columns I actually need for my analysis.
    cols = ['activity.id', 'athlete.id', 'name', 'start_date', 'elapsed_time', 'moving_time', 
            'average_cadence', 'average_watts', 'distance', 'segment.average_grade', 
            'segment.maximum_grade']
            
    data_df = data_df[cols]

    # Setting to display all columns.
    pd.set_option('display.max_columns', None)

    # Renaming columns.
    data_df = data_df.rename(columns = {'activity.id':'activity_id',
                                        'athlete.id':'athlete_id',
                                        'name':'segment_name',
                                        'elapsed_time':'elapsed_time_sec',
                                        'moving_time':'moving_time_sec',
                                        'average_cadence':'avg_cadence',
                                        'average_watts':'avg_watts',
                                        'distance':'distance_m',
                                        'segment.average_grade':'avg_gradient',
                                        'segment.maximum_grade':'max_gradient'
                                        })


    # Remove time and time zone information from 'start_date' column then converting into datetime format.
    data_df['start_date'] = data_df['start_date'].str[:-10]
    data_df['start_date'] = pd.to_datetime(data_df['start_date'], format='%Y-%m-%d')

    # Elapsed_time_sec column is in seconds. Adding column that's minutes:seconds.
    data_df['datetime'] = pd.to_datetime(data_df['elapsed_time_sec'], unit = 's')
    data_df['elapsed_time'] = data_df['datetime'].dt.strftime('%M:%S')
    del data_df['datetime']

    # Moving_time_sec column is in seconds. Adding column that's minutes:seconds.
    data_df['datetime'] = pd.to_datetime(data_df['moving_time_sec'], unit = 's')
    data_df['moving_time'] = data_df['datetime'].dt.strftime('%M:%S')
    del data_df['datetime']

    # Distance_m column is in meters. Adding column that's in miles.
    data_df['distance_mi']=data_df['distance_m'].apply(lambda x : x*0.000621371)

    # Converting the start date to an ordinal date for a regplot graph.
    data_df['date_ordinal'] = pd.to_datetime(data_df['start_date']).apply(lambda date: date.toordinal())

    # Sort the dataframe by 'moving_time_sec' column and get the three lowest values.
    fastest_three_times = data_df.nsmallest(3, 'moving_time_sec')

    # # Find the fastest time.
    fastest_time = data_df['moving_time_sec'].min()

    # # Find the date with the fastest time.
    fastest_date_ordinal = fastest_three_times.loc[fastest_three_times['moving_time_sec'] == fastest_time, 'date_ordinal'].values[0]
    fastest_date = date.fromordinal(int(fastest_date_ordinal))

    def format_minutes_seconds(x, _):
        minutes = int(x // 60)
        seconds = int(x % 60)
        return f"{minutes:02d}:{seconds:02d}"

    # Scatter plot w/ trend line - moving time and date.
    ax = sns.regplot(
        data=data_df,
        x='date_ordinal',
        y='moving_time_sec')
    ax.set_xlabel('Date')
    ax.set_ylabel('Time')
    plt.xticks(rotation=45)
    ax.set_title(segment_title)

    # Formatting y-axis label.
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_minutes_seconds))

    #Formatting x-axis label.
    new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
    formatted_labels = [date.strftime('%m-%Y') for date in new_labels]
    ax.set_xticklabels(formatted_labels)

    # Highlight the fastest time on the graph.
    ax.scatter(fastest_date_ordinal, fastest_time, color='red')
    ax.scatter([], [], color='red', label=f'Fastest Time: {format_minutes_seconds(fastest_time, None)}\nDate: {fastest_date.strftime("%m/%d/%Y")}')
            
    # Adding hover functionality
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"Date: {date.fromordinal(int(sel.target[0])).strftime('%m/%d/%Y')}\nTime: {format_minutes_seconds(sel.target[1], None)}"
    ))

    plt.legend()
    plt.show()

    # # In case I ever want to export the data.
    # filename = f"{segment_title}.csv"
    # data_df.to_csv(filename) 

segment(1566359, "Back Bay - Bridge to Vista Point\n1.87mi - 60ft - 0.5%")
segment(926220, "Backside Newport Coast from Turtle Ridge\n1.33mi - 339ft - 4.6%")
segment(660060, "Culver Big Ring\n.92mi - 153ft - 3.0%")
segment(913750, "Newport Coast Road\n2.15mi - 514ft - 4.3%")
segment(686890, "Ridge Park Road\n.83mi - 538ft - 9.1%")
segment(2813, "San Joaquin Road\n1.20mi - 303ft - 4.8%")


