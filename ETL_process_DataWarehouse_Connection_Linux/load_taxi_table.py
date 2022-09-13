import datetime
import numpy as np
import pandas as pd

print('¡Bienvenido al proceso de automatización para la carga de datos de taxis de NYC!')
n_registros = int(input("Por favor, ingrese la cantidad de registros que desee añadir: "))

print('Comienza el proceso...')
print('Descargando datos de taxi...')

df = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2018-02.parquet')

df = df.loc[(df.index.values>1000) & (df.index.values<=n_registros+1000)]

print('Datos de taxi descargados correctamente')

print('Normalizando datos de la tabla taxi...')

df.drop(columns=['congestion_surcharge','airport_fee'], inplace=True)

df.drop_duplicates(inplace=True)

df.rename(columns =
                    {'VendorID':'id_vendor',
                    'RatecodeID':'id_ratecode',
                    'PULocationID':'id_pu_zone',
                    'DOLocationID':'id_do_zone'}, inplace = True)


df['trip_distance_aux'] = df['trip_distance']
df['trip_distance_aux'].replace(0, 1, inplace=True)
df['trip_distance_aux'].fillna(1, inplace=True)

df['fare_per_mile'] = df.fare_amount / df.trip_distance_aux

df.loc[df['trip_distance'] == 0, 'fare_per_mile'] = 0

df.drop(columns=['trip_distance_aux'], inplace=True)

df['trip_time'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime

df.trip_time = df.trip_time.dt.total_seconds()

df['trip_time_aux'] = df['trip_time']
df['trip_time_aux'].replace(0, 1, inplace=True)
df['trip_time_aux'].fillna(1, inplace=True)

df['fare_per_minute'] = df.fare_amount / (df.trip_time_aux / 60)

df.loc[df['trip_time'] == 0, 'fare_per_minute'] = 0

df.drop(columns=['trip_time_aux'], inplace=True)

print('Descargando datos de zonas y boroughs...')

df_zone = pd.read_csv('https://raw.githubusercontent.com/soyHenry/DS-Proyecto_Grupal_TaxisNYC/main/taxi%2B_zone_lookup.csv')

print('Datos de zonas y boroughs descargados correctamente')

print('Conectando tabla de taxi y zonas...')

df_zone.rename(columns =
                    {'LocationID':'id_zone',
                    'Borough':'borough',
                    'Zone':'zone'}, inplace = True)


borough_data = {'id_borough': [1, 2, 3, 4, 5, 6, 7], 'borough':['Brooklyn', 'Bronx', 'Manhattan', 'Staten Island', 'Queens', 'EWR', 'Unknown']}
df_borough = pd.DataFrame(borough_data)

dic_zone_borough = {df_zone.id_zone[i] : df_zone.borough[i] for i in range (0,len(df_zone))}

dic_id_borough = {df_borough.borough[i] : df_borough.id_borough[i] for i in range (0, len(df_borough))}

df['pu_borough'] = df.id_pu_zone.map(dic_zone_borough)
df['do_borough'] = df.id_do_zone.map(dic_zone_borough)

df['id_borough'] = df.pu_borough.map(dic_id_borough)

df['id_time_borough'] = df.tpep_pickup_datetime.dt.strftime('%Y%m%d%H') + df.id_borough.astype(str)

df['outlier'] = 1

print('Tablas conectadas correctamente')
print('Identificando outliers de la tabla taxi...')

# Calculamos rango intercuartílico, mínimo, y máximo
IQR = df.trip_distance.quantile(.75) - df.trip_distance.quantile(.25)
min = df.trip_distance.quantile(.25) - (1.5 * IQR)
max = df.trip_distance.quantile(.75) + (1.5 * IQR)

# Indentificamos outliers
df.loc[df.trip_distance < min, "outlier"] = 0
df.loc[df.trip_distance > max, "outlier"] = 0

# Calculamos rango intercuartílico, mínimo, y máximo
IQR = df.fare_amount.quantile(.75) - df.fare_amount.quantile(.25)
min = df.fare_amount.quantile(.25) - (1.5 * IQR)
max = df.fare_amount.quantile(.75) + (1.5 * IQR)

# Indentificamos outliers
df.loc[df.fare_amount < min, "outlier"] = 0
df.loc[df.fare_amount > max, "outlier"] = 0

# Calculamos rango intercuartílico, mínimo, y máximo
IQR = df.trip_time.quantile(.75) - df.trip_time.quantile(.25)
min = df.trip_time.quantile(.25) - (1.5 * IQR)
max = df.trip_time.quantile(.75) + (1.5 * IQR)

# Indentificamos outliers
df.loc[df.trip_time < min, "outlier"] = 0
df.loc[df.trip_time > max, "outlier"] = 0

df['id_trip'] = df.index.values
df['id_trip'] = df['id_trip'] + 1

cols = list(df.columns)
df = df[cols[24:25] + cols[0:24]]

print('Identificación de outliers y normalización de datos finalizada')
print('Comienza la conexion a MySQL y PlanetScale')


print('Subiendo datos a la nube...')
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


ssl_args = {'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}}
engine = create_engine('mysql://user:passsword/database', connect_args=ssl_args)
Base = declarative_base()


df_subset = df.head(n_registros)
df_subset.to_sql('taxi', con = engine, if_exists = 'append', index=False, method='multi')


print('Datos subidos correctamente')
print('¡Proceso finalizado con éxito!')
