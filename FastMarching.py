from PriorityQueue import PriorityQueue
import numpy;

def fast_marching_method(Graph,start,goal):
    
    h = 1
    
    def calculus_distance(node,Graph,weights):
        neighbours = Graph.get_neighbours(node);
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
        
    def heuristic(node,goal):
        #return ((node[0]-goal[0])**2+(node[1]-goal[1])**2)**0.5*h
        return 0
    
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

#X,Y = meshgrid(numpy.linspace(0,precision-1,precision),numpy.linspace(0,precision-1,precision))
#plt.scatter(X,Y,c=weights,s=1000)
