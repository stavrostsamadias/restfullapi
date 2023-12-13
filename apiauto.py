from flask import Flask,render_template_string
from flask_restful import Resource,Api
from datetime import datetime
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import base64


app=Flask(__name__)
api=Api(app)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%H:%M:%S")
formatted_date =current_datetime.strftime("%d-%m-%y")
temps=[]
temps1=[]
global text_date
text_date=""
global text_time
text_time=""
global text_Moisture
text_Moisture=0
global text_Temperature
text_Temperature=0
global text_CO2_Sensor
text_CO2_Sensor=0

webpage="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-C3 RESTFULL API FROM 2 SENSORS</title>
</head>
<body>
    <h1 style="text-align: center;">ESP32-C3 RESTFULL API FROM 2 SENSORS</h1>
    <br>
    <h2 style="text-align: center;">Instructions for POST REQUEST</h2>
    <br>
    <h3>POST REQUEST FOR THE 1FIRST SENSOR</h3>
    <p>The data is taken by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" and with the post method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/1/get/">https://stayrostsamadias.pythonanywhere.com/1/get/</a> string:temp1 string:temp2 string:temp3</p>
    <br>
    <h3>POST REQUEST FOR THE 2SECOND SENSOR</h3>
    <p>The data is taken by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" and with the post method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/2/get/">https://stayrostsamadias.pythonanywhere.com/2/get/</a> string:temp1 string:temp2 string:temp3</p>
        
    <h2 style="text-align: center;">Instructions for DELETE REQUEST</h2>
    <br>
    <h3>POST REQUEST FOR THE 1FIRST SENSOR</h3>
    <p>If the data is not right and taken by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" use the DELETE method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/1/get/">https://stayrostsamadias.pythonanywhere.com/1/get/</a> string:temp1 string:temp2 string:temp3</p>
    <br>
    <h3>POST REQUEST FOR THE 2SECOND SENSOR</h3>
    <p>If the data is not right and taken by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" use the DELETE method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/2/get/">https://stayrostsamadias.pythonanywhere.com/2/get/</a> string:temp1 string:temp2 string:temp3</p>
    <br>
    <h2 style="text-align: center;">Instructions for GET REQUEST</h2>
    <br>
    <h3>GET REQUEST FOR THE 1FIRST SENSOR</h3>
    <p>If you need the data to taken from by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" use the GET method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/1/data/">https://stayrostsamadias.pythonanywhere.com/1/data/</a> string:temp1 string:temp2 string:temp3</p>
    <br>
    <h3>GET REQUEST FOR THE 2SECOND SENSOR</h3>
    <p>If you need the data to taken from by ESP32-C3 from the sensors "Moisture, Temperature, CO2_Sensor" use the GET method it's requests the data on the page <a href="https://stayrostsamadias.pythonanywhere.com/2/data/">https://stayrostsamadias.pythonanywhere.com/2/data/</a> string:temp1 string:temp2 string:temp3</p>
    <br>
    <h2 style="text-align: center;">GET ALL THE DATA</h2>
    <p>If you wand to see all the data from the 2 sensors you need to go <a href="https://stayrostsamadias.pythonanywhere.com/data/">https://stayrostsamadias.pythonanywhere.com/data/</a></p>
    <br>
    <h3 style="text-align: center;">Data Examples in Json</h3>
    <p>#values ​​1 1 1 1 present JSON {"Data_temps1": [{"Moisture": "1", "Temperature": "1", "CO2_Sensor": "1"}]}.</p>
    <br>
    <h2 style="text-align: center;">FOR THE GRAPHS OF SENSORS 1 AND 2</h2>
    <p>If you wand to see the data GRAPHS from the 1 sensor you need to go <a href="https://stayrostsamadias.pythonanywhere.com/grafics/1/">https://stayrostsamadias.pythonanywhere.com/grafics/1/</a></p>
    <p>If you wand to see the data GRAPHS from the 2 sensor you need to go <a href="https://stayrostsamadias.pythonanywhere.com/grafics/2/">https://stayrostsamadias.pythonanywhere.com/grafics/2/</a></p>
    <br>
    <h3 style="text-align: end;">Copyright Stavros Tsamadias for D.I.E.K Mesologhiou 2023</h3>
    <br>
