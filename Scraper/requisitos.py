#!/usr/bin/python3

import subprocess

"""
Función para instalar los requisitos del programa

"""

def install():
    subprocess.call('sudo apt update', shell=True)
    subprocess.call('sudo apt install python3-pip -y', shell=True)
    subprocess.call('pip3 install requests', shell=True)
    subprocess.call('sudo apt install tor -y', shell=True)
    subprocess.call('pip3 install fake_useragent', shell=True)
    subprocess.call('sudo apt install build-essential libssl-dev libffi-dev python-dev -y', shell=True)
    subprocess.call('pip3 install stem', shell=True)
    subprocess.call('pip3 install pysocks', shell=True)
    subprocess.call('pip3 install bs4', shell=True)

install()
