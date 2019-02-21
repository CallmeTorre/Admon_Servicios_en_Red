from enum import Enum

OIDPREFIX = '1.3.6.1.2.1'

class OID(Enum):
    TCPInputTraffic = '.6.10.0'
    TCPOutputTraffic = '.6.11.0'
    SNMPInput = '.11.1.0'
    SNMPOutput = '.11.2.0'
    UDPInput = '.7.1.0'
    UDPOutput = '.7.4.0'
    ICMPInput = '.5.1.0'
    ICMPOutput = '.5.14.0'
    TrafficInput = '.2.2.1.10.3'
    TrafficOutput = '.2.2.1.16.3'
    UpTime = '.25.1.1.0'
    Location = '.1.6.0'
    Name = '.1.5.0'
    OS = '.1.1.0'
    Processes = '.25.1.6.0'
    DateAndTime = '.25.1.2.0'