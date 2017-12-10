import os
import sys
import bpy

csfp = "/home/enzo/Documents/3dprinting/python_blender"
filepath = bpy.path.abspath(csfp)
print("csfp="+csfp)
if csfp not in sys.path:
    sys.path.insert(0, csfp)

filename = bpy.path.abspath(f"{csfp}/contour2d.py")
exec(compile(open(filename).read(), filename, 'exec'))