import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#DATA LOAD
SUBWAY_DATA_PATH = os.path.join("./data/subway/")
YEARS_1617_PATH = os.path.join(SUBWAY_DATA_PATH, "subway_congestion_2016_2017.csv")
YEARS_1819_PATH = os.path.join(SUBWAY_DATA_PATH, "subway_congestion_2018_2019.csv")
YEARS_2021_PATH = os.path.join(SUBWAY_DATA_PATH, "subway_congestion_2020_2021.csv")

congestion_1617 = pd.read_csv(YEARS_1617_PATH, encoding='cp949')
congestion_1819 = pd.read_csv(YEARS_1819_PATH, encoding='cp949')
congestion_2021 = pd.read_csv(YEARS_2021_PATH, encoding='cp949')

# 2021data 연번 drop, 2400, 2430 데이터 0으로 채워줌(코로나 시국이라 데이터가 없음)
congestion_2021 = congestion_2021.drop(['연번'], axis = 1)
congestion_2021['24시00분'] = 0
congestion_2021['24시30분'] = 0

# column의 이름 통일
columns_standard = ['days', 'lines_num', 'station_num', 'station_name', 'train_direction']
for i in range(len(congestion_1819.columns[5:])):
    columns_standard.append(congestion_1819.columns[5:][i])

congestion_1617.columns = columns_standard
congestion_1819.columns = columns_standard
congestion_2021.columns = columns_standard

# 결측치는 경우에는 0으로 채움
congestion_1617.fillna(0, inplace =True)
congestion_1819.fillna(0, inplace =True)
congestion_2021.fillna(0, inplace =True)

# 2호선에 지선과 관련된 데이터는 drop
def one_to_eight(data):
    condition = data[data['lines_num'].str.contains('지선')].index
    data.drop(condition, inplace=True)
    data = data.reset_index(drop=True)

    return data

congestion_1617 = one_to_eight(congestion_1617)
congestion_1819 = one_to_eight(congestion_1819)

# 1819는 '1호선'으로 표현되어 있어 숫자추출
for i in range(len(congestion_1819['lines_num'])):
    congestion_1819['lines_num'][i] = congestion_1819['lines_num'][i].split('호선')[0]

# 2020~2021년 데이터는 이미 int형
def lines_num_toint(data):
    """호선 column을 int형으로"""
    data['lines_num'] = data['lines_num'].astype('int64')

    return data

congestion_1617 = lines_num_toint(congestion_1617)
congestion_1819 = lines_num_toint(congestion_1819)

#0호선 데이터만 추출하는 함수
def which_line_num_data(data, lines_num):
    """어떤 호선의 데이터를 추출할 것인지 만드는 함수"""
    data = data[data['lines_num'] == lines_num]
    data = data.reset_index(drop=True)

    return data

#2호선만 추출
congestion_1617 = which_line_num_data(congestion_1617, 2)
congestion_1819 = which_line_num_data(congestion_1819, 2)
congestion_2021 = which_line_num_data(congestion_2021, 2)

# 데이터를 합침
concat_data = pd.concat([congestion_1617, congestion_1819, congestion_2021])

# 먼저 첫차, 출근, 일반, 퇴근, 퇴근이후 시간대의 혼잡도를 계산

#[5:8] 첫차 시간 05:30~06:30
#[8:14] 출근 시간 07:00~09:30
#[15:29] 일반 시간 10:00~17:00
# [29:35] 퇴근시간 17:30~20:00
# [35:44] 퇴근 이후시간 20:30~24:30

# 혼잡도 계산 함수
def congestion(data, column_name, range_start, range_end):    
    data.iloc[:,range_start:range_end] = data.iloc[:,range_start:range_end].astype('float64')
    sum_value = 0
    mean = 0
    
    for i in range(range_start, range_end):
        sum_value+= data.iloc[:,i]   
        
    mean = sum_value/(range_end-range_start)
    

    new_data = data.iloc[:, 0:5]
    new_data[column_name] = mean
    new_data.reset_index(drop=True, inplace=True)

    return new_data

congestion_first = congestion(concat_data, 'first_congestion', 5, 8)
congestion_working = congestion(concat_data, 'working_congestion', 8, 14)
congestion_standard = congestion(concat_data, 'standard_congestion', 15, 29)
congestion_home = congestion(concat_data, 'home_congestion', 29, 35)
congestion_last = congestion(concat_data, 'last_congestion', 35, 44)


