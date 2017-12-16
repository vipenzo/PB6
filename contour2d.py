
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
import re

from math import *

from deletedefaultobjects import delete_all

def rad(ang):
    while ang > 180:
        ang -= 360
    while ang < -180:
        ang += 360
    return radians(ang)

class Contorno2D:
    def __init__(self):
        self.verts = [Vector((0, 0, 0))]
        self.direction = 0.0
        self.definition=20

    def add_line(self, l):
        #print(f"add_line curr={self.verts[-1]}")
        self.verts.append(Vector((self.verts[-1].x + l * cos(rad(self.direction)), self.verts[-1].y + l * sin(rad(self.direction)), 0)))

    def rotate(self, ang):
        self.direction += ang

    def calcIntersection(self, ax, bx, ay, by, anga, angb):
        ma = tan(rad(anga))
        mb = tan(rad(angb))
        #y = ax + c  c = ax - y =  ma*ax - ay
        #y = bx + d  d = bx - y =  mb*bx - by
        aq = ma*ax + ay
        bq = mb*bx + by
        cx = (bq - aq) / (mb - ma)
        if (abs(cos(rad(anga))) < 0.00001):
            cy = mb*cx + bq
        else:
            cy = ma*cx + aq

        print(f"ma={ma} mb={mb} aq={aq} bq={bq} cx={cx} cy={cy}")
        return cx, cy

    def curve(self, deltacurr, deltanext, angolo):
        ax = self.verts[-1].x
        ay = self.verts[-1].y
        curdir = self.direction
        newdir = self.direction+angolo

        bx = ax+deltacurr * cos(rad(curdir))
        by = ay+deltacurr * sin(rad(curdir))
        bx = bx+deltanext * cos(rad(newdir))
        by = by+deltanext * sin(rad(newdir))

        print(f"curdir={curdir} newdir={newdir}")
        cx, cy = self.calcIntersection(ax, bx, ay, by, curdir, newdir)

        print(f"ax={ax}, ay={ay}")
        print(f"bx={bx}, by={by}")
        print(f"cx={cx}, cy={cy}")
        for s in range(self.definition):
            d = float(s+1)/self.definition
            pax = ax + (cx-ax)*d
            pay = ay + (cy-ay)*d
            pbx = cx + (bx-cx)*d
            pby = cy + (by-cy)*d
            print(f"s={s} d={d} pax={pax} pay={pay} pbx={pbx} pby={pby}")
            sx = pax + (pbx-pax)*d
            sy = pay + (pby-pay)*d
            print(f"sx={sx}, sy={sy} len={len(self.verts)}")

            self.verts.append(Vector((sx, sy, 0)))
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
            print(f"A. lastx={self.verts[-1].x}, lasty={self.verts[-1].y} len={len(self.verts)}")
            mg=re.match("L(\d+)|R(-?\d+)|C(-?\d+):(-?\d+):(-?\d+)", str)
            if mg:
                cmd=mg.group()
                if cmd[0]=="L":
                        self.add_line(int(cmd[1:]))
                elif cmd[0]=="R":
                        self.rotate(int(cmd[1:]))
                elif cmd[0]=="C":
                        print(cmd[1:])
                        deltax, deltay, angolo = cmd[1:].split(":")
                        print(f"deltax={deltax}, deltay={deltay}, angolo={angolo}")
                        self.curve(float(deltax), float(deltay), float(angolo))
                print(cmd)
                str = str[len(cmd):]
            else:
                done=True
                print("niet")
            print(f"Z. lastx={self.verts[-1].x}, lasty={self.verts[-1].y} len={len(self.verts)}")

    def prova(self):
        self.dsl_parse("L5C2:2:90L5C2:2:90L5C2:2:90L5C2:2:90")
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
