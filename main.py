# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup as btf
import requests as rq

def ExtracicionTexto():
    website = 'https://subslikescript.com/movie/Titanic-120338'
    try:
        result = rq.get(website)
        return result.text
    except Exception as e:
        result = 'no hay sitio web'
        return result

def UsandoParser():
    # localiza elementos y contiene la pagina
    soup = btf(ExtracicionTexto(),'lxml')
    # para simplificar la salida prettify
    # print(soup.prettify())
    # para excluir elementos que no queremos
    box_1 = soup.find('article',class_='main-article')
    #obtiene las transcripciones de la pelicula titanic
    titulo = box_1.find('h1').getText(strip=True,separator=' ').replace(' - full transcript',' ')
    transcript = box_1.find('div',class_='full-script').get_text(strip=True,separator=' ')
    #print(titulo)
    #print(transcript)
    with open(f'{titulo}.txt','w') as file:
        file.write(str(transcript))
UsandoParser()