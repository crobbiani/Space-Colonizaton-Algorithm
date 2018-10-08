bl_info = {
    "name": "SCA",
    "author": "Carlo Robbiani",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > Tool Shelf > SCA",
    "description": "Adds a tree to scene",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }
import bpy
from bpy.props import BoolProperty
from bpy.types import PropertyGroup

bpy.types.Scene.xyvalue = bpy.props.FloatProperty(name="width", description="change width of tree", default=4.0, min=1.0, max=10.0, soft_min=1.0, soft_max=10.0, step=1, precision=1, unit='NONE', update=None, get=None, set=None)
bpy.types.Scene.zvaluebot = bpy.props.FloatProperty(name="bottom height", description="change bottom height of tree", default=4.0, min=1.0, max=10.0, soft_min=1.0, soft_max=10.0, step=1, precision=1, unit='NONE', update=None, get=None, set=None)
bpy.types.Scene.zvaluetop = bpy.props.FloatProperty(name="top height", description="change top height of tree", default=10.0, min=3.0, max=15.0, soft_min=3.0, soft_max=15.0, step=1, precision=1, unit='NONE', update=None, get=None, set=None)
    
bpy.types.Scene.maxdist = bpy.props.FloatProperty(name="maxdist", description="change max dist", default=3.0, min=2.0, max=10.0, soft_min=2.0, soft_max=10.0, step=1, precision=1, unit='NONE', update=None, get=None, set=None)
bpy.types.Scene.mindist = bpy.props.FloatProperty(name="mindist", description="change min dist", default=1.0, min=0.5, max=10.0, soft_min=0.5, soft_max=10.0, step=1, precision=1, unit='NONE', update=None, get=None, set=None)
bpy.types.Scene.leaf = bpy.props.IntProperty(name="leaves", description="change number of leaves", default=150, min=10, max=1000, soft_min=10, soft_max=1000, step=1, update=None, get=None, set=None)   
bpy.types.Scene.Start =  bpy.props.FloatProperty(name="starting thickness", description="change start thickness", default=0.5, min=0.1, max=1.0, soft_min=0.1, soft_max=1.0, step=0.1, precision=1, unit='NONE', update=None, get=None, set=None)   
bpy.types.Scene.basis =  bpy.props.FloatProperty(name="factor 1", description="change factor for thinnig out branches", default=102, min=100, max=150, soft_min=100, soft_max=150, step=1, precision=1, unit='NONE', update=None, get=None, set=None)   
bpy.types.Scene.exp =  bpy.props.FloatProperty(name="factor 2", description="change factor for thinnig out branches", default=90, min=70, max=100, soft_min=70, soft_max=100, step=1, precision=1, unit='NONE', update=None, get=None, set=None)   



  
#Skin operator    
class Skin (bpy.types.Operator):
    """Add Skin Modifier to Selected Tree"""
    bl_idname = "object.skin_operator"
    bl_label = "Add Skin Modifier "
    
    def execute(self,context):
        bpy.ops.object.modifier_add(type='SKIN')
        return {'FINISHED'}
    
