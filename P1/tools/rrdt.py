import numpy as np
import os
import sys
import rrdtool
import time
from pysnmp.hlapi import *
from numpy import array
import threading

#TODO: Refactor this file

threads = list()
def hilotrafico(nomComunidad,ip,puerto):
    print("Hilo tcp activo")
    ret = rrdtool.create("./data/rd/tcp/trafico.rrd",
                         "--start", 'N',
                         "--step", '10',
                         "DS:inoctets:COUNTER:60:U:U",
                         "DS:outoctets:COUNTER:60:U:U",
                         "RRA:AVERAGE:0.5:6:10",
                         "RRA:AVERAGE:0.5:1:10")
    if ret:
        print(rrdtool.error())

    #threads = list()
    for i in range(2):
        if(i==0):
            t = threading.Thread(target=trafico,args=(nomComunidad,ip,puerto))
            threads.append(t)
            t.start()
        if(i==1):
            t = threading.Thread(target=graficaTrafico)
            threads.append(t)
            t.start()

def trafico(nomComunidad,ip,puerto):
    print(threading.currentThread().getName())
    total_input_traffic = 0
    total_output_traffic = 0

    while 1:
        total_input_traffic = int(
            consultaSNMP(nomComunidad, ip,
                         '1.3.6.1.2.1.6.10.0',puerto))
        total_output_traffic = int(
            consultaSNMP(nomComunidad, ip,
                         '1.3.6.1.2.1.6.11.0',puerto))

        valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        #print(valor)
        rrdtool.update('./data/rd/tcp/trafico.rrd', valor)
        rrdtool.dump('./data/rd/tcp/trafico.rrd', './data/rd/tcp/trafico.xml')
        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)


def graficaTrafico():
    tiempo_actual = int(time.time())
    tiempo_final = tiempo_actual - 86400
    tiempo_inicial = tiempo_final - 25920000 / 60
    print("graficando trafico")
    c = (str)(tiempo_actual)
    print(tiempo_actual)
    while(1):
        ret = rrdtool.graph("./data/rd/tcp/trafico.png",
                            "--start", c,
                            #"--end", "N",
                            "--title=TCP",
                            "--vertical-label=SEG IN",
                            "DEF:inoctets=./data/rd/tcp/trafico.rrd:inoctets:AVERAGE",
                            "DEF:outoctets=./data/rd/tcp/trafico.rrd:outoctets:AVERAGE",
                            "AREA:inoctets#00FF00:  ",
                            "LINE1:outoctets#0000FF:SEG Out \r")
        time.sleep(30)

def consultaSNMP(comunidad,host,oid,puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
    return resultado