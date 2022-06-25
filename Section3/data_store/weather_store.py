# 절대 경로를 참조할 수 있도록함
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from data_preprocessing import weather_preprocessing
weather = weather_preprocessing.weather

import sqlite3

conn = sqlite3.connect('data/project.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE weather (
            days varchar(255),
            temperature REAL,
            humidity REAL,
            precipitation REAL,
            PRIMARY KEY(date))""")
for i in range(len(weather)):
    cur.execute("""INSERT INTO weather(date, temperature, humidity, precipitation) VALUES (?,?,?,?)""", 
                (weather['date'][i], weather['temperature'][i], weather['humidity'][i], weather['precipitation'][i]))

conn.commit()
conn.close()
