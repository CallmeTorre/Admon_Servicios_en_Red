import re

from difflib import Differ
import filecmp, time, sys, os
import telnetlib, ftplib

from pysnmp.hlapi import *
from pysnmp.smi import builder
from pysnmp.smi import builder, view, compiler, rfc1902

def dowloadFile(ip):
    tel = telnetlib.Telnet(ip, 23)
    tel.read_until("User: ")
    tel.write("rcp\n")
    tel.read_until("Password: ")
    tel.write("rcp\n")
    time.sleep(1)
    tel.write("en \r\n conf \r\n service ftp \r\n copy run start \r\n exit \r\n  exit \r \n")
    time.sleep(1)
    tel.close()

    ftp = ftplib.FTP(ip)
    ftp.login("rcp","rcp")
    print(f"Descargando archivo de congiruración de {ip}")
    try:
        os.mkdir("download/" + ip)
        ftp.retrbinary("RETR " + "startup-config" ,open("./dfiles/" + filename, 'wb').write)
        print("Descargado archivo de configuracion")
    except:
        print("Error tratando de descargar el archivo")
    ftp.quit()

def uploadFile(ip, file_to_upload):
    ftp = ftplib.FTP(ip)
    ftp.login("rcp","rcp")
    try:
        print(f"Subiendo archivo {file_to_upload} a {ip}")
        ftp.storbinary("STOR newconfig", open(file_to_upload, "rb"), 1024)
    except:
        print(f"Error tratando de subir archivo {file_to_upload} a {ip}")
    ftp.quit()

    tel = telnetlib.Telnet(ip, 23)
    tn.read_until("User: ")
    tn.write("rcp\n")
    tn.read_until("Password: ")
    tn.write("rcp\n")
    time.sleep(1)
    tn.write("en \r\n conf \r\n service ftp \r\n copy running-config startup-config \r\n copy newconfig startup-config \r\n exit \r\n  exit \r \n")
    time.sleep(1)
    tn.close()
    print(f"Aplicando las configuraciones subidas")

def compareFiles(file1, file2):
    with open(file1) as f1:
        f1_text = f1.read()
    with open(file2) as f2:
        f2_text = f2.read()
    difference = filecmp.cmp(file1, file2)
    if difference:
        print(f"No hay diferencia entre {file1} y {file2}")
    else:
        print("Diferencias entre archivos: ")
        d = Differ()
        difference = list(d.compare(f1_text.splitlines(1), f2_text.splitlines(1)))
        print("\n".join(difference))

def checkSNMP(community, host, port, oid):
    mibBuilder = builder.MibBuilder()
    mibViewController = view.MibViewController(mibBuilder)
    compiler.addMibCompiler(mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@'])
    mibBuilder.loadModules('RFC1213-MIB','IF-MIB')
    objectIdentity = rfc1902.ObjectIdentity(oid).resolveWithMib(mibViewController)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port), timeout = 1.5, retries=0),
               ContextData(),
                ObjectType( objectIdentity )))

    if errorIndication:
        print(errorIndication, " : ", host)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= " ".join(varB.split()[2:])
            return resultado
    return -1

if __name__== "__main__":
    print("1.Subir configuracion")
    print("2.Descargar configuracion")
    print("3.Comparar archivos")
    print("4.Obtener inventario")
    option = input("Opcion:")
    if option == "1":
        ip = input("Ip: ")
        fil = input("Archivo: ")
        uploadFile(ip, fil)
    elif option == "2":
        ip = input("Ip: ")
        dowloadFile(ip)
    elif option == "3":
        file1 = input("Archivo1: ")
        file2 = input("Archivo2: ")
        compareFiles(file1, file2)
    else:
        ip = input("Ip: ")
        community = input("Comunidad: ")
        port = input("Puerto: ")
        texto = ""
        print("Sistema: " + checkSNMP(community, ip, port, "1.3.6.1.2.1.1.1.0"))
        print("Contacto: " + checkSNMP(community, ip, port, "iso.3.6.1.2.1.1.4.0"))
        num_interfaces = checkSNMP(community, ip, port, "iso.3.6.1.2.1.2.1.0")
        print("No. de interfaces de red: " + num_interfaces)
        for i in range( 1, int(num_interfaces)+1 ):
            texto += "Nombre: " + checkSNMP(community, ip, port, "iso.3.6.1.2.1.2.2.1.2."+str(i))
            texto += "\n"
            v = checkSNMP( community, ip, port, "iso.3.6.1.2.1.2.2.1.6."+str(i))
            s = ""
            if v != "":
                v = int(v, 16)
                s = '{0:016x}'.format(v)
                s = ':'.join(re.findall(r'\w\w', s))
            texto += "MAC: " + s
            texto += "\n\n";
        print(texto)
