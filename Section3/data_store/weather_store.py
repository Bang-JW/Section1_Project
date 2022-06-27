# 절대 경로를 참조할 수 있도록함
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from data_preprocessing import weather_preprocessing
weather = weather_preprocessing.weather

weather['discomfort_index'] = 1.8*(weather['temperature'])-0.55*(1-weather['humidity']/100)*(1.8*weather['temperature'] - 26) + 32


import sqlite3

conn = sqlite3.connect('data/project.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE weather(
            date varchar(255),
            days varchar(255),
            temperature REAL,
            humidity REAL,
            precipitation REAL,
            discomfort REAL,
            PRIMARY KEY(date))""")

for i in range(len(weather)):
    cur.execute("""INSERT INTO weather(date, days, temperature, humidity, precipitation, discomfort) VALUES (?,?,?,?,?,?)""", 
                (weather['date'][i], weather['days'][i], weather['temperature'][i], weather['humidity'][i], weather['precipitation'][i], weather['discomfort_index'][i]))

conn.commit()
conn.close()
