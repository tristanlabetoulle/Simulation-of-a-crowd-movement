from PriorityQueue import PriorityQueue
from GridGraph import GridGraph
from Obstacles import Obstacle

import numpy;

from pylab import imshow,show

precision = 1; #nodes per unity
horizontal_size = 100;
vertical_size = 100;

start = (1,1);
goal = (90,40);

obstacles = []
obstacle1 = Obstacle((70,0),10,70)
obstacle2 = Obstacle((80,60),18,10)
obstacles.append(obstacle1)
obstacles.append(obstacle2)

Graph = GridGraph(horizontal_size,vertical_size,precision)

Graph.update_map_obstales(obstacles)

def fast_marching_method(Graph,start,goal):
    
    def calculus_distance(node,Graph,weights):
        h=1;
        neighbours = Graph.get_neighbours(node);
        if 'up' in neighbours :
            if 'down' in neighbours:
                x1 = min(weights[neighbours['up']],weights[neighbours['down']]);
            else :
                x1 = weights[neighbours['up']];
        else :
            if 'down' in neighbours:
                x1 = weights[neighbours['down']];
        if 'left' in neighbours:
            if 'right' in neighbours:
                x2 = min(weights[neighbours['left']],weights[neighbours['right']]);
            else :
                x2 = weights[neighbours['left']];
        else :
            if 'right' in neighbours:
                x2 = weights[neighbours['right']];
        
        if 2*h**2-(x1-x2)**2>=0:
            return (x1+x2+(2*h**2-(x1-x2)**2)**0.5)/2
        else:
            return min(x1,x2)+h
        
    def heuristic(node,goal):
        return ((node[0]-goal[0])**2+(node[1]-goal[1])**2)**0.5
    
    frontier = PriorityQueue();
    weights = numpy.ones((Graph.vertical_size,Graph.horizontal_size))*float('inf');
    
    explored = []
    
    frontier.append([0,goal]);
    
    weights[goal] = 0
    
    while frontier:
        node = frontier.pop();
        explored.append(node[1])
        if node[1]==start:
            return weights
        neighbours = Graph.get_neighbours(node[1]);
        for neighbour in neighbours.itervalues():
            if neighbour not in explored and Graph.map[neighbour]:
                if not neighbour in frontier:
                    frontier.append([calculus_distance(neighbour,Graph,weights)+heuristic(neighbour, start),neighbour]);
                    weights[neighbour]=calculus_distance(neighbour,Graph,weights)
                elif weights[neighbour] > calculus_distance(neighbour,Graph,weights):
                    frontier[neighbour][0]=calculus_distance(neighbour,Graph,weights)+heuristic(neighbour, start);
                    weights[neighbour]=calculus_distance(neighbour,Graph,weights)
    return weights
        

weights = fast_marching_method(Graph, Graph.to_node(start),Graph.to_node(goal))
imshow(weights)

#X,Y = meshgrid(numpy.linspace(0,precision-1,precision),numpy.linspace(0,precision-1,precision))
#plt.scatter(X,Y,c=weights,s=1000)
show()