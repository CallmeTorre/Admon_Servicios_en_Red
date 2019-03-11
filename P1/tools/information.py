import sys
import time
import rrdt
import rrdtool
import network as nt
import threading as thr

sys.path.append('./data')
agents_db = './data/agents.txt'
tcp_db = './data/rd/tcp'
snmp_db = './data/rd/snmp'
icmp_db = './data/rd/icmp'
udp_db = './data/rd/udp'
traffic_db = './data/rd/traffic'

def getAgents():
    agents = []
    with open(agents_db) as file:
        for agent in file:
            info = agent.split(' ')
            if not nt.hasConexion(info[0]):
                info[-1] = 'DOWN'
            agents.append(info)
    return agents

def addAgent(agent):
    with open(agents_db, 'a') as file:
        file.write(agent + '\n')

def deleteAgent(agent_id):
    with open(agents_db, "r") as file:
        lines = file.readlines()
        with open(agents_db, "w") as new_file:
            for line in lines:
                if line.split(' ')[0] == agent_id:
                    pass
                else:
                    new_file.write(line)

def getAgentOS(community, ip, port):
    return nt.getOS(community, ip, port)

def getAgentLocation(community, ip, port):
    return nt.getLocation(community, ip, port)

def getAgentName(community, ip, port):
    return nt.getName(community, ip, port)

def getAgentUptime(community, ip, port):
    return nt.getUpTime(community, ip, port)

def getAgentInterfaces(community, ip, port):
    return nt.getInterfaces(community, ip, port)

def generateAllTraffic(community, ip, port):
    rrdt.createRRDDatabase(tcp_db)
    rrdt.createRRDDatabase(snmp_db)
    rrdt.createRRDDatabase(icmp_db)
    rrdt.createRRDDatabase(udp_db)
    rrdt.createRRDDatabase(traffic_db)

    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputTCPTraffic', 'getOutputTCPTraffic', tcp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputSNMPTraffic', 'getOutputSNMPTraffic', snmp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputICMPTraffic', 'getOutputICMPTraffic', icmp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputUDPTraffic', 'getOutputUDPTraffic', udp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputTraffic', 'getOutputTraffic', traffic_db), daemon=True).start()
    thr.Thread(target=__generateAllImages, daemon=True).start()

def __generateGeneralTraffic(community, ip, port, inputMethod, outputMethod, db):
    total_input_traffic = 0
    total_output_traffic = 0
    while True:
        try:
            total_input_traffic = int(getattr(nt,inputMethod,)(community, ip, port))
        except ValueError:
            total_input_traffic = 0
        try:
            total_output_traffic = int(getattr(nt,outputMethod,)(community, ip, port))
        except ValueError:
            total_output_traffic = 0
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(db, value)
        time.sleep(5)

def __generateAllImages():
    current_time = str(int(time.time()))
    while True:
        rrdt.createRRDImage(tcp_db, current_time, "Equipo 12 tcp")
        rrdt.createRRDImage(snmp_db, current_time, "Equipo 12 snmp")
        rrdt.createRRDImage(icmp_db, current_time, "Equipo 12 icmp")
        rrdt.createRRDImage(udp_db, current_time, "Equipo 12 udp")
        rrdt.createRRDImage(traffic_db, current_time, "Equipo 12 traffic")
        time.sleep(30)