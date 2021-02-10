#!/usr/bin/python3
import requests,sys,re
def find_sql_related_text(new_resp_text):
    key_str=("sql","syntax","function","does not exist","manual")
    for i in key_str:
        if i in new_resp_text:
            return True
    return False

def fuzz(resp,matches,url):
    sql_chars=(";","--","\'","\\*")
    for i in sql_chars:
        print("Url original: {}".format(url))
        print("Respuesta original")
        print("Codigo: {}   Tamaño: {}".format(resp.status_code,len(resp.content)))
        for j in matches:
            new_url=url[:j+3]+i+url[j+3:]
            print("\n\nUrl prueba: {}".format(new_url))
            new_resp=requests.get(new_url)
            print("Respuesta")
            print("Codigo: {}   Tamaño: {}".format(new_resp.status_code,len(new_resp.content)))
            if find_sql_related_text(new_resp.text.lower()):
                print("Esta petición arrojó una respuesta cuyo contenido muy posiblemente hace referencia a un error en la base de datos")
    return


with open(sys.argv[1]) as file:
    for url in file.readlines():
        matches=[m.start() for m in re.finditer('.=.', url)]
        resp=requests.get(url)
        fuzz(resp,matches,url)
