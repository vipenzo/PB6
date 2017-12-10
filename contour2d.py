
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
import re

from math import *

from deletedefaultobjects import delete_all


class Contorno2D:
    def __init__(self):
        self.verts = [Vector((0, 0, 0))]
        self.direction = 0.0
        self.definition=10

    def add_line(self, l):
        #print(f"add_line curr={self.verts[-1]}")
        self.verts.append(Vector((self.verts[-1].x + l * cos(radians(self.direction)), self.verts[-1].y + l * sin(radians(self.direction)), 0)))

    def rotate(self, ang):
        self.direction += ang

    def curve(self, raggio, angolo):
        raggio = float(raggio) / self.definition
        print(f"curve raggio={raggio}")
        step = float(angolo) / self.definition
        print(f"step={step}")
        for s in range(self.definition):
            self.verts.append(Vector((self.verts[-1].x + raggio * cos(radians(self.direction+s*step)), self.verts[-1].y + raggio * sin(radians(self.direction+s*step)), 0)))
        self.direction += angolo


    def add_object(self, verts, faces):
        edges = []
        mesh = bpy.data.meshes.new(name="New Object Mesh")
        print(verts)
        print(faces)
        mesh.from_pydata(verts, edges, faces)
        object_data_add(bpy.context, mesh)
        return bpy.context.active_object

    def extrude_verts(self, h):
        verts = self.verts
        l = len(verts)
        faces = [range(l)]
        verts += list(map(lambda x: Vector((x.x, x.y, h)), verts))
        faces += list(map(lambda x: [x, x+l, ((x+1) % l)+l, ((x+1) % l)], range(l)))
        faces += [[l] + [x+l for x in range(l-1,0,-1)]]
        return self.add_object(verts, faces)

    def make_solid(self, h):
        scale_x = 1
        scale_y = 1
        verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, 1 * scale_y, 0)),
                 Vector((1 * scale_x, -1 * scale_y, 0)),
                 Vector((-1 * scale_x, -1 * scale_y, 0)),
                ]
        l = len(verts)

        faces = [range(l)]
        verts += list(map(lambda x: Vector((x.x, x.y, h)), verts))
        faces += list(map(lambda x: [x, x+l, ((x+1) % l)+l, ((x+1) % l)], range(l)))
        faces += [[l] + [x+l for x in range(l,0,-1)]]

        return self.add_object(verts, faces)

    def dsl_parse(self, str):
        done=False
        while not done:
            mg=re.match("L(\d+)|R(-?\d+)|C(\d+):(-?\d+)", str)
            if mg:
                cmd=mg.group()
                if cmd[0]=="L":
                        self.add_line(int(cmd[1:]))
                elif cmd[0]=="R":
                        self.rotate(int(cmd[1:]))
                elif cmd[0]=="C":
                        print(cmd[1:])
                        raggio, angolo = cmd[1:].split(":")
                        print(f"raggio={raggio}")
                        print(f"angolo={angolo}")
                        self.curve(int(raggio), int(angolo))
                print(cmd)
                str = str[len(cmd):]
            else:
                done=True
                print("niet")

    def prova(self):
        self.dsl_parse("L5C1:-90L5C1:-90L5C1:-90L5C2:-90")
        """
        cmds = [
                ["L", 100],
                ["R", -90],
                ["L", 50],
                ["R", -90],
                ["L", 100]
                ]
        for cmd in cmds:
            if cmd[0] == "L":
                self.add_line(cmd[1])
            elif cmd[0] == "R":
                self.rotate(cmd[1])
        """

delete_all()
x=Contorno2D()
#obj = x.make_solid(5)
x.prova()
obj = x.extrude_verts(5)
obj.location=Vector((0,0,0))
print(f"obj={obj}")
