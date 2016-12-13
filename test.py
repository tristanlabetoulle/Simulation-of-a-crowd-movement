from pylab import *
import numpy

# the x distribution will be centered at -1, the y distro
# at +1 with twice the width.
x = numpy.random.randn(3000)-1
y = numpy.random.randn(3000)*2+1

hist,xedges,yedges = numpy.histogram2d(x,y,bins=40,range=[[-6,4],[-4,6]])
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1] ]
imshow(hist.T,extent=extent,interpolation='nearest',origin='lower')
colorbar()
show()

t={}
t['ss']=2
print 'ss' in t
