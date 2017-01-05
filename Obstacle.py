
class Obstacle():


    def __init__(self, position,width,height):

        self.position=position
        self.width=width
        self.height=height
        
    def __repr__(self):
        return 'Obstacle'+'\n'+'DL:'+str(self.position)+'DR:'+str((self.position[0]+self.width,self.position[1]))+'UR:'+str((self.position[0]+self.width,self.position[1]+self.height))+'UL:'+str((self.position[0]+self.width,self.position[1]))
        
    