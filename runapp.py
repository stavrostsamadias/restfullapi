from flask import Flask
from flask_restful import Resource,Api

app=Flask(__name__)
api=Api(app)


temps=[]

class tempouter(Resource):

    def get(self,Anemometer,Moisture,Temperature,CO2_Sensor):
        for i in temps:
            if i['Anemometer']== Anemometer and i['Moisture']== Moisture and i['Temperature']== Temperature and i['CO2_Sensor']==CO2_Sensor:
                return temps

        return {'Anemometer':None,"Moisture":None,"Temperature":None,"CO2_Sensor":None}


    def post(self,Anemometer,Moisture,Temperature,CO2_Sensor):
        data_temp={'Anemometer':Anemometer,"Moisture":Moisture,"Temperature":Temperature,"CO2_Sensor":CO2_Sensor}
        temps.append(data_temp)
        return data_temp


    def delete(self,Anemometer,Moisture,Temperature,CO2_Sensor):

      for ind,data_temp in enumerate(temps):
          if data_temp['Anemometer']== Anemometer and data_temp['Moisture']== Moisture and data_temp['Temperature']== Temperature and data_temp['CO2_Sensor']==CO2_Sensor:
                delete_temp=temps.pop(ind)
                print (delete_temp)
                return {'note':'delete success'}


class AllNames(Resource):
    def get(self):
        return {'Data_temps':temps}




api.add_resource(tempouter,"/temp/<string:Anemometer> <string:Moisture> <string:Temperature> <string:CO2_Sensor>")
api.add_resource(AllNames,"/temp/data")


if __name__=='__main__':
    app.run(debug=True)
