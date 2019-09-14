from collections import Counter

import FreeCAD
import Part

bodies = []
obj_to_var = {}

class Body:
    def __init__(self, obj):
        self.name = obj.Name
        self.label = obj.Label
        self.tip = obj.Tip
        self.obj = obj
        self.debug = False
        self.group = []

    def unparse(self):
        obj = self.obj
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        self.var_name = "body_" + self.name.lower()
        text = []
        text.extend([
            f"{self.var_name}_debug = {self.debug}",
            f"{self.var_name} = App.activeDocument().addObject('PartDesign::Body', '{self.name}')",
            f"{self.var_name}.Label = '{self.label}'",
        ])

        if self.obj.Group:
            grp = []
            for obj in self.obj.Group:
                obj_var = obj_to_var.get(obj, None)
                if not obj_var:
                    obj_var, sub_text = self.unparse_obj(obj)
                    text.extend(sub_text)
                grp.append(obj_var)
            grp = ', '.join(grp)
            text.extend([
                f"{self.var_name}.Group = [{grp}]"
            ])

        if self.tip:
            var_name, sub_text = self.unparse_obj(self.tip)
            text.extend(sub_text)
            text.extend([
                f"{self.var_name}.Tip = {var_name}",
            ])

        text.append("FreeCAD.ActiveDocument.recompute()")
        text.append(f"Part.export([{self.var_name}], '{self.name}.brep')")

        return text

    def unparse_obj(self, obj):
        if obj in obj_to_var:
            return obj_to_var[obj], []

        var_name = "obj_" + obj.Name.lower()
        obj_to_var[obj] = var_name
        if obj.TypeId == 'PartDesign::Pocket':
            text = self.unparse_pad_or_pocket(var_name, obj)
        elif obj.TypeId == 'PartDesign::Pad':
            text = self.unparse_pad_or_pocket(var_name, obj)
        elif obj.TypeId == 'PartDesign::Chamfer':
            text = self.unparse_chamfer_or_fillet(var_name, obj)
        elif obj.TypeId == 'PartDesign::Fillet':
            text = self.unparse_chamfer_or_fillet(var_name, obj)
        elif obj.TypeId == 'Sketcher::SketchObject':
            text = self.unparse_sketch(var_name, obj)
        elif obj.TypeId == 'PartDesign::ShapeBinder':
            text = self.unparse_shapebinder(var_name, obj)
        elif obj.TypeId == 'App::Plane':
            text = self.unparse_plane(var_name, obj)
        else:
            raise RuntimeError(f"Unknown TypeId {obj.TypeId} at unparse")

        if text:
            if 1:
                self.group.append(var_name)
                cnt = len(self.group)
                grp = ', '.join(self.group)
                text.extend([
                    f"if {self.var_name}_debug:",
                    f"    {self.var_name}.Tip = {var_name}",
                    f"    {self.var_name}.Group = [{grp}]",
                    f"    FreeCAD.ActiveDocument.recompute()",
                    f"    App.ActiveDocument.saveAs('debug/plate-{self.obj.Label}-{cnt:03d}-{obj.Label}.FCStd')",
                ])
            text.append("FreeCAD.ActiveDocument.recompute()")
            text.append(f"print('{obj.Label}')")
            text.append("")

        return var_name, text

    def unparse_plane(self, var_name, obj):
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        if obj.Role == "XY_Plane":
            text = [f"{var_name} = App.activeDocument().XY_Plane"]
        else:
            raise RuntimeError(f"Unknown plane role {obj.Role} at unparse")

        return text

    def unparse_shapebinder(self, var_name, obj):
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))
        orig_name = obj.Label
        if orig_name.endswith("_bind"):
            orig_name = orig_name[:-5]

        return [
            f"{var_name} = {self.var_name}.newObject('PartDesign::ShapeBinder', '{obj.Name}')",
            f"{var_name}_orig = App.getDocument('frame').getObject('{orig_name}')",
            f"{var_name}.TraceSupport = False",
            f"{var_name}.Support = [({var_name}_orig, '')]"
        ]

    def unparse_chamfer_or_fillet(self, var_name, obj):
        print(f"----------- {obj.Label} ------------")

        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        text = []
        assert(obj.BaseFeature)
        base_var_name, base_text = self.unparse_obj(obj.BaseFeature)
        text.extend(base_text)

        text.extend([
            f"{var_name} = {self.var_name}.newObject('{obj.TypeId}', '{obj.Name}')",
            f"{var_name}.Label = '{obj.Label}'",
            f"{var_name}.BaseFeature = {base_var_name}",
        ])
        if obj.TypeId == "PartDesign::Fillet":
            text.extend([
                f"{var_name}.Radius = '{obj.Radius}'",
            ])
        else:
            text.extend([
                f"{var_name}.Size = '{obj.Size}'",
            ])

        assert(obj.Base)
        assert(obj.Base[0] == obj.BaseFeature)
        edges = [f"'{a}'" for a in obj.Base[1]]
        edges = ', '.join(edges)

        text.extend([
            f"{var_name}.Base = ({base_var_name}, [{edges}])",
        ])
        return text

    def unparse_pad_or_pocket(self, var_name, obj):
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))
        text = []
        assert obj.Profile[0].TypeId == 'Sketcher::SketchObject'
        assert obj.Profile[1] == []
        base_var_name = None
        if obj.BaseFeature:
            base_var_name, base_text = self.unparse_obj(obj.BaseFeature)
            text.extend(base_text)

        up_var_name = None
        if obj.UpToFace:
            up_var_name, up_text = self.unparse_obj(obj.UpToFace[0])
            assert not up_text


        sketch_var_name, sketch_text = self.unparse_obj(obj.Profile[0])
        text.extend(sketch_text)
        text.extend([
            f"{var_name} = {self.var_name}.newObject('{obj.TypeId}', '{obj.Name}')",
            f"{var_name}.Label = '{obj.Label}'",
            f"{var_name}.Profile = ({sketch_var_name}, [])",
            f"{var_name}.Length = '{obj.Length}'",
            f"{var_name}.Length2 = '{obj.Length2}'",
            f"{var_name}.Type = '{obj.Type}'",
            f"{var_name}.Reversed = {obj.Reversed}",
            f"{var_name}.Midplane = {obj.Midplane}",
            f"{var_name}.Offset = '{obj.Offset}'",
        ])
        if base_var_name:
            text.extend([
                f"{var_name}.BaseFeature = {base_var_name}",
            ])

        if up_var_name:
            text.extend([
                f"{var_name}.UpToFace = ({up_var_name}, {obj.UpToFace[1]})",
            ])

        return text

    def unparse_sketch(self, var_name, obj):
        text = []
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        ext_geom_names = []
        if obj.ExternalGeometry:
            for ext_obj, ext_features in obj.ExternalGeometry:
                ext_obj_var = obj_to_var.get(ext_obj, None)
                if not ext_obj_var:
                    ext_obj_var, ext_text = self.unparse_obj(ext_obj)
                    text.extend(ext_text)
                for ext_feature in ext_features:
                    ext_geom_names.append([ext_obj_var, ext_feature])

        text.append(f"{var_name} = {self.var_name}.newObject('Sketcher::SketchObject', '{obj.Name}')")
        if obj.Support:
            support_obj = obj.Support[0][0]
            support_var = obj_to_var.get(support_obj, None)
            if not support_var:
                support_var, support_text = self.unparse_obj(support_obj)
                text.extend(support_text)
            obj_feature = obj.Support[0][1][0]
            text.append(f"{var_name}.Support = ({support_var}, ['{obj_feature}'])")

        if obj.MapMode:
            text.append(f"{var_name}.MapMode = '{obj.MapMode}'")

        vectors = {}
        geoms = []
        geom_names = []
        geoms_text = []
        vectors_text = []
        numbers = Counter()
        if obj.Geometry:
            for geom in obj.Geometry:
                if isinstance(geom, Part.LineSegment):
                    numbers["line"] += 1
                    n = numbers["line"]
                    geom_var_name = f"{var_name}_line_{n}"

                    start_point = self.get_vector(geom.StartPoint, numbers, var_name, vectors, vectors_text)
                    end_point = self.get_vector(geom.EndPoint, numbers, var_name, vectors, vectors_text)

                    geoms_text.append(f"{geom_var_name} = Part.LineSegment({start_point}, {end_point})")
                    if geom.Construction:
                        geoms_text.append(f"{geom_var_name}.Construction = {geom.Construction}")
                    if geom.Continuity != "CN":
                        geoms_text.append(f"{geom_var_name}.Continuity = {geom.Continuity}")
                elif isinstance(geom, Part.Circle):
                    numbers["circle"] += 1
                    n = numbers["circle"]
                    geom_var_name = f"{var_name}_circle_{n}"
                    center = self.get_vector(geom.Center, numbers, var_name, vectors, vectors_text)
                    geoms_text.append(f"{geom_var_name} = Part.Circle({center}, App.{geom.Axis}, {geom.Radius})")
                    if geom.Construction:
                        geoms_text.append(f"{geom_var_name}.Construction = {geom.Construction}")
                    if geom.Continuity != "CN":
                        geoms_text.append(f"{geom_var_name}.Continuity = {geom.Continuity}")
                elif isinstance(geom, Part.ArcOfCircle):
                    numbers["circle"] += 1
                    n = numbers["circle"]
                    geom_var_name = f"{var_name}_circle_{n}"
                    center = self.get_vector(geom.Center, numbers, var_name, vectors, vectors_text)
                    geoms_text.append(f"{geom_var_name} = Part.ArcOfCircle(Part.Circle({center}, App.{geom.Axis}, {geom.Radius}), {geom.FirstParameter}, {geom.LastParameter})")
                    if geom.Construction:
                        geoms_text.append(f"{geom_var_name}.Construction = {geom.Construction}")
                    if geom.Continuity != "CN":
                        geoms_text.append(f"{geom_var_name}.Continuity = {geom.Continuity}")
                elif isinstance(geom, Part.Point):
                    numbers["point"] += 1
                    n = numbers["point"]
                    geom_var_name = f"{var_name}_point_{n}"
                    center_point = FreeCAD.Vector(geom.X, geom.Y, geom.Z)
                    center = self.get_vector(center_point, numbers, var_name, vectors, vectors_text)
                    geoms_text.append(f"{geom_var_name} = Part.Point({center})")
                    if geom.Construction:
                        geoms_text.append(f"{geom_var_name}.Construction = {geom.Construction}")
                else:
                    print(type(geom))
                    raise RuntimeError(f"Unknown part class {geom} at sketch unparse")
                geoms.append(geom)
                geom_names.append(geom_var_name)
                obj_to_var[geom] = geom_var_name

        text.extend(vectors_text)
        text.extend(geoms_text)
        all_geoms = ", ".join(geom_names)
        text.extend([
            f"{var_name}_all_geoms = [{all_geoms}]",
            f"{var_name}.addGeometry({var_name}_all_geoms, False)",
        ])
        if ext_geom_names:
            ext_geoms_text = ', '.join([f"[{a}, '{b}']".format(a=a, b=b) for a, b in ext_geom_names])
            text.extend([
                f"{var_name}_all_ext_geoms = [{ext_geoms_text}]",
                f"for a, b in {var_name}_all_ext_geoms:",
                f"    {var_name}.addExternal(a.Name, b)",
            ])

        constraints = []
        i = 1
        if obj.Constraints:
            text.append(f"{var_name}_constraints = [")
            for constr in obj.Constraints:
                print(constr.Type,
                    constr.First,
                    constr.FirstPos,
                    constr.Second,
                    constr.SecondPos,
                    constr.Third,
                    constr.ThirdPos,
                    constr.Value)

                first_text = self.convert_geoindex(ext_geom_names, constr.First, geom_names, var_name)
                second_text = self.convert_geoindex(ext_geom_names, constr.Second, geom_names, var_name)
                third_text = self.convert_geoindex(ext_geom_names, constr.Third, geom_names, var_name)

                if constr.Type in ("Coincident", "Tangent"):
                    text.extend([
                        f"    Sketcher.Constraint('{constr.Type}',",
                        f"        {first_text}, {constr.FirstPos},",
                        f"        {second_text}, {constr.SecondPos},",
                        f"    ),"
                    ])
                elif constr.Type in ("Horizontal", "Vertical"):
                    if second_text is None:
                        text.extend([
                            f"    Sketcher.Constraint('{constr.Type}',",
                            f"        {first_text},",
                            f"    ),"
                        ])
                    else:
                        text.extend([
                            f"    Sketcher.Constraint('{constr.Type}',",
                            f"        {first_text}, {constr.FirstPos},",
                            f"        {second_text}, {constr.SecondPos},",
                            f"    ),"
                        ])
                elif constr.Type in ("DistanceX", "DistanceY", "Angle"):
                    if second_text is None:
                        text.extend([
                            f"    Sketcher.Constraint('{constr.Type}',",
                            f"        {first_text}, {constr.FirstPos},",
                            f"        {constr.Value},",
                            f"    ),"
                        ])
                    else:
                        text.extend([
                            f"    Sketcher.Constraint('{constr.Type}',",
                            f"        {first_text}, {constr.FirstPos},",
                            f"        {second_text}, {constr.SecondPos},",
                            f"        {constr.Value},",
                            f"    ),"
                        ])
                elif constr.Type == "Symmetric":
                    text.extend([
                        f"    Sketcher.Constraint('{constr.Type}',",
                        f"        {first_text}, {constr.FirstPos},",
                        f"        {second_text}, {constr.SecondPos},",
                        f"        {third_text}, {constr.ThirdPos},",
                        f"    ),"
                    ])
                elif constr.Type == "Radius":
                    text.extend([
                        f"    Sketcher.Constraint('{constr.Type}',",
                        f"        {first_text}, {constr.Value},",
                        f"    ),"
                    ])
                elif constr.Type == "PointOnObject":
                    text.extend([
                        f"    Sketcher.Constraint('{constr.Type}',",
                        f"        {first_text}, {constr.FirstPos},",
                        f"        {second_text},",
                        f"    ),"
                    ])
                elif constr.Type == "Equal":
                    text.extend([
                        f"    Sketcher.Constraint('{constr.Type}',",
                        f"        {first_text},",
                        f"        {second_text},",
                        f"    ),"
                    ])
                else:
                    print(constr.Type)
                    raise RuntimeError(f"Unknown constraint type {constr.Type} at sketch unparse")
                text.append(f"    # {i}")
                i += 1
            text.extend([
                f"]",
                f"{var_name}.addConstraint({var_name}_constraints)",
            ])


        return text

    def convert_geoindex(self, ext_geom_names, first, geom_names, var_name):
        if first != -2000:
            if first in [-1, -2]:
                first_text = f"{first}"
            elif first >= 0:
                first = geom_names[first]
                first_text = f"{var_name}_all_geoms.index({first})"
            else:
                first = ext_geom_names[-first - 3]
                first = "[{}, '{}']".format(*first)
                first_text = f"-{var_name}_all_ext_geoms.index({first})-3"
            print(first_text)
        else:
            first_text = None

        return first_text

    def get_vector(self, vector, numbers, var_name, vectors, vectors_text):
        str_vector = f"App.Vector({vector.x:.3f}, {vector.y:.3f}, {vector.z:.3f})"
        start_point = vectors.get(str_vector, None)
        if not start_point:
            numbers["vector"] += 1
            v_n = numbers["vector"]
            vector_var_name = f"{var_name}_vector_{v_n}"
            vectors_text.append(f"{vector_var_name} = {str_vector}")
            vectors[str_vector] = vector_var_name
            start_point = vector_var_name
        return start_point


