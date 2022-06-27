from flask import Flask, render_template, request
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pickle
from machine_learning import congestion_ml

#첫차
first_le_days = congestion_ml.first_le_days
first_le_name = congestion_ml.first_le_name
first_le_direction = congestion_ml.first_le_direction
#출근
working_le_days = congestion_ml.working_le_days
working_le_name = congestion_ml.working_le_name
working_le_direction = congestion_ml.working_le_direction
#일반
standard_le_days = congestion_ml.standard_le_days
standard_le_name = congestion_ml.standard_le_name
standard_le_direction = congestion_ml.standard_le_direction
#퇴근
home_le_days = congestion_ml.home_le_days
home_le_name = congestion_ml.home_le_name
home_le_direction = congestion_ml.home_le_direction
#막차
last_le_days = congestion_ml.last_le_days
last_le_name = congestion_ml.last_le_name
last_le_direction = congestion_ml.last_le_direction


app = Flask(__name__)
first_model = pickle.load(open("pickle/first.pkl", "rb"))
working_model = pickle.load(open("pickle/working.pkl", "rb"))
standard_model = pickle.load(open("pickle/standard.pkl", "rb"))
home_model = pickle.load(open("pickle/home.pkl", "rb"))
last_model = pickle.load(open("pickle/last.pkl", "rb"))

#첫 화면
@app.route("/")
def index_html():
    return render_template('index.html')

#첫차시간 
@app.route("/first")
def first_html():
    return render_template('first.html')

@app.route("/first/result", methods = ['POST'])
def first_result():
    data_list = []
    for data in request.form.values():
        data_list.append(data)    
    
    data_list[0] = first_le_days.transform([data_list[0]])
    data_list[1] = int(data_list[1])
    data_list[2] = int(data_list[2])
    data_list[3] = first_le_name.transform([data_list[3]])
    data_list[4] = first_le_direction.transform([data_list[4]])
    
    #온도
    data_list[5] = float(data_list[5])
    #습도
    data_list[6] = float(data_list[6])
    #강수량
    data_list[7] = float(data_list[7])
    result = first_model.predict([data_list[0:5]])
    weather_result = 1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32   

    return render_template('first.html', congestion = "This is congestion {}".format(result), subway_discomfort_index = weather_result + result)

# 출근시간
@app.route("/working")
def working_html():
    return render_template('working.html')

@app.route("/working/result", methods = ['POST'])
def working_result():
    data_list = []
    for data in request.form.values():
        data_list.append(data)    
    
    data_list[0] = working_le_days.transform([data_list[0]])
    data_list[1] = int(data_list[1])
    data_list[2] = int(data_list[2])
    data_list[3] = working_le_name.transform([data_list[3]])
    data_list[4] = working_le_direction.transform([data_list[4]])
    
    #온도
    data_list[5] = float(data_list[5])
    #습도
    data_list[6] = float(data_list[6])
    #강수량
    data_list[7] = float(data_list[7])


    result = working_model.predict([data_list[0:5]])
    weather_result = 1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32    

    return render_template('working.html', working_congestion = "This is congestion {}".format(result), working_subway_discomfort_index = weather_result + result)


#일반시간
@app.route("/standard")
def standard_html():
    return render_template('standard.html')

@app.route("/standard/result", methods = ['POST'])
def standard_result():
    data_list = []
    for data in request.form.values():
        data_list.append(data)    
    
    data_list[0] = standard_le_days.transform([data_list[0]])
    data_list[1] = int(data_list[1])
    data_list[2] = int(data_list[2])
    data_list[3] = standard_le_name.transform([data_list[3]])
    data_list[4] = standard_le_direction.transform([data_list[4]])
    
    #온도
    data_list[5] = float(data_list[5])
    #습도
    data_list[6] = float(data_list[6])
    #강수량
    data_list[7] = float(data_list[7])


    result = standard_model.predict([data_list[0:5]])
    weather_result = 1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32    

    return render_template('standard.html', standard_congestion = "This is congestion {}".format(result), standard_subway_discomfort_index = weather_result + result)


#퇴근시간
@app.route("/home")
def home_html():
    return render_template('home.html')

@app.route("/home/result", methods = ['POST'])
def home_result():
    data_list = []
    for data in request.form.values():
        data_list.append(data)    
    
    data_list[0] = home_le_days.transform([data_list[0]])
    data_list[1] = int(data_list[1])
    data_list[2] = int(data_list[2])
    data_list[3] = home_le_name.transform([data_list[3]])
    data_list[4] = home_le_direction.transform([data_list[4]])
    
    #온도
    data_list[5] = float(data_list[5])
    #습도
    data_list[6] = float(data_list[6])
    #강수량
    data_list[7] = float(data_list[7])


    result = home_model.predict([data_list[0:5]])
    weather_result = 1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32     

    return render_template('home.html', home_congestion = "This is congestion {}".format(result), home_subway_discomfort_index = weather_result + result)

#퇴근시간이후
@app.route("/last")
def last_html():
    return render_template('last.html')

@app.route("/last/result", methods = ['POST'])
def last_result():
    data_list = []
    for data in request.form.values():
        data_list.append(data)    
    
    data_list[0] = last_le_days.transform([data_list[0]])
    data_list[1] = int(data_list[1])
    data_list[2] = int(data_list[2])
    data_list[3] = last_le_name.transform([data_list[3]])
    data_list[4] = last_le_direction.transform([data_list[4]])
    
    #온도
    data_list[5] = float(data_list[5])
    #습도
    data_list[6] = float(data_list[6])
    #강수량
    data_list[7] = float(data_list[7])


    result = last_model.predict([data_list[0:5]])
    weather_result = 1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32  

    #subway_discomfort_index =  1.8*(data_list[5])-0.55*(1-data_list[6]/100)*(1.8*data_list[5] - 26) + 32 + model.predict([data_list[0:5]])

    return render_template('last.html', last_congestion = "This is congestion {}".format(result), last_subway_discomfort_index = weather_result + result)  

if __name__ == '__main__':
    app.run(port=5000, debug=True)