from pylab import *
import numpy
from Obstacles import Obstacle
from GridGraph import GridGraph

# the x distribution will be centered at -1, the y distro
# at +1 with twice the width.
x = numpy.random.randn(3000)-1
y = numpy.random.randn(3000)*2+1

hist,xedges,yedges = numpy.histogram2d(x,y,bins=40,range=[[-6,4],[-4,6]])
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1] ]
imshow(hist.T,extent=extent,interpolation='nearest',origin='lower')
colorbar()
#show()

#obstacle1 = Obstacle((30,0),5,5)
#obstacles = []
#obstacles.append(obstacle1)
#grid = GridGraph(200,100,0.5)
#grid.update_map_obstales(obstacles)

print float('inf')-float('inf')>=0