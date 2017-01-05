from Agent import Agent
from Obstacle import Obstacle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from math import exp

from Exit import Exit

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.set_xlim([1,10])
ax1.set_ylim([1,10])


agent1 = Agent((5,5),1)
agent2 = Agent((3,7),1)
agent3 = Agent((0,2),1)
agent4 = Agent((2,2),1)

agents = []
agents.append(agent1)
agents.append(agent2)
agents.append(agent3)
agents.append(agent4)

agent1.speed = (-2,2)
agent2.speed = (0.4,-0.4)
agents = []
agents.append(agent1)
agents.append(agent2)

obstacles = []
obstacle1= Obstacle((-2,2),4,1)
obstacle2= Obstacle((4,0),1,4)
obstacle3= Obstacle((-4,-3),3,1)
obstacle4= Obstacle((-2,4),1,2)

#obstacles.append(obstacle1)
#obstacles.append(obstacle2)
#obstacles.append(obstacle3)
#obstacles.append(obstacle2)

exits = []
exit1 = Exit((4,4),2,2)
#exits.append(exit1)

agent1.update_position(agents, obstacles, exits, 1, (10,10))
agent2.update_position(agents, obstacles, exits, 1, (10,10))

for obstacle in obstacles:
    ax1.add_patch(patches.Rectangle(obstacle.position,obstacle.width,obstacle.height))

for exit in exits:
    ax1.add_patch(patches.Rectangle(exit.position,exit.width,exit.height))

for agent in agents:
    print agent
    colour = agent.get_color_agent()
    ax1.add_patch(patches.Circle(agent.position,agent.size,color=[colour,0,0]))

plt.show()