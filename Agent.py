
from numpy.linalg import norm
from numpy import dot,array
from Obstacles import Obstacle

from math import exp

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
        self.size = size
        self.navigation_map = None
        self.pressure = 0
        self.pressure_scenery = False
        self.pressure_interaction = {}
        self.has_reached_exit = False
        
    def __equals__(self,other):
        return self.position == other.position
    
    def __repr__(self):
        return 'Agent '+str(self.position)+' '+str(self.speed)+' '+str(self.size)
        
    def update_speed(self,agents,obstacles):
        
        position_node = self.navigation_map.to_node(self.position)
        neighbours = self.navigation_map.get_neighbours(position_node);
        if 'y-1' in neighbours :
            if 'y+1' in neighbours:
                if (self.navigation_map.distances[neighbours['y-1']]>self.navigation_map.distances[neighbours['y+1']]):
                    sign_y = 1
                else:
                    sign_y = -1
                diff_y = max(max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['y-1']],self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['y+1']]),0);
            else :
                sign_y = -1
                diff_y = max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['y-1']],0);
        else :
            if 'y+1' in neighbours:
                sign_y = 1
                diff_y = max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['y+1']],0);
        if 'x-1' in neighbours:
            if 'x+1' in neighbours:
                if self.navigation_map.distances[neighbours['x-1']]>self.navigation_map.distances[neighbours['x+1']]:
                    sign_x = 1
                else :
                    sign_x = -1
                diff_x = max(max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['x-1']],self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['x+1']]),0);
            else :
                sign_x = -1
                diff_x = max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['x-1']],0);
        else :
            if 'x+1' in neighbours:
                sign_x = 1
                diff_x = max(self.navigation_map.distances[position_node]-self.navigation_map.distances[neighbours['x+1']],0);
        self.speed = (diff_x*sign_x,diff_y*sign_y)
        if self.speed!=(0,0):
            self.speed = (diff_x*sign_x/(diff_y**2+diff_x**2)**0.5,diff_y*sign_y/(diff_y**2+diff_x**2)**0.5)
            
        for obstacle in obstacles:
            DL = array(obstacle.position)
            UL = array((obstacle.position[0],obstacle.position[1]+obstacle.height))
            UR = array((obstacle.position[0]+obstacle.width,obstacle.position[1]+obstacle.height))
            DR = array((obstacle.position[0]+obstacle.width,obstacle.position[1]))
            corners = [DL,UL,UR,DR]
            
            for corner in corners:
                X = array(self.position)
                #print dot(X-corner,X-corner)**0.5,X
                if round(dot(X-corner,X-corner)**0.5,3)==self.size:
                    speed = array((-X[1]+corner[1],X[0]-corner[0]))
                    speed = speed/(dot(speed,speed)**0.5)
                    if dot(speed,self.speed)<0:
                        self.speed = tuple(-speed)
                    else:
                        self.speed = tuple(speed)
        
        if not self.pressure_scenery:
            U = array(self.speed)
            X = array(self.position)
            for agent in agents:
                if agent!=self:
                    X2 = array(agent.position)
                    distance_agents = dot(X-X2,X-X2)**0.5
                    direction=(X-X2)/(dot(X-X2,X-X2)**0.5)
                    sigma = 3
                    U=U+1*exp(-(distance_agents-self.size-agent.size)**2/(2*float(sigma)**2))*direction
            self.speed = tuple(U)
        
    def update_position(self,agents,obstacles,exits,dt,size_scene):
        
        def time_calculus_points(X,X2,U,r):
            A = dot(U,U)
            B = 2*(dot(X,U)-dot(X2,U))
            C = dot(X-X2,X-X2)-(r)**2
            DELTA2 = B**2-4*A*C
            if round(DELTA2,3)>0 and (-B-DELTA2**0.5)/(2*A)>=0 :#because of floating errors
                return (-B-DELTA2**0.5)/(2*A)
            else:
                return float('inf')
        
        def update_time_move_scenery(time_move,objects,dt,type_object):

            for i in range(len(objects)) :
                dl = objects[i].position
                ul = (objects[i].position[0],objects[i].position[1]+objects[i].height)
                ur = (objects[i].position[0]+objects[i].width,objects[i].position[1]+objects[i].height)
                dr = (objects[i].position[0]+objects[i].width,objects[i].position[1])
                
                time_move_right = float('inf')
                time_move_up = float('inf')
                if self.speed[0]!=0:
                    if self.speed[0]>0:
                        sign_ = 1
                    else:
                        sign_ = -1
                    time_move_right = min((dl[0]-sign_*self.size-self.position[0])/float(self.speed[0]),(dr[0]-sign_*self.size-self.position[0])/float(self.speed[0]))
                    if time_move_right<0:
                        time_move_right = float('inf')
                if self.speed[1]!=0:
                    if self.speed[1]>0:
                        sign_ = 1
                    else:
                        sign_ = -1
                    time_move_up = min((dl[1]-sign_*self.size-self.position[1])/float(self.speed[1]),(ul[1]-sign_*self.size-self.position[1])/float(self.speed[1]))
                    if time_move_up<0:
                        time_move_up = float('inf')
                
                if self.position[1]+self.speed[1]*time_move_right>=dl[1] and self.position[1]+self.speed[1]*time_move_right<=ul[1]:
                    new_time_move = time_move_right
                    direction_conflict=(1,0)
                elif self.position[0]+self.speed[0]*time_move_up>=dl[0] and self.position[0]+self.speed[0]*time_move_up<=dr[0]:
                    new_time_move = time_move_up
                    direction_conflict=(0,1)
                else:
                    X = array(self.position)
                    U = array(self.speed)
                    r = self.size
                    X2 = array(dl)
                    time_edge_1 = time_calculus_points(X, X2, U, r)
                    X2 = array(ul)
                    time_edge_2 = time_calculus_points(X, X2, U, r)
                    X2 = array(ur)
                    time_edge_3 = time_calculus_points(X, X2, U, r)
                    X2 = array(dr)
                    time_edge_4 = time_calculus_points(X, X2, U, r)
                    new_time_move = time_edge_1
                    direction_conflict=tuple((array(dl)-X)/norm(array(dl)-X))
                    if time_edge_2<new_time_move:
                        new_time_move = time_edge_2
                        direction_conflict=tuple((array(ul)-X)/norm(array(ul)-X))
                    if time_edge_3<new_time_move:
                        new_time_move = time_edge_3
                        direction_conflict=tuple((array(ur)-X)/norm(array(ur)-X))
                    if time_edge_4<new_time_move:
                        new_time_move = time_edge_4
                        direction_conflict=tuple((array(dr)-X)/norm(array(dr)-X))
                        
                if new_time_move<time_move:
                    time_move = new_time_move
                    if type_object=='exit':
                        self.has_reached_exit = True
                    else:
                        pressure = dt-time_move
                        U = array(self.speed)
                        self.pressure = abs(pressure*dot(U,direction_conflict))
                        self.pressure_scenery = True
                elif new_time_move==time_move:
                    pressure = dt-time_move
                    U = array(self.speed)
                    self.pressure = self.pressure + abs(pressure*dot(U,direction_conflict))
            
            return time_move
                    
        
        
        def update_time_move_agents(time_move,agents,dt):

            for agent in agents:
                if agent!=self:
                    X = array(self.position)
                    X2 = array(agent.position)
                    U = array(self.speed)
                    r1 = self.size
                    r2 = agent.size
                    if norm(X-X2)<r1+r2+dt*norm(U):
                        A = dot(U,U)
                        B = 2*(dot(X,U)-dot(X2,U))
                        C = dot(X-X2,X-X2)-(r1+r2)**2
                        DELTA2 = B**2-4*A*C
                        if DELTA2>0:
                            sol = (-B-DELTA2**0.5)/(2*A)
                            if round(sol,3)>=0 and sol<=time_move:
                                if sol<time_move:
                                    time_move = sol
                                    self.pressure = 0
                                pressure = dt-time_move
                                self.pressure_interaction[agent] = abs(pressure*dot(U,X2-X)/norm(X2-X))
                                agent.pressure_interaction[self] = abs(pressure*dot(U,X2-X)/norm(X2-X))
        
            return time_move
        
        for agent in self.pressure_interaction:
            del agent.pressure_interaction[self]
        self.pressure_interaction = {}
        self.pressure = 0
        self.pressure_scenery = False
            
        time_move = dt
        boundaries = [Obstacle((-1,0),1,size_scene[1]),Obstacle((0,size_scene[1]),size_scene[0],1),Obstacle((size_scene[0],0),1,size_scene[1]),Obstacle((0,-1),size_scene[0],1)]
        time_move = update_time_move_scenery(time_move, boundaries, dt,'boundary')
        time_move = update_time_move_scenery(time_move, obstacles, dt,'obstacle')
        
        time_move = update_time_move_agents(time_move, agents, dt)
        
        time_move = update_time_move_scenery(time_move, exits, dt,'exit')#the order is important, we check finally if the closest thing is the exit cf line 154
        
        U = array(self.speed)
        X =array(self.position)
        self.position = tuple(X+time_move*U)
            
    def get_color_agent(self):
        return min(exp(self.pressure+sum(self.pressure_interaction.itervalues())-1),1)
                