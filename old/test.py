import datetime as dt
import pypyodbc as odbc
import requests
import json
reqUrlPost = "http://127.0.0.1:8000/multimoneda/tasas/"
headersList = {
  "Accept": "*/*",
  "User-Agent": "dptosistemasgip@gmail.com" 
  }

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = '172.19.48.17,32139'
DATABASE_NAME = 'apidb'

def connection_string(driver_name, server_name, database_name):
    uid="sa"
    pwd="123456Ps"
    conn_string = f"""
        DRIVER={{{driver_name}}};
        SERVER={server_name};
        DATABASE={database_name};
        UID={uid};
        PWD={pwd};
        Trust_Connection=yes;        
    """
    return conn_string

def busquedafechafuente(fechatwit,fuente):
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
        cursor = conn.cursor()
        cursor.execute("select idfuente from dbo.multimoneda_tasas where fecha=? and fuente =?",[fechatwit,fuente])
        try:
            fila = cursor.fetchall()
            return len(fila)
        except Exception as e:
            print(str(e.value[1]))
            cursor.rollback()
        finally:
            cursor.close()
            conn.close()

def buscatasa(idfuente,fuente,fecha,den,num):
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
        cursor = conn.cursor()
        cursor.execute("SELECT id from dbo.multimoneda_tasas where idfuente=? and fuente=? and fecha=? and mon_den=? and mon_num=?",[idfuente,fuente,fecha,den,num])
        try:
            fila = cursor.fetchall()
            return len(fila)
        except Exception as e:
            print(str(e.value[1]))
            cursor.rollback()
        finally:
            cursor.close()
            conn.close()

def main():
    fechatwit = dt.datetime.strptime(input('fecha del twit:'),'%Y-%m-%d').date()
    fuente = input('fuente:')
    idfuente = input('idfuente:')
    num = input('numerador:')
    den = input('denominador:')
    resultado = buscatasa(idfuente,fuente,fechatwit,den,num)
    if resultado == 0:
        print('vacio',resultado)
    else:
        print('la cantidad de registros es: ',resultado)

def POST(diccionario):
  response = requests.request("POST", reqUrlPost, data=diccionario,  headers=headersList)
  print(response.text)

#POST()
#main()