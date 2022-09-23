import datetime
import requests
import re
import syncdb as db

nombre_autor='monitordolarvla'
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFtudwEAAAAAT3gd9aS3w1KeGPLKCz8IFxI1SHM%3D1kyJxnRQDJtnCxHgK6flUO4WB7p3ONqFFg6tF6JkmULyjvxizv"
search_url = "https://api.twitter.com/2/tweets/search/recent"
# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:'+nombre_autor+')','tweet.fields': 'author_id'}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print('Status API =',response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# EXTRAER TEXTO

def extraer(texto,entre_esto1,y_esto1):
  try:
    found1 = re.search(entre_esto1+'(.+?)'+y_esto1, texto).group(1)
    return found1
  except AttributeError:
    return 'N/A'

# RETORNA EL SIGNO CORRESPONDIENTE PARA CAMBIOPORC

def buscaTendecia(str):
    return '+' if (str.find('DIFSUBEDIF') != -1) else '-' if (str.find('DIFBAJADIF') != -1) else ''

def twitter():
  json_response = connect_to_endpoint(search_url, query_params)
    #print('dataset ===>',json_response.get('data'))
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    #print(json.dumps(json_response.get('data'), indent=4, sort_keys=True))
#  for twit in json_response.get('data'):
  for twit in reversed(json_response.get('data')):

    #print('Id del Autor: '+twit['author_id'])
    #print('Nombre del Autor: '+nombre_autor)
    #print('Id del Twit= '+twit['id'])
    str = twit['text']
    #print('Texto Original\n--------------\n'+str+'\n---------------')
    # reemplazar emojis
    str=str.replace('🗓️','AAA').replace('🕒','BBB').replace('💵','CCC').replace('🔻','DIFBAJADIF').replace('🔺','DIFSUBEDIF').replace('=','DIFIGUALDIF').replace(',','.').replace('Bs. ','').replace('%','').replace('APM','PM')
    
    # eliminar line breaks
    str=''.join(str.splitlines())
    #print(str)
    #imprime(str)
    fuente = nombre_autor
    mon_num = 'BS'
    mon_den = '$'
    item = 0
    if str[0:3]=='AAA':
      
      # convertir strings a formatos de datos
      fecha = datetime.datetime.strptime(extraer(str,'AAA ',' BBB'),'%d/%m/%Y').date()
      tasa = float(extraer(str,'CCC ',' DIF'))

      signo=buscaTendecia(str)
      if signo=='+':
        cambiopor = float(extraer(str,'DIF ',' Bs'))
      elif signo=='-':
        cambiopor = float(extraer(str,'DIF ',' Bs'))*-1
      else:
        cambiopor = float(extraer(str,'DIF ',' Bs'))

      hora = extraer(str,'BBB ',' CCC')
      cambioabs = float(extraer(str,'Bs ',' https'))
      idfuente = twit['id']
      medio = 'twitter'
      textorg = twit['text']
      timestamp = datetime.datetime.today()

      item = db.busquedaItem(fecha,fuente,mon_den,mon_num) + 1
      row = [[fuente,mon_num,mon_den,fecha,item,idfuente,tasa,hora,medio,textorg,cambiopor,cambioabs,timestamp]]
      #print("\n FORMATOS: \n","\n fuente: ",fuente,"\n numerador: ",mon_num,"\n denominador: ",mon_den,"\n fecha: ",fecha,"\n item: ",item,"\n idfuente: ",idfuente,"\n tasa: ",tasa,"\n hora: ",hora,"\n medio: ",medio,"\n\n original \n",textorg,"\n\n porcentual: ",cambiopor,"\n absoluto: ",cambioabs,"\n")

      if db.buscatasa(idfuente, fuente, fecha, mon_den, mon_num) == 0:
        db.insertDB(row)
        print('nuevo:',idfuente)
      else:
        print('\n ===== Ya existe el twitt ',idfuente,' ====== \n')
    else:
      print("Twit Publicitario o Informativo")
    print('\n xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n')
