import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from data_preprocessing import subway_preprocessing

congestion_first = subway_preprocessing.congestion_first
congestion_working = subway_preprocessing.congestion_working
congestion_standard = subway_preprocessing.congestion_standard
congestion_home = subway_preprocessing.congestion_home
congestion_last = subway_preprocessing.congestion_last

import sqlite3

conn = sqlite3.connect('data/project.db')
cur = conn.cursor()

# 첫차시간 혼잡도 table
cur.execute("""CREATE TABLE IF NOT EXISTS congestion_first (
            days varchar(255),
            station_name varchar(255),
            train_direction varchar(255),
            first_congestion REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS congestion_working (
            days varchar(255),
            station_name varchar(255),
            train_direction varchar(255),
            working_congestion REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS congestion_standard (
            days varchar(255),
            station_name varchar(255),
            train_direction varchar(255),
            standard_congestion REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS congestion_home (
            days varchar(255),
            station_name varchar(255),
            train_direction varchar(255),
            home_congestion REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS congestion_last (
            days varchar(255),
            station_name varchar(255),
            train_direction varchar(255),
            last_congestion REAL)""")

for i in range(len(congestion_first)):
    cur.execute("""INSERT INTO congestion_first(days, station_name, train_direction, first_congestion) VALUES (?,?,?,?)""", 
                [congestion_first['days'][i],congestion_first['station_name'][i],congestion_first['train_direction'][i],congestion_first['first_congestion'][i]])

for i in range(len(congestion_working)):
    cur.execute("""INSERT INTO congestion_working(days, station_name, train_direction, working_congestion) VALUES (?,?,?,?)""", 
                [congestion_working['days'][i],congestion_working['station_name'][i],congestion_working['train_direction'][i],congestion_working['working_congestion'][i]])

for i in range(len(congestion_standard)):
    cur.execute("""INSERT INTO congestion_standard(days, station_name, train_direction, standard_congestion) VALUES (?,?,?,?)""", 
                [congestion_standard['days'][i],congestion_standard['station_name'][i],congestion_standard['train_direction'][i],congestion_standard['standard_congestion'][i]])

for i in range(len(congestion_home)):
    cur.execute("""INSERT INTO congestion_home(days, station_name, train_direction, home_congestion) VALUES (?,?,?,?)""", 
                [congestion_home['days'][i],congestion_home['station_name'][i],congestion_home['train_direction'][i],congestion_home['home_congestion'][i]])

for i in range(len(congestion_last)):
    cur.execute("""INSERT INTO congestion_last(days, station_name, train_direction, last_congestion) VALUES (?,?,?,?)""", 
                [congestion_last['days'][i],congestion_last['station_name'][i],congestion_last['train_direction'][i],congestion_last['last_congestion'][i]])

conn.commit()
conn.close()

