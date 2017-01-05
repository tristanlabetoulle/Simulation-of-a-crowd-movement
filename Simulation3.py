from Obstacles import Obstacle
from Exits import Exit
from GridGraph import GridGraph
from FastMarching import fast_marching_method
from Agent import Agent

import numpy as numpy

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib import animation
from pylab import show,imshow

def example_simulation():
    
    size_scene = (100,100)#size_scene[0]==horizontal and size_scene[1]==vertical
    
    obstacle1 = Obstacle((70,40),10,60)
    obstacle2 = Obstacle((24,50),50,10)
    obstacle3 = Obstacle((30,10),10,40)
    obstacles = [obstacle1,obstacle2]
    
    exit = Exit((80,80),10,1)
    exits = [exit]

    agent1 = Agent((17,60),2)# warning, the size must be chosen so that precision*size is integer
    agent2 = Agent((10,40),2)
    agent3 = Agent((10,20),2)
    agent4 = Agent((10,30),2)
    agent5 = Agent((10,70),2)
    agent6 = Agent((10,80),2)
    agents = [agent1,agent2,agent4,agent5,agent6]
    agents = [Agent((10,90),2),Agent((10,80),2),Agent((10,70),2),Agent((10,60),2),Agent((10,50),2),Agent((10,40),2)
              ,Agent((10,30),2),Agent((10,20),2),Agent((10,10),2),Agent((14,90),2),Agent((14,80),2),Agent((14,70),2)
              ,Agent((14,60),2),Agent((14,50),2),Agent((14,40),2),Agent((14,30),2),Agent((14,20),2),Agent((14,10),2)
            
              ]

    time_simulation = 200 #in seconds
    dt = 1 # in seconds

    launch_simulation(size_scene,obstacles,exits,agents,time_simulation,dt)
    
def launch_simulation(size_scene,obstacles,exits,agents,time_simulation,dt):
    
    history_agents = []
    
    #create navigation field for each agent
    precision = 0.5#nodes per unity
    graph = GridGraph(size_scene,precision)
    for agent in agents:
        graph.prepare_graph_for_fast_marching(obstacles,exits,agent)
        fast_marching_method(graph, graph.to_node(agent.position))
        agent.navigation_map = graph
        imshow(graph.distances,interpolation='nearest',origin='lower')
        
    show()
    gggg = agents[13]
    #start simulation
    for t in range(int(time_simulation/dt)):
        
        #initialize patches for the agents for one frame of the animation
        patches_agents = []
        #
        
        print gggg,gggg.pressure_scenery
        pick_agent = numpy.random.choice(len(agents),len(agents),replace=False)
        for i in range(len(agents)):
            #update the speed of the agent
            
            agents[i].update_speed(agents,obstacles)
            #update the position of the agent
            agents[i].update_position(agents,obstacles,exits,dt,size_scene)
            
            #add patch of the agent for one frame
            patches_agents.append(patches.Circle(agents[i].position,agents[i].size,color=[agents[i].get_color_agent(),0,0]))
            #
        
        history_agents.append(patches_agents)
        
        agents = [v for i, v in enumerate(agents) if not v.has_reached_exit]
        
        if not agents:
            break;
    
    print 'Simulation finished at time '+str((t+1)*dt)
    
    display_simulation(history_agents, obstacles, exits, size_scene)
    
def display_simulation(history_agents,obstacles, exits, size_scene):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim([0,size_scene[0]])
    ax.set_ylim([0,size_scene[1]])

    for obstacle in obstacles:
        ax.add_patch(patches.Rectangle((obstacle.position[0],obstacle.position[1]),obstacle.width,obstacle.height))

    for exit in exits:
        ax.add_patch(patches.Rectangle((exit.position[0],exit.position[1]),exit.width,exit.height,color='black'))
    
    def init():
        return []

    def animate(i):
        patches = []
        for j in range(len(history_agents[i])):
            patches.append(ax.add_patch(history_agents[i][j]))
        return patches
    
    #interval doesn't work
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(history_agents), interval=1, blit=True)
    show()
    
example_simulation()