#remove doubles operator    
class removeDoubles (bpy.types.Operator):
    bl_idname = "object.doubles_operator"
    bl_label = "remove double vertices "
    
    def execute(self,context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles(threshold=0.2)
        bpy.ops.mesh.dissolve_limited()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class thin (bpy.types.Operator):
    """Thin out branches, requires Skin Modifier"""
    bl_idname = "object.thin_operator"
    bl_label = "thin out Branches"
    
    def execute (self, context):
        start = bpy.context.scene.Start
        scene = context.scene
        f1 = bpy.context.scene.basis/100.0
        f2 = bpy.context.scene.exp/100.0
        obj = scene.objects[scene.Tree]
        for v in obj.data.skin_vertices[0].data: 
            start = start *((f1**-f2))      #1.02**-0.9
            v.radius = (start,start)
            #print(v.radius[:])
        return {'FINISHED'}
    
class particlesystem (bpy.types.Operator):
    """Add Particle System, needs Weight Paint"""
    bl_idname = "object.particle"
    bl_label = "add particle system"
    
    def execute (self, context):
        scene = context.scene
        obj = scene.objects[scene.Tree]
        if len(obj.particle_systems) == 0:
            obj.modifiers.new("part", type='PARTICLE_SYSTEM')
            part = obj.particle_systems[0]

            settings = part.settings
            settings.count = 500
            settings.use_advanced_hair = True
            settings.use_rotations = True
            settings.phase_factor = 1.000
            settings.phase_factor_random = 2.000
    
            settings.physics_type = 'NEWTON'    
            settings.rotation_mode = 'GLOB_Z'
            settings.rotation_factor_random = 0.486
    
            settings.type = 'HAIR'
            settings.emit_from = 'FACE'
            settings.particle_size = 0.1
            settings.render_type = 'GROUP'

            return {'FINISHED'}
        
class Growth_limitation(PropertyGroup):
    my_bool = BoolProperty(
        name="Growth limitation",
        description="Limit Growth with Object",
        default = False
        )     

    
class SCA (bpy.types.Operator):
    """Add Tree to the scene"""
    bl_idname = "object.tree_operator"
    bl_label = "Add a tree to the scene"

    def execute(self, context):
        from .tree import Tree
        from .Branch import Branch
        from .Leaf import Leaf, l 
        return {'FINISHED'}
    

     


    
#Baum Tab und Knöpfe
class SCAPANEL(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "SCA Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "SCA"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Add Tree", icon='OUTLINER_OB_MESH')

        row = layout.row()
        row.operator("object.tree_operator", icon='MOD_SKIN')
        
        row = layout.row()
        col = row.column(align = True)
        col.prop(context.scene, 'xyvalue', slider = True)
        col.prop(context.scene, 'zvaluebot', slider = True)
        col.prop(context.scene, 'zvaluetop', slider = True)
        
        row = layout.row()
        col = row.column(align = True)
        col.prop(context.scene, 'maxdist', slider=True)
        col.prop(context.scene, 'mindist', slider=True)
        col.prop(context.scene, 'leaf', slider=True)
        
        row = layout.row()
        row.operator("object.skin_operator")
        
        row = layout.row()
        col = row.column(align = True)
        col.prop(context.scene, 'Start', slider = True)
        col.prop(context.scene, 'basis', slider = True)
        col.prop(context.scene, 'exp', slider = True)
        col.operator("object.thin_operator")
        
        #Auswählbox
        layout = self.layout
        scene = context.scene               
        layout.prop_search(scene, "Tree", scene, "objects")
        
        row = layout.row()
        row.operator("object.doubles_operator")
        
        row = layout.row()
        row.operator("object.particle")
        #print(bpy.context.scene.maxdist)
        
        row = layout.row()
        scene = context.scene
        row.prop(scene, "Growth_limitation")     
        
def register():
    bpy.utils.register_class(SCAPANEL)
    bpy.utils.register_class(SCA)
    bpy.utils.register_class(Skin)
    bpy.utils.register_class(removeDoubles)
    bpy.utils.register_class(thin)
    bpy.types.Scene.Tree = bpy.props.StringProperty()
    bpy.utils.register_class(particlesystem)
    bpy.types.Scene.Growth_limitation = bpy.props.BoolProperty()
    bpy.types.Scene.limiter = bpy.props.StringProperty()

    
def unregister():
    bpy.utils.unregister_class(SCAPANEL)
    bpy.utils.unregister_class(SCA)
    bpy.utils.unregister_class(Skin)
    bpy.utils.unregister_class(removeDoubles)
    bpy.utils.unregister_class(thin)
    bpy.utils.unregister_class(particlesystems)
    del bpy.types.Object.Tree
    del bpy.types.Object.Growth_limitation
    del bpy.types.Object.limiter


    
if __name__ == "__main__":
     register() 


    # test call
    #bpy.ops.object.simple_operator()
