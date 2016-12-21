from GridGraph import GridGraph
from numpy.linalg import norm
from numpy import dot,array

class Agent():
    '''
    classdocs
    '''


    def __init__(self, position,size):
        '''
        Constructor
        '''
        self.position = position
        self.speed = (0,0)
        self.size = 1
        self.colour = {}
        
    def __equals__(self,other):
        return self.position == other.position
    
    def __repr__(self):
        return 'Agent '+str(self.position)+' '+str(self.speed)+' '+str(self.size) + str(self.colour)
        
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
        
        def update_position_obstacles(self,obstacles,dt):
            for obstacle in obstacles :
                if self.speed[0]>0:
                    if self.speed[1]>0:
                        dx = obstacle.position[0]-self.position[0]
                        dy = obstacle.position[1]-self.position[1]
        
        def update_position_agents(self,agents,dt):
            time_move = dt
            index_time_move = []
            for i in range(len(agents)):
                if agents[i]==self:
                    index_self = i
                else:
                    X = array(self.position)
                    X2 = array(agents[i].position)
                    U = array(self.speed)
                    r1 = self.size
                    r2 = agents[i].size
                    if norm(X-X2)<r1+r2+dt*norm(U):
                        A = dot(U,U)
                        B = 2*(dot(X,U)-dot(X2,U))
                        C = dot(X-X2,X-X2)-(r1+r2)**2
                        DELTA2 = B**2-4*A*C
                        if DELTA2>0:
                            sol = (-B-DELTA2**0.5)/(2*A)
                            if sol>=0 and sol<=time_move:
                                if sol<time_move:
                                    index_time_move = []
                                    index_time_move.append(i)
                                    time_move = sol
                                else:
                                    index_time_move.append(i)
            for index in index_time_move:
                X = array(self.position)
                X2 = array(agents[index].position)
                U = array(self.speed)
                r1 = self.size
                r2 = agents[index].size
                A = dot(U,U)
                B = 2*(dot(X,U)-dot(X2,U))
                C = dot(X-X2,X-X2)-(r1+r2)**2
                DELTA2 = B**2-4*A*C
                pressure = dt-time_move
                agents[index].colour[index_self] = pressure*dot(U,X2-X)/norm(X2-X)
                agents[index_self].colour[index] = pressure*dot(U,X2-X)/norm(X2-X)
        
        
        
        
            self.position = tuple(X+time_move*U)
        
        return agents