</body>
</html>"""
#global img_base64
#img_base64=0


webpage2 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Plotly</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Sensor Data Chart</h1>
    <div id="myChart"></div>
    <script>
        var chartData = {{ chart_data | tojson|safe }};
        var dates = chartData.labels;
        var moistureData = chartData.datasets[0].data;
        var temperatureData = chartData.datasets[1].data;
        var co2Data = chartData.datasets[2].data;

        var traceMoisture = {
            x: dates,
            y: moistureData,
            type: 'scatter',
            mode: 'lines',
            name: 'Moisture'
        };

        var traceTemperature = {
            x: dates,
            y: temperatureData,
            type: 'scatter',
            mode: 'lines',
            name: 'Temperature'
        };

        var traceCO2 = {
            x: dates,
            y: co2Data,
            type: 'scatter',
            mode: 'lines',
            name: 'CO2'
        };

        var layout = {
            title: 'Sensor Data',
            xaxis: {
                title: 'Date and Time'
            },
            yaxis: {
                title: 'Value'
            }
        };

        Plotly.newPlot('myChart', [traceMoisture, traceTemperature, traceCO2], layout);
        
        
        function updateCharts() {
            // Κάνε αίτηση AJAX για τα δεδομένα των δύο σελίδων
            fetch('http://127.0.0.1:5000/grafics/2')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('chart1').innerHTML = data;
                });

          setTimeout(updateCharts, 5000);
        }
        // Καλεί τη συνάρτηση για πρώτη φορά
        updateCharts();
    </script>
    
</body>
</html>
"""

webpage1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Plotly</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Sensor Data Chart</h1>
    <div id="myChart"></div>
    <script>
        var chartData = {{ chart_data | tojson|safe }};
        var dates = chartData.labels;
        var moistureData = chartData.datasets[0].data;
        var temperatureData = chartData.datasets[1].data;
        var co2Data = chartData.datasets[2].data;

        var traceMoisture = {
            x: dates,
            y: moistureData,
            type: 'scatter',
            mode: 'lines',
            name: 'Moisture'
        };

        var traceTemperature = {
            x: dates,
            y: temperatureData,
            type: 'scatter',
            mode: 'lines',
            name: 'Temperature'
        };

        var traceCO2 = {
            x: dates,
            y: co2Data,
            type: 'scatter',
            mode: 'lines',
            name: 'CO2'
        };

        var layout = {
            title: 'Sensor Data',
            xaxis: {
                title: 'Date and Time'
            },
            yaxis: {
                title: 'Value'
            }
        };

        Plotly.newPlot('myChart', [traceMoisture, traceTemperature, traceCO2], layout);
        function updateCharts() {
            // Κάνε αίτηση AJAX για τα δεδομένα των δύο σελίδων
            fetch('http://127.0.0.1:5000/grafics/1')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('chart1').innerHTML = data;
                });

          setTimeout(updateCharts, 5000);
        }

        // Καλεί τη συνάρτηση για πρώτη φορά
        updateCharts();
    </script>
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return webpage

@app.route('/grafics/2')
def index2():
    response = requests.get(url="http://127.0.0.1:5000/2/data")
    data_text = response.json()['Temps']
    if response.status_code != 200:
        return "Unauthorized", 401

    data_text = response.json().get('Temps', [])

    if not data_text:
        return "No data found", 401

    chart_data = {
        'labels': [],
        'datasets': [
            {
                'label': 'Moisture',
                'data': []
            },
            {
                'label': 'Temperature',
                'data': []
            },
            {
                'label': 'CO2',
                'data': []
            }
        ]
    }

    for i in range(len(data_text)):
        text_date = data_text[i]['date']
        text_time = data_text[i]['time']
        text_Moisture = int(data_text[i]['Moisture'])
        text_Temperature = int(data_text[i]['Temperature'])
        text_CO2_Sensor = int(data_text[i]['CO2_Sensor'])

        chart_data['labels'].append(f"{text_date} {text_time}")
        chart_data['datasets'][0]['data'].append(text_Moisture)
        chart_data['datasets'][1]['data'].append(text_Temperature)
        chart_data['datasets'][2]['data'].append(text_CO2_Sensor)
    return render_template_string(webpage2, chart_data=chart_data)


