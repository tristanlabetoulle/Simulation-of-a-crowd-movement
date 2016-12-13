class GridGraph:
    
    def __init__(self,horizontal_size,vertical_size,precision):
        self.precision = precision
        self.horizontal_size = int(horizontal_size*precision)
        self.vertical_size = int(vertical_size*precision)
    
    def get_neighbours(self,node):
        result = {};
        if node[1]<self.horizontal_size-1:
            result['right']=(node[0],node[1]+1);
        if node[0]>0:
            result['up']=(node[0]-1,node[1]);
        if node[1]>0:
            result['left']=(node[0],node[1]-1);
        if node[0]<self.vertical_size-1:
            result['down']=(node[0]+1,node[1]);
        return result;
    
    def to_node(self,coordinates):
        return (int(coordinates[0]*self.precision),int(coordinates[1]*self.precision))
    
    
        
