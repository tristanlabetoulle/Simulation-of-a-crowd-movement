from Obstacles import Obstacle
from FastMarching import fast_marching_method
from Agent import Agent
from Exits import Exit
from GridGraph import GridGraph

import matplotlib.patches as patches

import numpy;
import matplotlib.pyplot as plot;

from pylab import imshow,show

def update_agents():
    
    precision = 1#nodes per unity
    Graph = GridGraph(horizontal_size,vertical_size,precision)
    
    
    pick_agent = numpy.random.randint(len(agents),size = len(agents))
    for i in pick_agent:
        Graph.prepare_graph_for_agent(obstacles,exits,agents[i])
        distances = fast_marching_method(Graph, Graph.to_node(agents[i].position))
        fig1 = plot.figure()
        ax1 = fig1.add_subplot(111, aspect='equal')
        ax1.set_xlim([-0.5/float(precision),horizontal_size+0.5/float(precision)])
        ax1.set_ylim([-0.5/float(precision),vertical_size+0.5/float(precision)])
        
        for obstacle in obstacles:
            ax1.add_patch(patches.Rectangle((obstacle.position[0]-0.5,obstacle.position[1]-0.5),obstacle.width+1,obstacle.height+1))
        
        imshow(distances,origin='lower',extent=[-0.5/float(precision),horizontal_size+0.5/float(precision),-0.5/float(precision),vertical_size+0.5/float(precision)],interpolation="nearest")
        #show()
        for j in range(40):
            ax1.add_patch(patches.Circle(agents[i].position,agents[i].size))
            print agents[i].position,i
            agents[i].update_speed(distances, Graph)
            if agents[i].reached_exit(exits,dt):
                
                print j,'finito'
                del agents[i]
            else:
                agents[i].update_position(agents,obstacles,exits,dt)
        
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
obstacle2 = Obstacle((60,80),18,10)
obstacle3 = Obstacle((40,10),60,10)
obstacles.append(obstacle1)
obstacles.append(obstacle2)
obstacles.append(obstacle3)

agents = []
agent1 = Agent((65,63),3)
agents.append(agent1)


time_simulation = 10

dt = 1

for i in range(int(time_simulation/float(dt))):
    update_agents()

