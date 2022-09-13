import datetime
import numpy as np
import pandas as pd


from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ssl_args = {'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}}
engine = create_engine('mysql://user:passsword/database', connect_args=ssl_args)

#Create table payment_type

p_type = {'id_payment_type': [1, 2, 3, 4, 5, 6], 'type': ['Credit card', 'Cash', 'No charge', 'Dispute' ,'Unknown', 'Voided trip']}
df_p_type = pd.DataFrame(p_type)
print('Tabla payment_type creada')


df_p_type.to_sql('payment_type', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla payment_type subida')





#Create table ratecode

ratecode = {'id_ratecode': [1, 2, 3, 4, 5, 6], 'descript': ['Standard rate', 'JFK', 'Newark', 'Nassau or Westchester' ,'Negotiated fare', 'Group ride']}
df_ratecode = pd.DataFrame(ratecode)
print('Tabla rate_code creada')



df_ratecode.to_sql('rate_code', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla rate_code subida')



#Create tabla vendor

vendor = {'id_vendor': [1, 2], 'descript': ['Creative Mobile Technologies', 'VeriFone Inc.']}
df_vendor = pd.DataFrame(vendor)
print('Tabla vendor creada')



df_vendor.to_sql('vendor', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla vendor subida')


#Create tabla borough

df_borough = pd.read_csv('borough.csv')
print('Tabla borough creada')

df_borough.to_sql('borough', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla borough subida')



#Create tabla zone

df_zone = pd.read_csv('zone.csv')
print('Tabla zone creada')


df_zone.to_sql('zone', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla zone subida')


#Create tabla weather

df_weather = pd.read_csv('data_weather.csv')
print('Tabla weather creada')


df_weather.to_sql('weather', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla weather subida')


#Create tabla weather_snow

df_weather_snow = pd.read_csv('weather_snow.csv')
print('Tabla weather_snow creada')


df_weather_snow.to_sql('weather_snow', con = engine, if_exists = 'replace', index=False, method='multi')
print('Tabla weather_snow subida')


