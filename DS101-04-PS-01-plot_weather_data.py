import pandas as pd
import numpy as np
from datetime import datetime
from ggplot import *
import pandasql

pd.options.mode.chained_assignment = None

def get_day_number(date):
    return datetime.strftime(datetime.strptime(date, '%Y-%m-%d').date(), '%d')


def plot_weather_data(weather_data):
    """
    You are passed in a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.
    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
 ->  * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    To see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    """

    weather_data['daynumber'] = weather_data['DATEn'].apply(lambda d: get_day_number(d))
    weather_data.rename(columns=lambda x: x.replace(' ', '_').lower(), inplace=True)

    q = '''
        select daynumber, sum(ENTRIESn_hourly) as entries
        from weather_data
        group by daynumber
    '''

    # Execute your SQL command against the pandas frame
    result = pandasql.sqldf(q.lower(), locals())

    plot = ggplot(result, aes(x='daynumber')) + \
           geom_bar(aes(weight='entries'), fill='green') + \
           ggtitle('Total number of entries per day') + xlab('Day number') + ylab('Entries')

    return plot


df = pd.read_csv(r"Data\turnstile_data_master_with_weather.csv")
print plot_weather_data(df)