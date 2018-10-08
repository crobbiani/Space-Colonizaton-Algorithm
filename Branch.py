from mathutils import Vector
import bpy
from copy import copy, deepcopy
def add(u, v):    
    return [a + b for a, b in zip(u, v)]


    
class Branch:
    
    def __init__(self,parent,pos,dir):
            self.pos = copy(pos)
            self.count = 0
            self.parent = parent
            self.dir = dir
            self.origDir = deepcopy(self.dir)
            self.saveDir = copy(dir)
            
    def reset(self):
        self.dir = copy(self.origDir)
        self.count = 0

    
    
            
    def next(self):
        nextPos = tuple(add(self.pos, self.dir))
        nextBranch = Branch(self, nextPos, copy(self.dir))
        return nextBranch
            
    
    
#b = Branch(None,Vector([0,0,0]),Vector([0,1,0]))
#print(b.pos)
#print(b.dir)
#n = add(([0,0,0]), ([0,0,1]))
#print(n)
    
  