# HTTP Bruteforcer

## How to use
```
# No configuration file:
python3 main.py -u www.example.local [options]

# With configuration file:
python3 main.py -c /path/to/script.config

# Some options in the config file and some via prompt(promt has priority):
python3 main.py [options] -c /path/to/script.config

# Configuration file settings:
Flags carrying additional parameters must separate the flag from the
parameter by "=". Likewise, the flags will be indicated by the following names:
* -u=url
* -v=verbose
* -r=file_reporte
* -m=mhttp
* -i=list_busqueda
* -s=certificado
* -a=agente_usuario
* -e=servidor_ver
* -t=tiempo_req
```

### Flags description:
* -h: Help.
* -u: URL on which the analysis will be done. Consider protocol (HTTP | HTTPS), host (IP | domain name), port and directory.
* -v: Verbose mode
* -r: Used to indicate the file where the results will be reported. If not stated, consider whether it is written to a file by default or to standard output.
* -m: used to tell the program to look for enabled HTTP methods.
* -i: used to indicate to the program the list of files to search.
* -s: used to tell the program to give information about TLS / SSL (certificate)
* -a: used to tell the program which user agent (User-Agent) to use in each request
* -e: used to tell the program to extract the versions of the server (HTTP headers) and the application (HTML tag)
* -t: used to indicate a wait of n seconds between requests to avoid blocking by the server.
* -c: used to indicate a configuration file containing all the desired execution options.

## Description
The goal of this program is to find files with sensitive information hosted on web servers, such as, for example, database backups, code repositories, configuration files, etc.

Likewise, the program will serve to display relevant information about the server and the application:
- Server version via HTTP headers 'Server' and 'X-Powered-By'
- CMS version, if you use one, through the HTML tag 'generator'
- HTTP methods enabled through the OPTIONS method
- Validity of the certificate and its information (in case the service is using HTTPS)

## Descripción adicional:
It only performs the scan from the url that is indicated to deeper directories, that is, if the url http://something.com/archives/ is sent as a parameter it does not search in external directories or on the same level, for this case example: http://algo.com/ or http://algo.com/imagenes/
