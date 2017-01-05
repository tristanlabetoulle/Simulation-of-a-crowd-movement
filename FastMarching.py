from PriorityQueue import PriorityQueue
import numpy;

from pylab import show,imshow

def fast_marching_method(graph,start):
    
    h = 1
    
    def calculus_distance(node,graph,weights):
        neighbours = graph.get_neighbours(node);
        if 'y-1' in neighbours :
            if 'y+1' in neighbours:
                x1 = min(weights[neighbours['y-1']],weights[neighbours['y+1']]);
            else :
                x1 = weights[neighbours['y-1']];
        else :
            if 'y+1' in neighbours:
                x1 = weights[neighbours['y+1']];
        if 'x-1' in neighbours:
            if 'x+1' in neighbours:
                x2 = min(weights[neighbours['x-1']],weights[neighbours['x+1']]);
            else :
                x2 = weights[neighbours['x-1']];
        else :
            if 'x+1' in neighbours:
                x2 = weights[neighbours['x+1']];
        
        if 2*h**2-(x1-x2)**2>=0:
            return (x1+x2+(2*h**2-(x1-x2)**2)**0.5)/2
        else:
            return min(x1,x2)+h
        
    
    frontier = PriorityQueue();
    weights = graph.distances;
    
    explored = []
    
    goals = numpy.where(graph.indicator_map==2)
    goals_x = goals[0]
    goals_y = goals[1]
    for i in range(goals_x.size):
        frontier.append([0,(goals_x[i],goals_y[i])])
        weights[(goals_x[i],goals_y[i])] = 0
    
       
    while frontier:
        node = frontier.pop();
        explored.append(node[1])
        #if node[1]==start:
        #   return weights
        neighbours = graph.get_neighbours(node[1]);
        for neighbour in neighbours.itervalues():
            if neighbour not in explored and graph.indicator_map[neighbour]:
                if not neighbour in frontier:
                    frontier.append([calculus_distance(neighbour,graph,weights),neighbour])
                    weights[neighbour]=calculus_distance(neighbour,graph,weights)
                elif weights[neighbour] > calculus_distance(neighbour,graph,weights):
                    frontier[neighbour][0]=calculus_distance(neighbour,graph,weights)
                    weights[neighbour]=calculus_distance(neighbour,graph,weights)
    graph.distances = weights
    
#X,Y = meshgrid(numpy.linspace(0,precision-1,precision),numpy.linspace(0,precision-1,precision))
#plt.scatter(X,Y,c=weights,s=1000)
