import os
import pandas as pd
import datetime

WEATHER_DATA_PATH = os.path.join("./data/weather/")
HUMIDITY_PATH = "humidity.csv"
RAIN_PATH = "rain.csv"
TEMPERATURE_PATH = "temperature.csv"


#humidity = pd.read_csv(WEATHER_DATA_PATH + "humidity.csv", encoding='cp949')

# 
def preprocessing(file_name, first_column_name, second_column_name):
    data = pd.read_csv(WEATHER_DATA_PATH + file_name, encoding='cp949')
    data = data[[data.columns[2], data.columns[3]]]

    if file_name == RAIN_PATH:

        data[data.columns[1]] = data[data.columns[1]].fillna(0)
        data = data.dropna()
        data = data.rename(columns = {data.columns[0] : first_column_name, data.columns[1] : second_column_name})

    else:

        data = data.dropna()
        data = data.rename(columns = {data.columns[0] : first_column_name, data.columns[1] : second_column_name})

    return data

humidity = preprocessing(HUMIDITY_PATH, 'date', 'humidity')
rain = preprocessing(RAIN_PATH, 'date', 'precipitation')
temperature = preprocessing(TEMPERATURE_PATH, 'date', 'temp')

# data를 한개로 합침
weather = pd.DataFrame()
weather['date'] = humidity['date']
weather['temperature'] = temperature['temp']
weather['humidity'] = humidity['humidity']
weather['precipitation'] = rain['precipitation']

def get_days(data):
    
    data['days'] = '평일'
    
    
    
    for i in range(len(data)):
        date = data['date'][i].split('-')
        date = list(map(int, date))
        
        days = datetime.date(date[0], date[1], date[2]).weekday()  
    
        if days >= 0  | days <=4:
            data['days'][i] = '평일'
        
        elif days == 5:
            data['days'][i] = '토요일'
    
        elif days == 6:
            data['days'][i] = '일요일'

get_days(weather)



