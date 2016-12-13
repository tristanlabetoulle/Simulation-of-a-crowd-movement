from PriorityQueue import PriorityQueue
from GridGraph import GridGraph
from Obstacles import Obstacle
from FastMarching import *
from Agent import *

import numpy;

from pylab import imshow,show


precision = 0.5; #nodes per unity
horizontal_size = 100;
vertical_size = 100;

exit = (10,10);

obstacles = []
obstacle1 = Obstacle((70,0),10,70)
obstacle2 = Obstacle((80,60),18,10)
obstacles.append(obstacle1)
obstacles.append(obstacle2)

agents = []
agent1 = Agent((10,80))

Graph = GridGraph(horizontal_size,vertical_size,precision)

Graph.update_map_obstales(obstacles)

weights = fast_marching_method(Graph, Graph.to_node(agent1.position),Graph.to_node(exit))
imshow(weights)
show()

agent1.update_speed(weights, Graph)
