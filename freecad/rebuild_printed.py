import os
import FreeCAD
import Part
import PartDesign

App = FreeCAD
print(dir(PartDesign))
for part in [
      'left_y_idler_plate',
      'left_y_motor_plate',
      'left_y_carriage_plate',
      'left_z_rod_support',
      'left_z_rod_plate',
      'x_carriage_plate',
      'titan_mount_plate',
   ]:
   FreeCAD.open(f"{part}.FCStd")
   App.setActiveDocument(part)
   body = None
   for o in FreeCAD.ActiveDocument.Objects:
       if o.TypeId == "PartDesign::Body":
           body = o
           break

   print(body)
   Part.export([body], f'printed/{part}.brep')



