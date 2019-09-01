import FreeCAD

v = FreeCAD.open('vitamins/vitamins2.FCStd')
for obj in v.Objects:
    print(obj.Name, obj.Label)
    obj.Shape.exportBrep(f'vitamins/breps/{obj.Label}.brep')