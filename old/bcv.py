import requests
import bs4
import datetime as dt
import syncdb as db

def bcv():

    meses = ("enero","febrero","marzo","abril","mayo","junio","julio",
        "agosto","septiembre","octubre","noviembre","diciembre")

    res = requests.get("http://bcv.org.ve/")
    soup = bs4.BeautifulSoup(res.text,"lxml")

    tasadolar = round(float(soup.select('#dolar strong')[0].text.strip().replace('.','').replace(',','.')),2)
    tasaeuro = round(float(soup.select('#euro strong')[0].text.strip().replace('.','').replace(',','.')),2)

    fechaStr=soup.select('.dinpro')[0].text.split("Fecha Valor:",1)[1].strip().split(",",1)[1].strip().replace('  ',' ')
    fec=fechaStr.split(' ')
    fec[1]=str(meses.index(fec[1].lower())+1).zfill(2)

    fecha=dt.datetime.strptime(fec[2]+'-'+fec[1]+'-'+fec[0],'%Y-%m-%d')
    fuente='bcv'
    idfuente='N/A'
    mon_num = 'BS'
    mon_den = ['EUR','$']
    hora = 'N/A'
    medio = 'website'
    textorg = 'N/A'
    cambiopor = 0
    cambioabs = 0
#    timestamp = dt.datetime.today()
    itemdol = db.busquedaItem(fecha,fuente,mon_den[1],mon_num) + 1
    itemeu = db.busquedaItem(fecha,fuente,mon_den[0],mon_num) + 1
    #rowd = [[fuente,mon_num,mon_den[1],fecha,itemdol,idfuente,tasadolar,hora,medio,textorg,cambiopor,cambioabs,timestamp]]
    #rowe = [[fuente,mon_num,mon_den[0],fecha,itemeu,idfuente,tasaeuro,hora,medio,textorg,cambiopor,cambioabs,timestamp]]
    
    dicdolar = {
        "fuente": fuente,
        "mon_num": mon_num,
        "mon_den": mon_den[1],
        "fecha": fecha,
        "item": itemdol,
        "idfuente": idfuente,
        "tasa": tasadolar,
        "hora": hora,
        "medio": medio,
        "textorg": textorg,
        "cambiopor": cambiopor,
        "cambioabs": cambioabs
    }

    diceuro={
        "fuente": fuente,
        "mon_num": mon_num,
        "mon_den": mon_den[0],
        "fecha": fecha,
        "item": itemeu,
        "idfuente": idfuente,
        "tasa": tasaeuro,
        "hora": hora,
        "medio": medio,
        "textorg": textorg,
        "cambiopor": cambiopor,
        "cambioabs": cambioabs
    }

    for i in mon_den:
        if db.buscatasa(idfuente, fuente, fecha,i, mon_num) == 0:
            if i == 'EUR':
                db.POST(diceuro)
            else:
                db.insertDB(dicdolar)
        else:
            print('\n tasa ',mon_num,'/',i,' bcv al ', fecha,' ya existe \n')