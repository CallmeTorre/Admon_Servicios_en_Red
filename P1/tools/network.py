import subprocess, platform
from pysnmp.hlapi import *
from tools.constants import OIDPREFIX, OID

def getSnmpInfo(communityName, ip, port, oid, is_complete=False):
    result = ""
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd( SnmpEngine(),
                CommunityData(communityName),
                UdpTransportTarget((ip, port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))))
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
      result = ""
      if is_complete:
        for varBind in varBinds:
          result += (' = '.join([x.prettyPrint() for x in varBind]))
        result = result.split("=")[1]
      else:
        for varBind in varBinds:
          varB=(' = '.join([x.prettyPrint() for x in varBind]))
          result= varB.split()[2]
    return result

def getInputTCPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.TCPInputTraffic.value)

def getOutputTCPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.TCPOutputTraffic.value)

def getInputSNMPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.SNMPInput.value)

def getOutputSNMPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.SNMPOutput.value)

def getInputICMPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.ICMPInput.value)

def getOutputICMPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.ICMPOutput.value)

def getInputUDPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.UDPInput.value)

def getOutputUDPTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.UDPOutput.value)

def getInputTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.TrafficInput.value)

def getOutputTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.TrafficOutput.value)

def getLocation(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + OID.Location.value)

def getName(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + OID.Name.value)

def getOS(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + OID.OS.value, is_complete=True)

def getInterfaces(communityName, ip, port):
  interfaces = []
  for elem in range(1,15):
    interface = getSnmpInfo(
                              communityName,
                              ip,
                              port,
                              OIDPREFIX + OID.Interfaces.value + "." + str(elem))
    interface_status = getSnmpInfo(
                                    communityName,
                                    ip,
                                    port,
                                    OIDPREFIX + OID.InterfaceStatus.value + "." + str(elem))
    if interface == 'No' or interface_status == 'No':
      continue
    interfaces.append((interface,interface_status))
  return interfaces

def getProcesses(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + OID.Processes.value)

def getDateAndTime(communityName, ip, port):
    snmpInfo = getSnmpInfo(communityName,ip,port, OIDPREFIX + OID.DateAndTime.value)
    year = int(snmpInfo[3:7], 16)
    month = int(snmpInfo[7:9], 16)
    day = int(snmpInfo[9:11], 16)
    hour = int(snmpInfo[11:13], 16)
    minutes = int(snmpInfo[13:15], 16)
    seconds = int(snmpInfo[15:17], 16)
    d_sec = int(snmpInfo[17:19], 16)
    return str(year)+"-"+str(month)+"-"+str(day)+", "+str(hour)+":"+str(minutes)+":"+str(seconds)+"."+str(d_sec)

def getUpTime(communityName, ip, port):
    timetick = int(getSnmpInfo(communityName, ip, port, OIDPREFIX + OID.UpTime.value))
    days = int(timetick/8640000)
    timetick -= days*8640000
    hours = int(timetick/360000)
    timetick -= hours*360000
    minutes = int(timetick/6000)
    timetick -= minutes*6000
    seconds = int(timetick/100)
    if(days > 0):
      time = str(days)+"d "+str(hours)+"h "+str(minutes)+"min "+str(seconds)+"seg"
    elif(hours > 0):
      time = str(hours)+"h "+str(minutes)+"min "+str(seconds)+"seg"
    else:
      time = str(minutes)+"min "+str(seconds)+"seg"
    return time

def hasConexion(host):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
    except Exception:
        return False
    return True
