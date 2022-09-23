from datetime import date, datetime
from tkinter import Variable
import pandas as pd # pip install pandas
import pypyodbc as odbc
from requests import Response 
from Google import create_service

""" OBTENER EL DATA SET DE GOOGLE SHEETS """

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

google_sheets_id = '1VMjvWyTW8B778g1rrSAaD7LnROYriiMZsc365uoqszY'

response = service.spreadsheets().values().get(
    spreadsheetId=google_sheets_id,
    majorDimension='ROWS',
    range='B1:D3'
).execute()

#   IGNORA EL ENCABEZADO Y TRAE SOLO LOS VALORES 

row = response['values'][1:]

#for value in row:
#    print(value[0],value[1],value[2])

#id = value[0]
#fecha=value[1]
#valor=float(value[2])

print("192.168.1.28",row)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = '192.168.1.28'
DATABASE_NAME = 'B00010006'
  
def connection_string(driver_name, server_name, database_name):
    uid="admin"
    pwd="polysaco"
    conn_string = f"""
        DRIVER={{{driver_name}}};
        SERVER={server_name};
        DATABASE={database_name};
        UID={uid};
        PWD={pwd};
        Trust_Connection=yes;        
    """
    return conn_string

try:    
    conn = odbc.connect(connection_string(DRIVER_NAME,SERVER_NAME,DATABASE_NAME))
    print('Connection created')    
except odbc.DatabaseError as e:
    print('Database Error:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error')
    print(str(e.value[1]))
else:
    #CONEXION QUE DA ACCESO A LAS TABLAS
    cursor = conn.cursor()
    sql_insert = """
        INSERT INTO dbo.en01divisa (fecha,valor,moneda)
        VALUES(?,?,?)
    """    
    try:
        cursor.executemany(sql_insert,row)
        cursor.commit()
        print('Data import complete')
    except Exception as e:
        print(str(e.value[1]))
        cursor.rollback()
    finally:
        cursor.close()
        conn.close()
        
