
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from math import *

class Contorno2D:
    def make_solid(self, h):
        scale_x = 1
        scale_y = 2
        verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, -1 * scale_y, 0)),
                 Vector((-1 * scale_x, -1 * scale_y, 0)),
                ]
        l = len(verts)

        edges = []
        faces = [[0, 1, 2, 3]]
        
    
        verts += list(map(lambda x: Vector((x.x, x.y, h)), verts))
        faces += list(map(lambda x: [x, x+l, ((x+1) % l)+l, ((x+1) % l)], range(l)))
        faces += [[l, l+3, l+2, l+1]]
        
        mesh = bpy.data.meshes.new(name="New Object Mesh")
        print(verts)
        print(faces)
        mesh.from_pydata(verts, edges, faces)
        object_data_add(bpy.context, mesh)
        
    def add_object(self, context):
        scale_x = 1
        scale_y = 2

        verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, -1 * scale_y, 0)),
                 Vector((-1 * scale_x, -1 * scale_y, 0)),
                ]

        edges = []
        faces = [[0, 1, 2, 3]]

        mesh = bpy.data.meshes.new(name="New Object Mesh")
        mesh.from_pydata(verts, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)
        object_data_add(context, mesh)


x=Contorno2D()
x.make_solid(5)