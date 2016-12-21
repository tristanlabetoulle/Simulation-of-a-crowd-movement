from Agent import Agent

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from math import exp

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.set_xlim([-5,5])
ax1.set_ylim([-5,5])


agent1 = Agent((0.2,0),1)
agent2 = Agent((2.2,0),1)
agent3 = Agent((0,2),1)
agent4 = Agent((2,2),1)

agents = []
agents.append(agent1)
agents.append(agent2)
agents.append(agent3)
agents.append(agent4)

agent1.speed = (1,1.8)
agents = agent1.update_position(agents, None, 1)




for agent in agents:
    print sum(agent.colour.itervalues())
    colour = min(exp(sum(agent.colour.itervalues())-2),1)
    ax1.add_patch(patches.Circle(agent.position,1,color=[colour,0,0]))

plt.show()