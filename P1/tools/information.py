import sys
import time
import rrdtool
import network as nt
import threading as thr
sys.path.append('./data')
agents_db = './data/agents.txt'

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

def generateTCPTraffic(community, ip, port):
    __createTCPDatabase()
    thr.Thread(target=__generateTCPTraffic, args=(community, ip, port)).start()
    thr.Thread(target=__generateTCPImage).start()

def __generateTCPTraffic(community, ip, port):
    total_input_traffic = 0
    total_output_traffic = 0

    while True:
        total_input_traffic = int(nt.getInputTraffic(community, ip, port))
        total_output_traffic = int(nt.getOutputTraffic(community, ip, port))
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdtool.update('./data/rd/tcp/trafico.rrd', value)
        rrdtool.dump('./data/rd/tcp/trafico.rrd', './data/rd/tcp/trafico.xml')
        time.sleep(1)

def __generateTCPImage():
    current_time = str(int(time.time()))
    while True:
        ret = rrdtool.graph("./data/rd/tcp/trafico.png",
                            "--start", current_time,
                            #"--end", "N",
                            "--title=TCP",
                            "--vertical-label=SEG IN",
                            "DEF:inoctets=./data/rd/tcp/trafico.rrd:inoctets:AVERAGE",
                            "DEF:outoctets=./data/rd/tcp/trafico.rrd:outoctets:AVERAGE",
                            "AREA:inoctets#00FF00:  ",
                            "LINE1:outoctets#0000FF:SEG Out \r")
        time.sleep(30)

#TODO Add try catch
def __createTCPDatabase():
    rrdtool.create( "./data/rd/tcp/trafico.rrd",
                    "--start", 'N',
                    "--step", '10',
                    "DS:inoctets:COUNTER:60:U:U",
                    "DS:outoctets:COUNTER:60:U:U",
                    "RRA:AVERAGE:0.5:6:10",
                    "RRA:AVERAGE:0.5:1:10")