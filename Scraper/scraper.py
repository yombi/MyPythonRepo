#!/bin/python3
"""
Trafico anonimo, cambio de ip ante baneo, obtiene 50 resultados
"""
import sys
import requests
import time
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import stem.socket
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urlparse
from reporte import reporte

engine_paging={
        'google':'start=',
        'bing':'first=',
        'aol':'b=',
        'yahoo':'b=',
        'ecosia':'p=',
        'duckduckgo':''
        }

controller = Controller.from_port() #controlador para interactuar con el socket de tor
proxie = {'https':'socks5://127.0.0.1:9050'} #tor
headers_Get = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

mail_regex = r"[a-zA-Z0-9_.+-áéíóú]+@[a-zA-Z0-9-áéíóú]+\.[a-zA-Z0-9-.áéíóú]+"
results={}
emails = []
alter_query=""
mail=False

def limpieza_url(url):
    resultados = []
    if type(url) == list:
        for u in url:
            url_limpia, url_estructurada = "", ""
            for dot in urlparse(u).path.split("RU=")[1].split('%3a'):
                url_limpia += dot + ":"
            for slash in url_limpia.split('%2f'):
                url_estructurada += slash + "/"
            resultados.append(url_estructurada.split("RK")[0])
        return resultados
    else:
        url_limpia = urlparse(url)
        return url_limpia.scheme + "://" + url_limpia.netloc + "/"


def get_mails(description):
    return re.findall(mail_regex, description, re.I)

def new_ip():
    controller.authenticate(password = 'hola123.,')# autenticacion de acuerdo a lo establecido en /etc/tor/torrc
    controller.signal(Signal.NEWNYM)#renovacion de ip

def get_urls(engine,response):
    soup = BeautifulSoup(response, "html.parser")
    tag="div"
    class_dict={}
    output=[]
    if engine=='google':
        class_dict['class']='r'
    if engine=='bing':
        tag="li"
        class_dict['class']='b_algo'
    if engine=='duckduckgo':
        class_dict['class']='links_main links_deep result__body'
    if engine=='ecosia':
        class_dict['class']='result-firstline-container'
    if engine=='aol':
        class_dict['class']='compTitle options-toggle'
    if engine=='yahoo':
        class_dict['class']='dd algo algo-sr relsrch Sr'
    for tag_div in soup.find_all(tag, class_dict):
        tag_a = tag_div.find_all('a')#obtemos las etiquetas <a href>
        if tag_a:
            output.append(tag_a[0]['href'])#obtenemos la url
    return output

def banned(text):
    if 'CAPTCHA' in text: #Google y ecosia
        return True
    if 'If this error persists, please let us know: error-lite@duckduckgo.com' in text: #Duckduckgo
        return True
    if 'Verizon' in text: #aol y yahoo
        return True
    return False

def search(query,engine):
    aux=0
    page=0
    page_ecosia=0
    output = []
    query = query.replace(' ', '+')
    print(f"Busqueda utilizando {engine}")
    if engine=="duckduckgo":
        url = f'https://html.duckduckgo.com/html/?q={query}'
    while len(output) < 50 and page < 70:
        paging=engine_paging[engine]
        if engine_paging[engine]=='p=':
            paging+=str(page_ecosia)
        else:
            paging+=str(page)
        if engine=="google" or engine=="bing":
            url = f'https://www.{engine}.com/search?q={query}&{paging}'
        if engine=="yahoo" or engine=="aol":
            url = f'https://search.{engine}.com/search?q={query}&{paging}'
        if engine=="duckduckgo":
             url = f'https://html.duckduckgo.com/html/?q={query}'
        if engine=="ecosia":
            url = f'https://www.ecosia.org/search?q={query}&{paging}'
        response = requests.get(url, headers=headers_Get,proxies=proxie)#peticion con headers definidos a traves de tor
#        print(response.text)
        while banned(response.text): #baneado
            print("Ip rechazada")
            new_ip()
            time.sleep(3) #para no sobrecargar tanto a tor
            print(requests.get('https://httpbin.org/ip', proxies=proxie).text)#ip usada en nuestras peticiones
            response = requests.get(url, headers=headers_Get,proxies=proxie)
        print(f"---------------Changing {engine} page----------------")
        print(url)
        page+=10#cambio de página de resultados
        page_ecosia+=1
        #print(response.text)
        #print(get_urls(engine,response.text))

        if mail:
            emails=get_mails(response.text)
            if emails:
                for email in emails:
                    output.append(email)
        else:
            for site in get_urls(engine,response.text):
                output.append(site)
    return output
"""
Funcion que busca los correos electronicos existentes en una pagina web.
"""
#Suponemos que la bandera dada por el usuario --mails esta activada
#mail = 1
if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Es necesario agregar argumentos")
        print("Ej:")
        print("python3 scraper.py -q \"site:unam.mx\" -f xml")
        print("python3 scraper.py -ip 132.248.54.220  -f html")
        print("python3 scraper.py -q \"drupal OR wordpress\"  -f txt")
        print("Ayuda: ")
        print("python3 scraper.py -h")
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--params',action='store_true',dest='params')
    parser.add_argument('-ip', action='store', dest='ip')
    parser.add_argument('-f','--format',action='store',dest='format')
    parser.add_argument('-q','--query',action='store',dest='query')
    arguments=parser.parse_args()
    new_ip()

    datos = reporte(arguments.format, start=True) if arguments.format else None
    if "\"" in arguments.query:
        print(arguments.query)
    if arguments.ip:
        query=f"ip:{arguments.ip}"
    else:
        query=arguments.query
        if "\'" in query:
            query=query.replace("\'", "\"")
    if "mail:" in query:
        index = query.find('mail:')
        alter_query = query[:index+4] + ' ' + query[index+5:]
        mail=True

    for engine in ('google','bing','duckduckgo','aol','ecosia','yahoo'):
        if arguments.ip and engine=='google':
            continue
        if mail and engine != 'google':
            results[engine]=search(alter_query,engine)
        elif arguments.ip and engine=="bing":
            alter_query=query.replace(":", " ")
            results[engine]=search(alter_query,engine)
        else:
            results[engine]=search(query,engine)
        if not mail and (engine == "yahoo" or engine == "aol"):
            results[engine]=limpieza_url(results[engine])
        if arguments.params and not mail:
            for url in results[engine]:
                url=limpieza_url(url)
        if not arguments.format:
            print(f"Resultados de {engine}")
            for res in results[engine]:
                print(res)
        else:
            datos += reporte(arguments.format, engine + " " + query, "header")
            for result in results[engine]:
                datos += reporte(arguments.format, result, "section")
                datos += reporte(arguments.format, option="parrafo")
    reporte(arguments.format, datos, end=True) if arguments.format else None
