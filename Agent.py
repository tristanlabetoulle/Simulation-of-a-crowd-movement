from GridGraph import GridGraph
from numpy.dual import norm
class Agent():
    '''
    classdocs
    '''


    def __init__(self, position):
        '''
        Constructor
        '''
        self.position = position
        self.speed = (0,0)
        
    def update_speed(self,weights,graph):
        position_node = graph.to_node(self.position)
        neighbours = graph.get_neighbours(position_node);
        if 'y-1' in neighbours :
            if 'y+1' in neighbours:
                if (weights[neighbours['y-1']]>weights[neighbours['y+1']]):
                    sign_y = 1
                else:
                    sign_y = -1
                diff_y = max(max(weights[position_node]-weights[neighbours['y-1']],weights[position_node]-weights[neighbours['y+1']]),0);
            else :
                sign_y = -1
                diff_y = max(weights[position_node]-weights[neighbours['y-1']],0);
        else :
            if 'y+1' in neighbours:
                sign_y = 1
                diff_y = max(weights[position_node]-weights[neighbours['y+1']],0);
        if 'x-1' in neighbours:
            if 'x+1' in neighbours:
                if weights[neighbours['x-1']]>weights[neighbours['x+1']]:
                    sign_x = 1
                else :
                    sign_x = -1
                diff_x = max(max(weights[position_node]-weights[neighbours['x-1']],weights[position_node]-weights[neighbours['x+1']]),0);
            else :
                sign_x = -1
                diff_x = max(weights[position_node]-weights[neighbours['x-1']],0);
        else :
            if 'x+1' in neighbours:
                sign_x = 1
                diff_x = max(weights[position_node]-weights[neighbours['x+1']],0);
        self.speed = (diff_x*sign_x,diff_y*sign_y)
        if self.speed!=(0,0):
            self.speed = (diff_x*sign_x/(diff_y**2+diff_x**2)**0.5,diff_y*sign_y/(diff_y**2+diff_x**2)**0.5)
        
    def update_position(self,agents,obstacles,dt):
        
        
        self.position = (self.position[0]+dt*self.speed[0],self.position[1]+dt*self.speed[1])