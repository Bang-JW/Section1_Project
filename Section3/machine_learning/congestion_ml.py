import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from data_preprocessing import subway_preprocessing, weather_preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import numpy as np
import pickle

# 데이터 merge
weather = weather_preprocessing.weather
congestion_first = subway_preprocessing.congestion_first
congestion_working = subway_preprocessing.congestion_working
congestion_standard = subway_preprocessing.congestion_standard
congestion_home = subway_preprocessing.congestion_home
congestion_last = subway_preprocessing.congestion_last

first = pd.merge(left = congestion_first, right = weather, how='inner', on = 'days')
working = pd.merge(left = congestion_working, right = weather, how='inner', on = 'days')
standard = pd.merge(left = congestion_standard, right = weather, how='inner', on = 'days')
home = pd.merge(left = congestion_home, right = weather, how='inner', on = 'days')
last = pd.merge(left = congestion_last, right = weather, how='inner', on = 'days')


#불쾌지수 계산
data_list = [first, working, standard, home, last]

for data in data_list:
    data['discomfort_index'] = 1.8*(data['temperature'])-0.55*(1-data['humidity']/100)*(1.8*data['temperature'] - 26) + 32
    data['subway_discomfort'] = data['discomfort_index'] + data.iloc[:,5]

#model 만드는 함수 

def make_ml_model(data):

    data['date'] = pd.to_datetime(data['date'])

    train = data[data['date']<='2021-06-30']
    train.set_index('date', inplace=True)

    val = data[data['date']>='2021-07-01']
    val.set_index('date', inplace=True)

    X_train = train.iloc[:,0:5]
    y_train = train.iloc[:,5]

    X_val = val.iloc[:,0:5]
    y_val = val.iloc[:,5]

    le_days = LabelEncoder()
    le_name = LabelEncoder()
    le_direction = LabelEncoder()

    X_train['days'] = le_days.fit_transform(X_train['days'])
    X_train['station_name'] = le_name.fit_transform(X_train['station_name'])
    X_train['train_direction'] = le_direction.fit_transform(X_train['train_direction'])

    X_val['days'] = le_days.transform(X_val['days'])
    X_val['station_name'] = le_name.transform(X_val['station_name'])
    X_val['train_direction'] = le_direction.transform(X_val['train_direction'])

    dt = DecisionTreeRegressor()
    model = dt.fit(X_train, y_train)

    return model, le_days, le_name, le_direction

#첫차시간대 model
first_model, first_le_days, first_le_name, first_le_direction= make_ml_model(first)

#출근시간대 model
working_model, working_le_days, working_le_name, working_le_direction = make_ml_model(working)

#일반시간대 model
standard_model, standard_le_days, standard_le_name, standard_le_direction = make_ml_model(standard)

#퇴근시간대 model
home_model, home_le_days, home_le_name, home_le_direction = make_ml_model(home)

#막차시간대 model
last_model, last_le_days, last_le_name, last_le_direction = make_ml_model(last)

with open('pickle/first.pkl', 'wb') as fw:
    pickle.dump(first_model, fw)

with open('pickle/working.pkl', 'wb') as fw:
    pickle.dump(working_model, fw)

with open('pickle/standard.pkl', 'wb') as fw:
    pickle.dump(standard_model, fw)

with open('pickle/home.pkl', 'wb') as fw:
    pickle.dump(home_model, fw)

with open('pickle/last.pkl', 'wb') as fw:
    pickle.dump(last_model, fw)