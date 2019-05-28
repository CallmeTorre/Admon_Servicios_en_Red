from difflib import Differ
import filecmp, time, sys, os
import telnetlib, ftplib

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
        ftp.retrbinary("RETR " + "startup-config" ,open("download/" + filename, 'wb').write)
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
