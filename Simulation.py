from Obstacles import Obstacle
from FastMarching import fast_marching_method
from Agent import *

import numpy;
import matplotlib.pyplot as plot;

from pylab import imshow,show


precision = 2; #nodes per unity
horizontal_size = 100;
vertical_size = 100;

exit = (90,90);

obstacles = []
obstacle1 = Obstacle((70,40),10,60)
obstacle2 = Obstacle((60,80),18,10)
obstacle3 = Obstacle((40,10),60,10)
obstacles.append(obstacle1)
obstacles.append(obstacle2)
obstacles.append(obstacle3)

agents = []
agent1 = Agent((55,80),1)
agents.append(agent1)

Graph = GridGraph(horizontal_size,vertical_size,precision)

Graph.update_map_obstales(obstacles)

weights = fast_marching_method(Graph, Graph.to_node(agent1.position),Graph.to_node(exit))
imshow(weights,origin='lower',extent=[0,horizontal_size,0,vertical_size])


dt = 2

positions = []


for i in range(100):
    
    
    agent1.update_speed(weights, Graph)
    agent1.update_position(agents,obstacles,dt)
    positions.append(agent1.position)

positions = numpy.array(positions)
print positions
axis = plot.gca()
axis.set_xlim([0,horizontal_size])
axis.set_ylim([0,vertical_size])
plot.scatter(positions[:,0],positions[:,1])
show()

