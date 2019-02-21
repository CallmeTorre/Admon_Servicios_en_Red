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
            agents.append(agent.split(' '))
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

def generateAllTraffic(community, ip, port):
    rrdt.createRRDDatabase(tcp_db)
    rrdt.createRRDDatabase(snmp_db)
    rrdt.createRRDDatabase(icmp_db)
    rrdt.createRRDDatabase(udp_db)
    rrdt.createRRDDatabase(traffic_db)
    thr.Thread(target=__generateTCPTraffic, args=(community, ip, port)).start()
    thr.Thread(target=__generateSNMPTraffic, args=(community, ip, port)).start()
    thr.Thread(target=__generateICMPTraffic, args=(community, ip, port)).start()
    #thr.Thread(target=__generateUDPTraffic, args=(community, ip, port)).start()
    thr.Thread(target=__generateTraffic, args=(community, ip, port)).start()
    thr.Thread(target=__generateAllImages).start()

def __generateTCPTraffic(community, ip, port):
    total_input_traffic = 0
    total_output_traffic = 0

    while True:
        total_input_traffic = int(nt.getInputTCPTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputTCPTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(tcp_db, value)
        time.sleep(5)

def __generateSNMPTraffic(community, ip, port):
    while True:
        total_input_traffic = int(nt.getInputSNMPTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputSNMPTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(snmp_db, value)
        time.sleep(1)

def __generateICMPTraffic(community, ip, port):
    while True:
        total_input_traffic = int(nt.getInputICMPTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputICMPTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(icmp_db, value)
        time.sleep(1)

def __generateUDPTraffic(community, ip, port):
    while True:
        total_input_traffic = int(nt.getInputUDPTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputUDPTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(udp_db, value)
        time.sleep(1)

def __generateTraffic(community, ip, port):
    while True:
        total_input_traffic = int(nt.getInputTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(traffic_db, value)
        time.sleep(1)

def __generateAllImages():
    current_time = str(int(time.time()))
    while True:
        rrdt.createRRDImage(tcp_db, current_time, "tcp")
        rrdt.createRRDImage(snmp_db, current_time, "snmp")
        rrdt.createRRDImage(icmp_db, current_time, "icmp")
        rrdt.createRRDImage(udp_db, current_time, "udp")
        rrdt.createRRDImage(traffic_db, current_time, "traffic")
        time.sleep(30)