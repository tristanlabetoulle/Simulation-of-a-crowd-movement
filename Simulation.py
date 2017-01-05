from Obstacles import Obstacle
from FastMarching import fast_marching_method
from Agent import Agent
from Exits import Exit
from GridGraph import GridGraph

import matplotlib.patches as patches

from matplotlib import animation

import numpy;
import matplotlib.pyplot as plot;

from pylab import imshow,show

from math import exp

def create_plot():
    fig1 = plot.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([0,horizontal_size])
    ax1.set_ylim([0,vertical_size])

    for obstacle in obstacles:
        ax1.add_patch(patches.Rectangle((obstacle.position[0],obstacle.position[1]),obstacle.width,obstacle.height))

    for exit in exits:
        ax1.add_patch(patches.Rectangle((exit.position[0],exit.position[1]),exit.width,exit.height,color='black'))
    return fig1,ax1

def update_agents(time_simulation,dt,agents):
    
    history_agents = []
    
    precision = 1#nodes per unity
    Graph = GridGraph(horizontal_size,vertical_size,precision)
    
    for agent in agents:
        Graph.prepare_graph_for_agent(obstacles,exits,agent)
        agent.navigation_map = fast_marching_method(Graph, Graph.to_node(agent.position))
    
    
    
    for t in range(int(time_simulation/dt)):
        
        #fig,ax = create_plot()
        
        patches_agents = []
        numpy.random.seed(0)
        pick_agent = numpy.random.choice(len(agents),len(agents),replace=False)
        delete=[]
        for i in range(len(agents)):
            print agents,i
            agents[i].update_speed(agents[i].navigation_map, Graph,agents)
            if agents[i].reached_exit(exits,dt):        
                delete.append(i)
            else:
                agents[i].update_position(agents,obstacles,exits,dt)
                #print (agents[1].position[0]-agents[2].position[0])**2+(agents[1].position[1]-agents[2].position[1])**2
                #ax.add_patch(patches.Circle(agents[i].position,agents[i].size))
                colour = min(exp(sum(agents[i].colour_agents.itervalues())+sum(agents[i].colour_obstacles.itervalues())-1),1)
                patches_agents.append(patches.Circle(agents[i].position,agents[i].size,color=[colour,0,0]))
        
        agents = [v for i, v in enumerate(agents) if i not in delete]
        #show()
        if not agents:
            print 'finished'
            break;
        
        history_agents.append(patches_agents)
    
    fig,ax = create_plot()
    
    def init():
    # initialize an empty list of cirlces
        return []

    def animate(i):
    # draw circles, select to color for the circles based on the input argument i.
        patches = []
        for j in range(len(history_agents[i])):
             patches.append(ax.add_patch(history_agents[i][j]))
        print i
        return history_agents[i]

    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(history_agents), interval=25, blit=True)
    show()    

horizontal_size = 100;
vertical_size = 100;

exits = []
exit = Exit((80,100),20,1)
#exit2 = Exit((80,80),5,1)
exits.append(exit)
#exits.append(exit2)

obstacles = []
obstacle1 = Obstacle((70,40),10,60)
obstacle2 = Obstacle((40,50),50,10)
obstacle3 = Obstacle((40,10),60,10)
obstacles.append(obstacle1)
#obstacles.append(obstacle2)
obstacles.append(obstacle3)

agents = []
agent1 = Agent((20,60),3)
agent2 = Agent((10,40),3)
agent3 = Agent((10,20),3)
agent4 = Agent((10,30),3)
agent5 = Agent((10,70),3)
agent6 = Agent((10,80),3)
agents.append(agent1)
agents.append(agent2)
agents.append(agent3)
agents.append(agent4)
agents.append(agent5)
agents.append(agent6)


time_simulation = 200

dt = 2


        

update_agents(time_simulation,dt,agents)

show()
