import os
import FreeCAD
import Part

FreeCAD.newDocument("vitamins")
FreeCAD.setActiveDocument("vitamins")

for fn in os.listdir('vitamins/breps'):
   print("----------- {} ------------".format(fn))
   if fn.endswith('.brep'):
      fn = fn[:]
      name = fn[:-5]
      print(fn, name)
      p = Part.insert('vitamins/breps/' + fn, "vitamins")

x = 0
y = 0
for o in FreeCAD.ActiveDocument.Objects:
   print(o.Name)
   o.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, 0), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0))
   x += 100
   if x > 500:
      x = 0
      y += 100

FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.saveAs("vitamins/vitamins.FCStd")