@app.route('/grafics/1')
def index1():
    response = requests.get(url="http://127.0.0.1:5000/1/data")
    data_text = response.json()['Temps']
    if response.status_code != 200:
        return "Unauthorized", 401

    data_text = response.json().get('Temps', [])

    if not data_text:
        return "No data found", 401

    chart_data = {
        'labels': [],
        'datasets': [
            {
                'label': 'Moisture',
                'data': []
            },
            {
                'label': 'Temperature',
                'data': []
            },
            {
                'label': 'CO2',
                'data': []
            }
        ]
    }

    for i in range(len(data_text)):
        text_date = data_text[i]['date']
        text_time = data_text[i]['time']
        text_Moisture = int(data_text[i]['Moisture'])
        text_Temperature = int(data_text[i]['Temperature'])
        text_CO2_Sensor = int(data_text[i]['CO2_Sensor'])

        chart_data['labels'].append(f"{text_date} {text_time}")
        chart_data['datasets'][0]['data'].append(text_Moisture)
        chart_data['datasets'][1]['data'].append(text_Temperature)
        chart_data['datasets'][2]['data'].append(text_CO2_Sensor)
    return render_template_string(webpage1, chart_data=chart_data)



class webpageapi1(Resource):

    def get(self,temp1,temp2,temp3):

        for tem in temps:
            if tem['Moisture'] and tem["Temperature"] and tem["CO2_Sensor"] == temp1 and temp2 and temp3 :
                return tem
        return {"Moisture": None, "Temperature":None, "CO2_Sensor": None}

        pass

    def post(self,temp1,temp2,temp3):

        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime("%H:%M:%S")
        formatted_date =current_datetime.strftime("%d-%m-%y")
        temperatures={"date":formatted_date,"time":formatted_time,"Moisture": temp1, "Temperature":temp2, "CO2_Sensor": temp3}
        temps.append(temperatures)
        return temperatures

    def delete(self,temp1,temp2,temp3):

        for ind,tem in enumerate(temps):
            if tem['Moisture'] and tem["Temperature"] and tem["CO2_Sensor"] == temp1 and temp2 and temp3 :
                delete_temp=temps1.pop(ind)
                return {'note':"delete success"}
        return {'note':"not success"}


class AllTemps1(Resource):
    def get(self):
        return {'Temps':temps}

class webpageapi2(Resource):

    def get(self,temp1,temp2,temp3):

        for tem in temps1:
            if tem['Moisture'] and tem["Temperature"] and tem["CO2_Sensor"] == temp1 and temp2 and temp3 :
                return tem
        return {"Moisture": None, "Temperature":None, "CO2_Sensor": None}

        pass

    def post(self,temp1,temp2,temp3):

        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime("%H:%M:%S")
        formatted_date =current_datetime.strftime("%d-%m-%y")

        temperatures={"date":formatted_date,"time":formatted_time,"Moisture": temp1, "Temperature":temp2, "CO2_Sensor": temp3}
        temps1.append(temperatures)
        return temperatures

    def delete(self,temp1,temp2,temp3):

        for ind,tem in enumerate(temps1):
            if tem['Moisture'] and tem["Temperature"] and tem["CO2_Sensor"] == temp1 and temp2 and temp3 :
                delete_temp=temps.pop(ind)
                return {'note':"delete success"}
        return {'note':"not success"}


class AllTemps2(Resource):
    def get(self):
        return {'Temps':temps1}

class AllTemps(Resource):
    def get(self):
        return {'sensors1':temps,'sensors2':temps1}


api.add_resource(webpageapi1,'/1/get/<string:temp1> <string:temp2> <string:temp3>')
api.add_resource(AllTemps1,'/1/data')

api.add_resource(webpageapi2,'/2/get/<string:temp1> <string:temp2> <string:temp3>')
api.add_resource(AllTemps2,'/2/data')

api.add_resource(AllTemps,'/data')

#api.add_resource(fisrtpage,'/')


if __name__=="__main__":
    app.run(debug=True)


