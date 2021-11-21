#!/usr/bin/python3
import socket,sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store', required=True,dest='list')
parser.add_argument('-p', action='store',required=True, dest='ports')
arguments=parser.parse_args()
str=arguments.ports
min=int(str.split("-")[0])
max=int(str.split("-")[1])
with open(arguments.list) as file:
    for host in file.readlines():
        print ('\nHost: {}'.format(host))
        host = host.strip('\n')
        host = host.strip('\t')
        host= host.strip('\r')
        ip  = socket.gethostbyname(host)
        for port in range(min,max):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print ("Puerto {} abierto".format(port))
                sock.close()
            except socket.gaierror:
                print ('El host {} no pudo ser resuelto'.format(host))
                sys.exit()
