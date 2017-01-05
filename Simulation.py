from Obstacle import Obstacle
from Exit import Exit
from GridGraph import GridGraph
from FastMarching import fast_marching_method
from Agent import Agent

import numpy as numpy

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib import animation
from pylab import show,imshow

import os
from os import startfile

def example_simulation():
    
    size_scene = (100,100)#size_scene[0]==horizontal and size_scene[1]==vertical
    
    obstacles = [Obstacle((70,40),10,60),Obstacle((20,50),50,10),Obstacle((30,10),10,40)]
    
    exits = [Exit((85,99),10,2)]

    # warning, the size must be chosen as an integer, agent.size*precision must preferably be an integer to improve speed
    agents = [Agent((10,90),1),Agent((10,80),1),Agent((10,70),1),Agent((10,60),2),Agent((10,50),2),Agent((10,40),2)
              ,Agent((10,30),2),Agent((10,20),2),Agent((10,10),2),Agent((14,90),2),Agent((14,80),2),Agent((14,70),2)
              ,Agent((14,60),2),Agent((14,50),2),Agent((14,40),2),Agent((14,30),2),Agent((14,20),2),Agent((14,10),4)
              ]

    time_simulation = 40 #in seconds
    dt = .1 # in seconds

    launch_simulation(size_scene,obstacles,exits,agents,time_simulation,dt)
    
def launch_simulation(size_scene,obstacles,exits,agents,time_simulation,dt):
    
    history_agents = []
    
    print "Initialization of the agents..."
    #create navigation field for each agent
    precision = 0.5#nodes per unity
    
    navigation_maps = {}
    
    for agent in agents:
        if agent.size not in navigation_maps:
            debug_precision = precision
            #to make sure that precision*agent.size is an integer
            if not precision*agent.size==int(precision*agent.size):
                debug_precision = 1
            graph = GridGraph(size_scene,debug_precision)
            graph.prepare_graph_for_fast_marching(obstacles,exits,agent)
            fast_marching_method(graph, graph.to_node(agent.position))
            navigation_maps[agent.size] = graph
            #shows the distance map to the exit after applying the fast marching method
            #imshow(graph.distances,interpolation='nearest',origin='lower')
            #show()
    for agent in agents:
        agent.navigation_map = navigation_maps[agent.size]
        
    
    loading_bar = 0
    print "Simulation running..."
    
    #start simulation
    for t in range(int(time_simulation/dt)):
        
        #loading bar
        if int(t/float(int(time_simulation/dt))*100)==loading_bar:
            print "#",
            loading_bar = loading_bar+10
        
        #initialize patches for the agents for one frame of the animation
        patches_agents = []
        
        numpy.random.seed(1)
        pick_agent = numpy.random.choice(len(agents),len(agents),replace=False)
        for i in pick_agent:
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
    
    print ''
    print 'Simulation finished at time '+str((t+1)*dt)+'s'
    
    display_simulation(history_agents, obstacles, exits, size_scene,dt,3)
    
def display_simulation(history_agents,obstacles, exits, size_scene,dt,speed):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim([0,size_scene[0]])
    ax.set_ylim([0,size_scene[1]])

    for obstacle in obstacles:
        ax.add_patch(patches.Rectangle((obstacle.position[0],obstacle.position[1]),obstacle.width,obstacle.height))

    for exit_ in exits:
        ax.add_patch(patches.Rectangle((exit_.position[0],exit_.position[1]),exit_.width,exit_.height,color='black'))
    
    def init():
        for i in range(len(history_agents)):
            for j in range(len(history_agents[i])):
                history_agents[i][j].set_visible(False)
        return []

    def animate(i):
        patches = []
        if i>0:
            for j in range(len(history_agents[i-1])):
                history_agents[i-1][j].set_visible(False)
        for j in range(len(history_agents[i])):
            history_agents[i][j].set_visible(True)
            patches.append(ax.add_patch(history_agents[i][j]))
        return patches
    
    
    #interval doesn't work
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(history_agents), interval=dt*1000/float(speed))
    
    def save_simulation():
        print "Saving the simulation..."
        
        # Set up formatting for the movie files
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=1/float(dt)*speed, metadata=dict(artist='Me'), bitrate=1800)

        filename = os.path.dirname(__file__)+'\Videos\simulation.mp4'
        
        anim.save(filename, writer)
        startfile(filename)
    
    save_simulation()
    
    print 'Simulation saved.'
    
example_simulation()