import numpy

class GridGraph:
    
    def __init__(self,horizontal_size,vertical_size,precision):
        self.precision = precision
        self.horizontal_size = int(horizontal_size*precision)+1
        self.vertical_size = int(vertical_size*precision)+1
        self.map = numpy.ones((self.vertical_size,self.horizontal_size))
    
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
    
    def update_map_obstales(self,obstacles):
        for obstacle in obstacles:
            dl = obstacle.position
            ur = (obstacle.position[0]+obstacle.width,obstacle.position[1]+obstacle.height)
            self.map[self.to_node(dl)[0]:self.to_node(ur)[0]+1,self.to_node(dl)[1]:self.to_node(ur)[1]+1]=0
            #self.map[self.to_node(obstacle.position)[0]:self.to_node(obstacle.position)[0]+int(self.precision*obstacle.width)+1,self.to_node(obstacle.position)[1]:self.to_node(obstacle.position)[1]+int(self.precision*obstacle)+1]=0
        
