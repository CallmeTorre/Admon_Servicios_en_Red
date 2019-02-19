import sys
sys.path.append('./data')
agents_db = './data/agents.txt'

def get_agents():
    agents = []
    with open(agents_db) as file:
        for agent in file:
            agents.append(agent.split(' '))
    return agents

def add_agent(agent):
    with open(agents_db, 'a') as file:
        file.write(agent + '\n')

def delete_agent(agent_id):
    with open(agents_db, "r") as file:
        lines = file.readlines()
        with open(agents_db, "w") as new_file:
            for line in lines:
                if line.split(' ')[0] == agent_id:
                    pass
                else:
                    new_file.write(line)

