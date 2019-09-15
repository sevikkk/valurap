import sys
import FreeCAD
import os
import Part

App = FreeCAD

in_gui = False
if App.ActiveDocument:
    assert(App.ActiveDocument.Label == "print")
    in_gui = True

if not in_gui:
    App.newDocument("print")
    App.setActiveDocument("print")

pp = []

workdir = os.path.dirname(__file__)
part = "left_y_idler_plate"
Part.insert(f'{workdir}/{part}.brep', App.ActiveDocument.Name)
p = App.ActiveDocument.getObject(part)
if p.ViewObject:
    p.ViewObject.Visibility = False

bbox = p.Shape.BoundBox
plc = App.Placement(
    App.Vector(
        -(bbox.XMin + bbox.XMax)/2,
        -bbox.YMin,
        -(bbox.ZMin + bbox.ZMax)/2,
        ),
    App.Rotation(App.Vector(0,0,1),0)
)
plc = App.Placement(
    App.Vector(0, 0, 0),
    App.Rotation(App.Vector(1,0,0),90)
).multiply(plc)
p.Placement = plc

right_part = 'right' + part[4:]
rp = App.ActiveDocument.addObject("Part::Mirroring", right_part)
rp.Source = p
rp.Label = right_part
rp.Normal = (1, 0, 0)
rp.Base = (0, 0, 0)
plc = App.Placement(
    App.Vector(0, 40, 0),
    App.Rotation(App.Vector(1,0,0),0)
)
rp.Placement = plc
if rp.ViewObject:
    rp.ViewObject.Visibility = True

pp.append(rp)

part = "left_y_motor_plate"
Part.insert(f'{workdir}/{part}.brep', App.ActiveDocument.Name)
p = App.ActiveDocument.getObject(part)
if p.ViewObject:
    p.ViewObject.Visibility = False

bbox = p.Shape.BoundBox
plc = App.Placement(
    App.Vector(
        -(bbox.XMin + bbox.XMax)/2,
        -bbox.YMax,
        -(bbox.ZMin + bbox.ZMax)/2,
        ),
    App.Rotation(App.Vector(0,0,1),0)
)
plc = App.Placement(
    App.Vector(0, 0, 0),
    App.Rotation(App.Vector(1,0,0),-90)
).multiply(plc)

p.Placement = plc

right_part = 'right' + part[4:]
rp = App.ActiveDocument.addObject("Part::Mirroring", right_part)
rp.Source = p
rp.Label = right_part
rp.Normal = (1, 0, 0)
rp.Base = (0, 0, 0)
plc = App.Placement(
    App.Vector(0, -40, 0),
    App.Rotation(App.Vector(1,0,0),0)
)
rp.Placement = plc

if rp.ViewObject:
    rp.ViewObject.Visibility = True

pp.append(rp)

heated_plate = App.ActiveDocument.addObject("Part::Box", "HeatedPlate_base")
heated_plate.Length = "200 mm"
heated_plate.Width = "200 mm"
heated_plate.Height = "3 mm"
heated_plate.Placement = App.Placement(
    App.Vector(-100, -100, -3),
    #App.Vector(0, 0, -3),
    App.Rotation(App.Vector(0,0,1),0)
)
if heated_plate.ViewObject:
    heated_plate.ViewObject.Visibility = True

print(heated_plate.Shape.BoundBox)

import Mesh
Mesh.export(pp,f"{workdir}/{right_part}.stl")
