from random import random, uniform,randint
import bpy
from mathutils import Vector, Matrix
from bpy.props import BoolProperty



class Leaf(object):
	def __init__(self,pos,erreicht):
		self.pos = pos
		self.erreicht = 0 
			
	def reached(self):
		self.erreicht = 1
		

l = Leaf((uniform(-4.0,4.0),uniform(-4.0,4.0),uniform(4.0,9.0)),0)

