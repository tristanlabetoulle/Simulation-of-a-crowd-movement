from GridGraph import GridGraph
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
        #print neighbours
        #print 'u',weights[neighbours['up']],'d',weights[neighbours['down']],'l',weights[neighbours['left']],'r',weights[neighbours['right']]
        if 'up' in neighbours :
            if 'down' in neighbours:
                if (weights[neighbours['up']]>weights[neighbours['down']]):
                    sign_x1 = 1
                else:
                    sign_x1=-1
                x1 = min(weights[neighbours['up']],weights[neighbours['down']]);
            else :
                sign_x1 = -1
                x1 = weights[neighbours['up']];
        else :
            if 'down' in neighbours:
                sign_x1 = 1
                x1 = weights[neighbours['down']];
        if 'left' in neighbours:
            if 'right' in neighbours:
                if weights[neighbours['left']]>weights[neighbours['right']]:
                    sign_x2 = 1
                else :
                    sign_x2 = -1
                x2 = min(weights[neighbours['left']],weights[neighbours['right']]);
            else :
                sign_x2 = -1
                x2 = weights[neighbours['left']];
        else :
            if 'right' in neighbours:
                sign_x2 = 1
                x2 = weights[neighbours['right']];
        if abs(x1-x2)<1 :
            alpha = 0.5+abs(x2-x1)/(2*(2-abs(x2-x1)**2)**0.5)
            if x1>x2 :
                self.speed = (alpha*sign_x1,(1-alpha)*sign_x2)
            else :
                self.speed = ((1-alpha)*sign_x1,alpha*sign_x2)
        else:
            if x1>x2:
                self.speed = (sign_x1,0)
            else:
                self.speed = (0,sign_x2)
        #print self.speed