d = FreeCAD.open('left_y_motor_plate.FCStd')
#d = FreeCAD.open('left_y_idler_plate.FCStd')
#d = FreeCAD.open('plate.FCStd')
for obj in d.Objects:
    #print(obj.TypeId, obj.Name, obj.Label)
    #print(obj.PropertiesList)
    if obj.TypeId == 'PartDesign::Body':
        bodies.append(Body(obj))
    elif obj.TypeId == 'App::Origin':
        pass
    elif obj.TypeId == 'App::Line':
        pass
    elif obj.TypeId == 'App::Plane':
        pass
    elif obj.TypeId == 'PartDesign::ShapeBinder':
        #print(obj.PropertiesList)
        #print(obj.Placement)
        pass
    elif obj.TypeId == 'Sketcher::SketchObject':
        #print(obj.PropertiesList)
        pass
    elif obj.TypeId == 'PartDesign::Pad':
        #print(obj.PropertiesList)
        pass
    elif obj.TypeId == 'PartDesign::Pocket':
        #print(obj.PropertiesList)
        pass
    elif obj.TypeId == 'PartDesign::Fillet':
        # print(obj.PropertiesList)
        pass
    elif obj.TypeId == 'PartDesign::Chamfer':
        # print(obj.PropertiesList)
        pass
    else:
        raise RuntimeError(f"Unknown TypeId {obj.TypeId} on top-level")

f = open("left_y_motor_plate.py", "w")
f.write("""
import sys
import FreeCAD
import Part
import Sketcher

App = FreeCAD

print(1)
FreeCAD.open("frame.FCStd")
App.setActiveDocument("frame")
FreeCAD.ActiveDocument.recompute()
print(2)

FreeCAD.newDocument("plate")
App.setActiveDocument("plate")
print(3)
""")

for body in bodies:
    text = body.unparse()
    print("\n".join(text))
    f.write("\n".join(text) + "\n")

f.write("""
App.ActiveDocument.saveAs("plate.FCStd")
""")
f.close()




