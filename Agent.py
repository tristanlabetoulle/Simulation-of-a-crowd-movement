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
        self.size = size
        self.colour_agents = {}
        self.colour_obstacles = {}
        
    def __equals__(self,other):
        return self.position == other.position
    
    def __repr__(self):
        return 'Agent '+str(self.position)+' '+str(self.speed)+' '+str(self.size)
        
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
        
        def update_time_move_obstacles(time_move,obstacles,agents,dt):
            index_conflict_obstacles = []
            direction_conflict_obstacles = {}
            for i in range(len(obstacles)) :
                dl = obstacles[i].position
                ul = (obstacles[i].position[0],obstacles[i].position[1]+obstacles[i].height)
                ur = (obstacles[i].position[0]+obstacles[i].width,obstacles[i].position[1]+obstacles[i].height)
                dr = (obstacles[i].position[0]+obstacles[i].width,obstacles[i].position[1])
                
                new_time_move = float('inf')
                
                if self.speed[0]>=0:
                    if self.speed[1]>=0:
                        if self.speed[0]:
                            time_move_right = (dl[0]-self.size-self.position[0])/float(self.speed[0])
                        else:
                            time_move_right = float('inf')
                        if self.speed[1]:
                            time_move_up = (dl[1]-self.size-self.position[1])/float(self.speed[1])
                        else:
                            time_move_up = float('inf')
                            
                        if time_move_up>=0 and time_move_up<=new_time_move:
                            new_time_move = time_move_up
                            direction_conflict_obstacles[i]=(0,1)
                        if time_move_right>=0 and time_move_right<=new_time_move:
                            new_time_move = time_move_right
                            direction_conflict_obstacles[i]=(1,0)
                    else:
                        if self.speed[0]:
                            time_move_right = (ul[0]-self.size-self.position[0])/float(self.speed[0])
                        else:
                            time_move_right = float('inf')
                        time_move_down = (ul[1]+self.size-self.position[1])/float(self.speed[1])
                        
                        if time_move_down>=0 and time_move_down<=new_time_move:
                            new_time_move = time_move_down
                            direction_conflict_obstacles[i]=(0,-1)
                        if time_move_right>=0 and time_move_right<=new_time_move:
                            new_time_move = time_move_right
                            direction_conflict_obstacles[i]=(1,0)
                else:
                    if self.speed[1]>=0:
                        time_move_left = (dr[0]+self.size-self.position[0])/float(self.speed[0])
                        if self.speed[1]:
                            time_move_up = (dr[1]-self.size-self.position[1])/float(self.speed[1])
                        else:
                            time_move_up = float('inf')
                        if time_move_up>=0 and time_move_up<=new_time_move:
                            new_time_move = time_move_up
                            direction_conflict_obstacles[i]=(0,1)
                        if time_move_left>=0 and time_move_left<=new_time_move:
                            new_time_move = time_move_left
                            direction_conflict_obstacles[i]=(-1,0)
                    else:
                        time_move_left = (ur[0]+self.size-self.position[0])/float(self.speed[0])
                        time_move_down = (ur[1]+self.size-self.position[1])/float(self.speed[1])
                        
                        if time_move_down>=0 and time_move_down<=new_time_move:
                            new_time_move = time_move_down
                            direction_conflict_obstacles[i]=(0,-1)
                        if time_move_left>=0 and time_move_left<=new_time_move:
                            new_time_move = time_move_left
                            direction_conflict_obstacles[i]=(-1,0)
                
                if new_time_move<time_move:
                    index_conflict_obstacles = []
                    index_conflict_obstacles.append(i)
                    temp = direction_conflict_obstacles[i]
                    direction_conflict_obstacles = {}
                    direction_conflict_obstacles[i]=temp
                    time_move = new_time_move
                elif new_time_move==time_move:
                    index_conflict_obstacles.append(i)
            
            index_agent = agents.index(self)
            agents[index_agent].colour_obstacles={}
            for i in index_conflict_obstacles:
                pressure = dt-time_move
                U = array(self.speed)
                print 'aa'
                print pressure*dot(U,direction_conflict_obstacles[i])
                agents[index_agent].colour_obstacles[i] = pressure*dot(U,direction_conflict_obstacles[i])
            return time_move,agents
        
        def update_time_move_agents(time_move,agents,dt):
            index_time_move = []
            for i in range(len(agents)):
                if agents[i]!=self:
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
            
            index_agent = agents.index(self)
            agents[index_agent].colour_agents = {}
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
                agents[index].colour_agents[index_agent] = pressure*dot(U,X2-X)/norm(X2-X)
                agents[index_agent].colour_agents[index] = pressure*dot(U,X2-X)/norm(X2-X)
        
            return time_move,agents
        
        time_move = dt
        time_move,agents = update_time_move_obstacles(time_move, obstacles,agents, dt)
        time_move,agents = update_time_move_agents(time_move, agents, dt)
        
        index_agent = agents.index(self)
        U = array(self.speed)
        X =array(self.position)
        agents[index_agent].position = tuple(X+time_move*U)
        
        return agents