import numpy

from pylab import show,imshow

class GridGraph:

    global OBSTACLE
    global EXIT
    OBSTACLE = 0
    EXIT = 2
        
    def __init__(self,size_scene,precision):
        self.precision = precision
        self.horizontal_size = int(size_scene[0]*precision)+1
        self.vertical_size = int(size_scene[1]*precision)+1
        self.indicator_map = numpy.ones((self.vertical_size,self.horizontal_size))
        self.distances = numpy.ones((self.vertical_size,self.horizontal_size))*float('inf')
    
    def get_neighbours(self,node):
        result = {};
        if node[1]<self.horizontal_size-1:
            result['x+1']=(node[0],node[1]+1);
        if node[1]>0:
            result['x-1']=(node[0],node[1]-1);
        if node[0]<self.vertical_size-1:
            result['y+1']=(node[0]+1,node[1]);
        if node[0]>0:
            result['y-1']=(node[0]-1,node[1]);
        return result;
    
    def to_node(self,coordinates):
        return (int(coordinates[1]*self.precision),int(coordinates[0]*self.precision))
    
    def prepare_graph_for_fast_marching(self,obstacles,exits,agent):
        for obstacle in obstacles:
            dl = (obstacle.position[0]-agent.size,obstacle.position[1]-agent.size)
            ur = (obstacle.position[0]+obstacle.width+agent.size,obstacle.position[1]+obstacle.height+agent.size)
            
            for x in range(self.to_node(dl)[0]+1,self.to_node(ur)[0]):
                for y in range(self.to_node(dl)[1]+1,self.to_node(ur)[1]):
                    if x>=0 and x<self.indicator_map.shape[0] and y>=0 and y<self.indicator_map.shape[1]:
                        self.indicator_map[x,y]=OBSTACLE
        for exit_ in exits:
            dl = (exit_.position[0],exit_.position[1])
            ur = (exit_.position[0]+exit_.width,exit_.position[1]+exit_.height)
            for x in range(self.to_node(dl)[0],self.to_node(ur)[0]+1):#we make sure the exit always exists by adding 1
                for y in range(self.to_node(dl)[1],self.to_node(ur)[1]+1):
                    if x>=0 and x<self.indicator_map.shape[0] and y>=0 and y<self.indicator_map.shape[1]:
                        self.indicator_map[x,y]=EXIT
                        