from pysnmp.hlapi import *

OIDPREFIX = '1.3.6.1.2.1'

def getSnmpInfo(communityName, ip, port, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
        CommunityData(communityName, mpModel=0),
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
        for varBind in varBinds:
            result += (' = '.join([x.prettyPrint() for x in varBind]))
    return result.split("=")[1]

def getInputTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + '.6.10.0')

def getOutputTraffic(communityName, ip, port):
    return getSnmpInfo(communityName, ip, port, OIDPREFIX + '.6.11.0')

def getUpTime(communityName, ip, port):
    timetick = int(getSnmpInfo(communityName, ip, port, OIDPREFIX + '.25.1.1.0'))
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

def getLocation(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + '.1.6.0')

def getName(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + '.1.5.0')

def getOS(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + '.1.1.0')

def getProcesses(communityName, ip, port):
    return getSnmpInfo(communityName,ip,port, OIDPREFIX + '.25.1.6.0')

def getDateAndTime(communityName, ip, port):
    snmpInfo = getSnmpInfo(communityName,ip,port, OIDPREFIX + '.25.1.2.0')
    year = int(snmpInfo[3:7], 16)
    month = int(snmpInfo[7:9], 16)
    day = int(snmpInfo[9:11], 16)
    hour = int(snmpInfo[11:13], 16)
    minutes = int(snmpInfo[13:15], 16)
    seconds = int(snmpInfo[15:17], 16)
    d_sec = int(snmpInfo[17:19], 16)
    return str(year)+"-"+str(month)+"-"+str(day)+", "+str(hour)+":"+str(minutes)+":"+str(seconds)+"."+str(d_sec)

def hasConexion(host):
    return not bool(os.system("ping -c 1 " + host))
