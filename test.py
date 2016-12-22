from Agent import Agent
from Obstacles import Obstacle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from math import exp

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.set_xlim([-5,5])
ax1.set_ylim([-5,5])


agent1 = Agent((0,0),1)
agent2 = Agent((-3,1),1)
agent3 = Agent((0,2),1)
agent4 = Agent((2,2),1)

agents = []
agents.append(agent1)
agents.append(agent2)
agents.append(agent3)
agents.append(agent4)

agent1.speed = (-2,2)
agents = []
agents.append(agent1)
agents.append(agent2)

obstacles = []
obstacle1= Obstacle((-2,2),4,1)
obstacle2= Obstacle((2,-2),1,4)
obstacle3= Obstacle((-3,-3),4,1)
obstacle4= Obstacle((-3,-3),1,4)

obstacles.append(obstacle1)
obstacles.append(obstacle2)
obstacles.append(obstacle3)
#obstacles.append(obstacle4)

agents = agent1.update_position(agents, obstacles, 1)


for obstacle in obstacles:
    ax1.add_patch(patches.Rectangle(obstacle.position,obstacle.width,obstacle.height))


for agent in agents:
    print agent
    colour = min(exp(sum(agent.colour_agents.itervalues())+sum(agent.colour_obstacles.itervalues())-2),1)
    ax1.add_patch(patches.Circle(agent.position,agent.size,color=[colour,0,0]))

plt.show()