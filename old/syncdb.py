import json
import pypyodbc as odbc
#import pyodbc as odbc
import requests
reqUrlPost = "http://industrial-api-escawo.apps.clusteros.ocp.intra.polybarq.com/multimoneda/tasas/"
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

# retorna el tamaño de la consulta,  
# de no existir retorna 0

def buscatasa(idfuente,fuente,fecha,den,num):
    try:    
        conn = odbc.connect(connection_string(DRIVER_NAME,SERVER_NAME,DATABASE_NAME))
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

# busqueda creada para asignar el valor de item, 
# retorna 0 si no encuentra el valor, 
# de lo contrario retorna la cantidad de items

def busquedaItem(fecha,fuente,den,num):
  try:    
      conn = odbc.connect(connection_string(DRIVER_NAME,SERVER_NAME,DATABASE_NAME))
  except odbc.DatabaseError as e:
      print('Database Error:')
      print(str(e.value[1]))
  except odbc.Error as e:
      print('Connection Error')
      print(str(e.value[1]))
  else:
      cursor = conn.cursor()
      cursor.execute("select id from dbo.multimoneda_tasas where fecha=? and fuente =? and mon_den=? and mon_num=?",[fecha,fuente,den,num])
      try:
          fila = cursor.fetchall()
          return len(fila)
      except Exception as e:
          print(str(e.value[1]))
          cursor.rollback()
      finally:
          cursor.close()
          conn.close()

# INSERTAR EN SQLSERVER, crear tuplas con la data para utilizar este metodo


def insertDB(row):
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
      sql_insert = """
        INSERT INTO dbo.multimoneda_tasas (fuente,mon_num,mon_den,fecha,item,idfuente,tasa,hora,medio,textorg,cambiopor,cambioabs,timestamp)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
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

def POST(diccionario):
  response = requests.request("POST", reqUrlPost, data=diccionario,  headers=headersList)
  print(response.text)
