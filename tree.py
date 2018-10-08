from mathutils import Vector
from array import array
import bpy
from .Branch import Branch
from .Leaf import Leaf, l
from bpy.props import BoolProperty
from math import sqrt
import math
from functools import partial
from random import randint, random, uniform
from copy import copy, deepcopy
#from .scaoperator import bpy 


#https://blenderartists.org/t/detecting-if-a-point-is-inside-a-mesh-2-5-api/485866/4
def point_inside(point,obj):
    axes = [ Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)) ]
    outside = False
    mat = obj.matrix_world.copy()
    mat.invert()
    for axis in axes:
        orig = mat*point
        count = 0
        while True:
            a,location,normal,index = obj.ray_cast(orig,orig+axis*1.84467e+19)
            if index == -1: break
            count += 1
            orig = location + axis*0.00001
        if count%2 == 0:
            outside = True
            break
    return not outside

def closest(pos, count, n, x, y, z):
    d2 = 1e30
    for i in range(n):
        if count[i] > 1:
            continue
        dx, dy, dz = x-pos[i*3], y-pos[i*3+1], z-pos[i*3+2]
        d = dx*dx + dy*dy + dz*dz
        if d < d2:
            d2 = d
            ci = i
            v = dx, dy, dz
    return d2, ci, v


def getDistance(p0, p1):
        return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)



# importiert von https://blender.stackexchange.com/questions/5898/how-can-i-create-a-cylinder-linking-two-points-with-python

class Tree:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Tools Tab Label'
    bl_context = 'objectmode'
    bl_category = 'SC'

    
   
    def __init__(self):
        # Vektor operationen

        def div(x,y):
            return(x[0]/y, x[1]/y, x[2]/y)

        def sub(x,y):
            return(x[0]-y[0], x[1]-y[1], x[2]-y[2])

        def normieren(x,y):
            länge = sqrt(x[0]**2 + x[1]**2 + x[2]**2)
            return((x[0]/länge + x[1]/länge+ x[2]/länge)*y)
        
        def length_squared(u):
            return sum([a ** 2 for a in u])


        def add(u, v):    
            return [a + b for a, b in zip(u, v)]

        def norm(u):
            return setlength(u, 0.5)

        def scale_by_scalar(u, scalar):
            return [a * scalar for a in u]

        def length(u):
            return math.sqrt(length_squared(u))

        def setlength(u, l):
            return scale_by_scalar(u, l / length(u))
        
        branches = []
        leaves = [] 
        verts = ()
        closeEnough = 0 # False
        
        #leaves generieren
        for i in range(0,bpy.context.scene.leaf):
            leaves.append(Leaf((uniform(-bpy.context.scene.xyvalue,bpy.context.scene.xyvalue),uniform(-bpy.context.scene.xyvalue,bpy.context.scene.xyvalue),uniform(bpy.context.scene.zvaluebot,bpy.context.scene.zvaluetop)),0))
            #bpy.ops.mesh.primitive_uv_sphere_add(size=0.1, location=leaves[i].pos)
            i =+ 1
            
        #Prüfen für Objekt    
        if bpy.context.scene.Growth_limitation == True:    
            for i in reversed(range(len(leaves))):
                myobj = bpy.context.object
                #mypoint = mathutils.Vector(leaves[i].pos)
                if (point_inside(Vector(leaves[i].pos),myobj)) == False:
                    del leaves[i]
   
        #Stamm machen    
        root = Branch(None,(0,0,0),(0,0,0.5))
        branches.append(root)
        current = root       

        max_dist = bpy.context.scene.maxdist#3
        min_dist = bpy.context.scene.mindist#1
        while closeEnough == 0: # False             
            for i in range (len(leaves)):
                g = 0
                g = getDistance(current.pos, leaves[i].pos)
                #print(g) 
                if (g < max_dist):
                    #print('schlaufe 1')
                    closeEnough = 1
                if (closeEnough == 0):
                    #print('         schlaufe 2          ')
                    nextPos = tuple(add(branches[i].pos,branches[i].dir))
                    branch = Branch(i,nextPos,branches[i].dir)
                    current = branch
                    branches.append(current)
                     
        
        #Der eigentliche Algorithmus                    
        def grow(self):           
            self.record = 100000
            for i in range(len(leaves)):
                leaf = leaves[i]
                closestBranch = None
                self.closestDir = None
                
                #Den nächsten Ast bestimmen
                for j in range(len(branches)):
                    #print(j) 
                    branch = branches[j]
                    dir = sub(leaf.pos ,branch.pos)
                    d = length(dir)
                    #print(d)
                    if (d < min_dist):
                        leaf.reached()
                        break
                    #elif(d > max_dist):      
                    elif (closestBranch == None or d < self.record):
                        closestBranch = branch
                        self.record = d
                         
                #Dessen Richtung bestimmen                              
                if (closestBranch is not None):
                    newDir = tuple(sub(leaf.pos, closestBranch.pos))
                    newDirnormed = norm(newDir)
                    #print(newDir)
                    closestBranch.dir = tuple(add(closestBranch.dir, newDirnormed))
                    closestBranch.count += 1
                
            #alle Blätter entfernen die erreicht wurden                       
            for i in reversed(range(len(leaves))):
                if (leaves[i].erreicht == 1):
                    del(leaves[i])

            branchcopy = deepcopy(branches)    
            #print(branches[0].dir)                                       
            for i in reversed(range(len(branches))):
                branch = branches[i]
                #print(branch.count)            
                if (branch.count > 0):               
                    branch.dir = tuple(div(branch.dir,branch.count))
                    newPos = tuple(add(branch.pos,branch.dir))
                    newB = Branch(i, newPos, branch.dir)
                    branches.append(newB)
                    branch.reset()
        
        
        for i in range(70):    
            grow(self)

        # this assumes all vertex positions are unique (= do not overlap)
        # create a mapping from vertex position to vertex index 
        verts = {b.pos:i for i,b in enumerate(branches)}
        # create vertex pairs as edge by locating vert index based on coordinates
        edges = [ (verts[b.pos],verts[branches[b.parent].pos])for b in branches if b.parent is not None]
        # replace vertex mapping by simple list of coordinates
        verts = [b.pos for b in branches]
 
        mesh = bpy.data.meshes.new("tree_mesh")
        mesh.from_pydata(verts, edges, faces=[])
        mesh.update()

        obj = bpy.data.objects.new("Tree", mesh)

        scene = bpy.context.scene
        scene.objects.link(obj)
        #remove doubles muss man noch machen


tree= Tree()




