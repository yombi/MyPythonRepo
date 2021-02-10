#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse,sys,urllib.request,re
from datetime import datetime
from bs4 import BeautifulSoup
from subprocess import check_output
from requests import get
from random import choice
from time import sleep

def NormalizaURL(url):
	'''Return String: Normalización http://url.domain to => url.domain'''
	if '//' in url:
		url = url.split('//')
		return url[1]

def NormalizaCertificado(certificado):
	'''Retorna la información relevante del certificado'''
	pass

def RandomAgent():
	user_lists = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36']
	print(choice(user_lists))

def MuestraResultados(lista,lista_url):
	if diccionario['file_reporte']:
		file=open(diccionario['file_reporte'],"w")
	else:
		file=open("reporte.txt","w")
	if diccionario['verbose']:
		print('Mandando resultados al archivo '+file.name)
	for resultado in lista:
		file.write(str(resultado))
		file.write(chr(10))
	for resultado in lista_url:
		file.write(str(resultado))
		file.write(chr(10))
	file.close()

def ExistePalabraClave(url):
	for palabra in PalabrasClave:
		if palabra in url:
			return True
	return False

def GetHTML(url):
	if diccionario['verbose']:
		print("Obteniendo informacion de "+url)
		
	#obtengo el html de la pagina

	# Cambiando
	codigo_html=urllib.request.urlopen(url).read().decode()

	if diccionario['tiempo_req']:
		sleep(int(diccionario['tiempo_req']))

	#lo convierto a objeto BeautifulSoup lo cual lo hace más manejable(ver doc de BeautifulSoup)
	datos=BeautifulSoup(codigo_html,features='html.parser')
	return datos

def GetCMS(url):
	datos=GetHTML(url)
	meta=datos('meta')#la etiqueta meta es la que contiene la version del CMS
	for tag in meta:#obtengo versiones de CMS
		if re.search('[a-z]*[0-9][.][0-9]', str(tag.get('content'))):
			cms.append(str(tag.get('content')))
	return cms

def RecorrePagina(raiz,url):#raiz es la url original que se mandó en terminal o archivo
	if diccionario['verbose']:
		print("Entrando a "+url)
	datos=GetHTML(url)
	links=datos('a')#obtengo todos los enlaces
	for tag in links:
		#print("Liga a evaluar: "+str(tag.get('href')))
		if ExistePalabraClave(str(tag.get('href'))):
			resultados_url.append(str(tag.get('href')))
		if not re.search(raiz, str(tag.get('href'))) or str(tag.get('href')) in visitados or re.search(raiz+'.*[.]', str(tag.get('href'))):
			continue
		if diccionario['verbose']:
			print("Llendo a "+str(tag.get('href')))
		visitados.append(str(tag.get('href')))
		RecorrePagina(raiz,str(tag.get('href')))

def GetHeaderServer(url):
	'''Retorna datos del servidor en un diccionario'''
	if diccionario['verbose']:
		print('Extrayendo datos del servidor')
	result = {'date':'','server':'','powered':'','X-XSS-Protection':''}
	try:
		response = get(url)
		# print(response.headers)
		try:
			date = response.headers['Date'] # Fecha
			result['date'] = date
		except:
			pass
		try:
			server = response.headers['Server'] # Servidor
			result['server'] = server
		except:
			pass
		try:
			powered = response.headers['X-Powered-By'] # Versión de php
			result['powered'] = powered
		except:
			pass
		try:
			powered = response.headers['X-XSS-Protection'] # Protección contra X-XSS
			result['X-XSS-Protection'] = powered
		except:
			pass
	except:
		print("Sitio no disponible")
	return result

def GetOptions(url):
	'''Retorna las opciones habilitadas en un string'''
	if diccionario['verbose']:
		print('Verificando opciones activadas del server')
	url = NormalizaURL(url)
	flags = 'curl -X OPTIONS '+url+' -i -s | grep Allow:'
	output = ''
	try:
		output = (check_output(flags, shell=True)).decode("utf-8")
		output = output.split('\r\n')
		output = output[0] # Filtramos para obtener: Allow: GET, HEAD
	except:
		print("Error al obtener OPTIONS")
	return output

def GetCertServer(url):
	'''Retorna un string con toda la información del certificado SSL'''
	if diccionario['verbose']:
		print('Obteniendo informacion del certificado')
	# Normalización http://url.domain to => url.domain
	url = NormalizaURL(url)
	# flags = 'keytool -printcert -sslserver '+url+':443 >cert.txt' # Así puedes sacar todo el documento a un archivo
	flags = 'keytool -printcert -sslserver '+url+':443 > certificado_completo.txt'
	#print(flags)
	output = ''
	try:
		output = (check_output(flags, shell=True)).decode("utf-8")
	except:
		print("Error al obtener el certificado, el sitio puede no tener ssl")
	if output:
		return output
	return 'No disponible'

if __name__ == "__main__":
#############################################
# Generando Argumentos
	parser = argparse.ArgumentParser()
	parser.add_argument('-u','--url' ,action='store',help="url a atacar")
	parser.add_argument('-v','--verbose' ,action='store_true',help="Modo verboso")
	parser.add_argument('-m', action='store_true',help="buscar metodos http habilitados",dest='mhttp')
	parser.add_argument('-i',nargs='+',help="lista de archivos para hacer la búsqueda",dest='list_busqueda')
	parser.add_argument('-s',action='store_true',help="información sobre TLS/SSL",dest='certificado')
	parser.add_argument('-a',action='store',help="agente de usuario a utilizar",dest='agente_usuario')
	parser.add_argument('-e',action='store_true',help="extraer las versiones del servidor",dest='servidor_ver')
	parser.add_argument('-t',action='store',help="espera de n segundos entre peticiones",dest='tiempo_req')
	parser.add_argument('-c',action='store',help="indicar un archivo de configuración",dest='conf_file')
	parser.add_argument('-r', action='store',help="Archivo sobre el cual escribir el reporte",dest='file_reporte')
	args=parser.parse_args()

	diccionario={}
	cms=[]
	visitados=[]
	resultados_url=[]
	PalabrasClave=[]
	resultados=[]
	fecha=datetime.now()

# Generando diccionario de argumentos
	for k in vars(args):#meto las banderas y sus valores a un diccionario
		diccionario[k]=getattr(args, k)


	if args.conf_file:#Si se dio un archvio de confuguración,completamos el diccionario
	#con esos valores
		with open(args.conf_file) as file:
			for line in file.readlines():
				line=line.rstrip()
				line=line.split("=")
				if not diccionario[line[0]] and line[0] in ['url','list_busqueda','agente_usuario','tiempo_req','file_reporte']:
					diccionario[line[0]]=line[1]
				elif not diccionario[line[0]]:
					diccionario[line[0]]=True

	if not diccionario['url']:
		#Si entra aqui, es por que ni en archivo,ni en linea de comandos se dio una URL
		raise Exception("Se debe dar una url")



	with open('PalabrasClave.txt','r') as file:
		for line in file.readlines():
			PalabrasClave.append(line)
		PalabrasClave.append('.sql')

	if diccionario['certificado']:
		resultados.append('Resultados de la URL '+diccionario['url'])
		resultados.append("Cert:"+GetCertServer(diccionario['url']))

	if diccionario['mhttp']:
		resultados.append("mhttp:"+GetOptions(diccionario['url']))

	if diccionario['servidor_ver']:
		resultados.append("Server:"+str(GetHeaderServer(diccionario['url'])))
	resultados_url.append('Documentos sensibles:')
	RecorrePagina(diccionario['url'],diccionario['url'])
	MuestraResultados(resultados,resultados_url)
