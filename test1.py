import requests
data=['1 1 1 1']
data1=['Anemometer:3%0Moistrure:3%0Temperature:3%0CO2_Sensor:3']

for i in data:
    responce=requests.post("http://127.0.0.1:5000/temp/"+i,params="json")

print(responce.text)

responce1=requests.get("http://127.0.0.1:5000/temp/data",params="json")
print(responce1.json())

a=responce1.json()

data_names=[]



for i in a:
    for x in range(len(a[i])):
        #print(a[i][x]['name'])
       data_names.append([a[i][x]['Anemometer'],a[i][x]['Moisture'],a[i][x]['Temperature'],a[i][x]['CO2_Sensor']])

print(len(data_names))
