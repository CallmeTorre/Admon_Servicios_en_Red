import sys
sys.path.append('./data')
agents_db = './data/agents.txt'

def get_agents():
    agents = []
    with open(agents_db) as file:
        for agent in file:
            agents.append(agent.split(','))
    return agents