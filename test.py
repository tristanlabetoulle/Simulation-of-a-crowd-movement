from PriorityQueue import PriorityQueue
from GridGraph import GridGraph
from Obstacles import Obstacle
from FastMarching import *
from Agent import *

import numpy;
import matplotlib.pyplot as plot;

from pylab import imshow,show

def calculation_vector(position,weights,graph):
    neighbours = graph.get_neighbours(position);
    if 'i-1' in neighbours :
        if 'i+1' in neighbours:
            if (weights[neighbours['i-1']]>weights[neighbours['i+1']]):
                sign_x1 = 1
            else:
                sign_x1=-1
            diffy = max(max(weights[position]-weights[neighbours['i+1']],weights[position]-weights[neighbours['i-1']]),0)
        else :
            sign_x1 = -1
            diffy = max(weights[position]-weights[neighbours['i-1']],0);
    else :
        if 'i+1' in neighbours:
            sign_x1 = 1
            diffy = max(weights[position]-weights[neighbours['i+1']],0);
        else:
            sign_x1 = 0
            diffy = 0
    if 'j-1' in neighbours:
        if 'j+1' in neighbours:
            if weights[neighbours['j-1']]>weights[neighbours['j+1']]:
                sign_x2 = 1
            else :
                sign_x2 = -1
            diffx = max(max(weights[position]-weights[neighbours['j-1']],weights[position]-weights[neighbours['j+1']]),0)
        else :
            sign_x2 = -1
            diffx = max(weights[position]-weights[neighbours['j-1']],0);
    else :
        if 'j+1' in neighbours:
            sign_x2 = 1
            diffx = max(weights[position]-weights[neighbours['j+1']],0);
        else:
            sign_x2 = 0
            diffx = 0
    res = (diffx*sign_x2,diffy*sign_x1)
    return res


hh = 100
vv = 100


obstacles = []
obstacle1 = Obstacle((0,70),10,70)
obstacle2 = Obstacle((60,80),18,10)
obstacles.append(obstacle1)
obstacles.append(obstacle2)

agents = []
agent1 = Agent((80,15))

precision = 0.1

Graph = GridGraph(hh,vv,precision)

Graph.update_map_obstales(obstacles)

exit = (10,80)

weights = fast_marching_method(Graph, Graph.to_node(agent1.position),Graph.to_node(exit))
imshow(weights)
print weights
print 'aa'
show()
X,Y = numpy.meshgrid(numpy.arange(0,int(hh*precision),1),numpy.arange(0,int(vv*precision),1))
W = X*X+Y*Y

U = X.astype(float)
V = X.astype(float)
for i in range(int(hh*precision)):
    for j in range(int(vv*precision)):
        U[i,j]=1
        V[i,j]=1
plot.gca().invert_yaxis()

plot.quiver(X,Y,U,V)
show()
print U,V