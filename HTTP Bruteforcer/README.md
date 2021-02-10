# HTTP Bruteforcer

## ¿Cómo usarlo?
```
# Sin archivo de configuración:
python3 main.py -u www.example.local [options]

# Con archivo de configuración:
python3 main.py -c /path/to/script.config

# Combinado(Se da prioridad a las banderas de la terminal):
python3 main.py [options] -c /path/to/script.config

# Archvio de configuración:
Las banderas que llevan parametros adicionales deberán separar la bandera del
parametro por un "=". Asimismo, las banderas serán indicadas por los siguientes nombres:
* -u:url
* -v:verbose
* -r:file_reporte
* -m:mhttp
* -i:list_busqueda
* -s:certificado
* -a:agente_usuario
* -e:servidor_ver
* -t:tiempo_req
```

### Banderas Disponibles:
* -h: Ayuda sobre las opciones del programa.
* -u: URL sobre la cuál se hará el análisis. Considerar protocolo (HTTP|HTTPS), host (IP|nombre de dominio), puerto y directorio.
* -v: Modo verboso, sirve para que el programa sea descriptivo durante su ejecución. En caso de no indicarse, debe ser silencioso.
* -r: Sirve para indicar el archivo donde se reportarán los resultados. Si no se indica, considerar si se escribe en un archivo por defecto o en la salida estándar.
* -m: sirve para indicarle al programa que busque los método HTTP habilitados.
* -i: sirve para indicarle al programa la lista de archivos para hacer la búsqueda.
* -s: sirve para indicarle al programa que dé información sobre TLS/SSL (certificado)
* -a: sirve para indicarle al programa qué agente de usuario (User-Agent) utilizar en cada petición
* -e: sirve para indicarle al programa que extraiga las versiones del servidor (encabezados HTTP) y de la aplicación (etiqueta HTML)
* -t: sirve para indicar una espera de n segundos entre peticiones para evitar bloqueos por parte del servidor.
* -c: sirve para indicar un archivo de configuración que contenga todas opciones de ejecución deseadas.

## Descripción
El objetivo de este programa es encontrar archivos con información sensible alojados en servidores web, como por ejemplo, respaldos de bases de datos, repositorios de código, archivos de configuración, etc.

Asimismo, el programa servirá para mostrar información relevante del servidor y la aplicación:
- Versión del servidor a través de los encabezados HTTP 'Server' y 'X-Powered-By'
- Versión del CMS, en caso de utilizar uno, a través de la etiqueta HTML 'generator'
- Métodos HTTP habilitados a través del método OPTIONS
- Validez del certificado y la información del mismo (en caso de que el servicio esté usando HTTPS)

## Descripción adicional:
Unicamente realiza el escaneo a partir de la url que se le indica a directorios mas profundos, es decir, si se envia como parámetro la url http://algo.com/archivos/ no busca en directorios externos o del mismo nivel por ejemplo: http://algo.com/ o http://algo.com/imagenes/
