from enum import Enum

OIDPREFIX = '1.3.6.1.2.1'

class OID(Enum):
    TCPInputTraffic = '.6.10.0'
    TCPOutputTraffic = '.6.11.0'
    SNMPInput = '.11.1.0'
    SNMPOutput = '.11.2.0'
    UpTime = '.25.1.1.0'
    Location = '.1.6.0'
    Name = '.1.5.0'
    OS = '.1.1.0'
    Processes = '.25.1.6.0'
    DateAndTime = '.25.1.2.0'