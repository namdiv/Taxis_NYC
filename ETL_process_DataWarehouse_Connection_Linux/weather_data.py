#cada tupla tiede: latitud, longitud, elevacion, nombre del borough
bronx = [40.8499, -73.8664, 19, "The Bronx"]
brooklyn = [40.6501, -73.9496, 18, 'Brooklyn']
manhattan = [40.7834, -73.9663, 38, 'Manhattan']
queens = [40.6815, -73.8365, 13, 'Queens']
staten_island = [40.5623, -74.1399, 23, 'Staten Island']

#generamos una lista  con las tuplas
lista = [bronx, brooklyn, manhattan, queens,staten_island]

#importamos las librerias 
from datetime import datetime
#PIP INSTALL METEOSTAT
from meteostat import Point, Daily, Hourly
import pandas as pd

#descarga de la informacion 
#descargamos la info de todos los boroughs en un mismo dataframe

df_weather_list = []
for i in lista:
    #Seteo del periodo estudiado
    start = datetime(2018, 1, 1)
    end = datetime(2018, 1, 31)
    #seteo de locacion (latitud, longitud, elevacion)
    location = Point([i][0][0], [i][0][1], [i][0][2])
    # indicamos que queremos una frecuencia por hora
    data = Hourly(location, start, end)
    data = data.fetch()
    #creamos un dataframe
    df_weather = pd.DataFrame(data)
    df_weather['Borough'] = [i][0][3]
    df_weather_list.append(df_weather)
df_weather = pd.concat(df_weather_list) 

df_weather.reset_index(inplace=True)

#eliminamos las columnas muchos valores nulos (o todos)
df_weather.drop(["snow"], axis = 1, inplace = True)
df_weather.drop(["wpgt"], axis = 1, inplace = True)
df_weather.drop(["tsun"], axis = 1, inplace = True)
df_weather.drop(["coco"], axis = 1, inplace = True)

df_weather['prcp'].fillna(0, inplace = True)

a = df_weather['wdir'].mean() #promedio de direccion de viento
df_weather['wdir'].fillna(a, inplace=True)
   
b = df_weather['pres'].mean() #promedio de direccion de viento
df_weather['pres'].fillna(b, inplace=True) #promedio de presion atmosferica

df_weather.rename(columns={"dwpt": "dew_point", "rhum": "hum", "prcp":"rain", "Borough":"borough", "wdir":"wind_dir", "wspd":"wind_speed"}, inplace=True)

df_weather_borough = pd.DataFrame(df_weather['borough'].unique())

df_weather_borough.reset_index(inplace = True)

df_weather_borough.rename(columns={0: "borough", "index":"id_borough"}, inplace=True)

df_weather.replace({"The Bronx":0, "Brooklyn":1, "Manhattan":2, "Queens":3, "Staten Island":4}, inplace=True)

df_weather.rename(columns={"borough":"id_borough"}, inplace=True)

df_weather.loc[df_weather.rain > 20, 'rain'] = 1

df_weather['id_time_borough'] = df_weather.time.dt.strftime('%Y%m%d%H') + df_weather.id_borough.astype(str)

###############################################################
print("Tabla weather subida correctamente")