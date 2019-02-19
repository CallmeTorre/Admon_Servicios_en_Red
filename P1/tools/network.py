from pysnmp.hlapi import *

def consulta(nomComunidad,ip,puerto,oid):
  errorIndication, errorStatus, errorIndex, varBinds = next(
      getCmd(SnmpEngine(),
             CommunityData(nomComunidad, mpModel=0),
             UdpTransportTarget((ip, puerto)),
             ContextData(),
             ObjectType(ObjectIdentity(oid)))
  )

  if errorIndication:
      print(errorIndication)
  elif errorStatus:
      print('%s at %s' % (errorStatus.prettyPrint(),
                          errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
  else:
      cadena = ""
      for varBind in varBinds:
          cadena += (' = '.join([x.prettyPrint() for x in varBind]))
      return cadena.split("=")[1]


def checatiempo(nomComunidad,ip,puerto):
  timetick = int(consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.25.1.1.0'))
  dias = int(timetick/8640000)
  timetick -= dias*8640000
  horas = int(timetick/360000)
  timetick -= horas*360000
  minutos = int(timetick/6000)
  timetick -= minutos*6000
  segundos = int(timetick/100)
  if(dias > 0):
    time = str(dias)+"d "+str(horas)+"h "+str(minutos)+"min "+str(segundos)+"seg"
  elif(horas > 0):
    time = str(horas)+"h "+str(minutos)+"min "+str(segundos)+"seg"
  else:
    time = str(minutos)+"min "+str(segundos)+"seg"
  return time

def checalocation(nomComunidad,ip,puerto):
  return consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.1.6.0')

def checaNombre(nomComunidad,ip,puerto):
  return consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.1.5.0')

def checaSistema(nomComunidad,ip,puerto):
  return consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.1.1.0')

def checaProcesos(nomComunidad,ip,puerto):
  return consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.25.1.6.0')

def checaFechaHora(nomComunidad,ip,puerto):
  cadena = consulta(nomComunidad,ip,puerto,'1.3.6.1.2.1.25.1.2.0')
  year = int(cadena[3:7],16)
  month = int(cadena[7:9],16)
  day = int(cadena[9:11],16)
  hour = int(cadena[11:13],16)
  minutes = int(cadena[13:15],16)
  seconds = int(cadena[15:17],16)
  d_sec = int(cadena[17:19],16)
  return str(year)+"-"+str(month)+"-"+str(day)+", "+str(hour)+":"+str(minutes)+":"+str(seconds)+"."+str(d_sec)