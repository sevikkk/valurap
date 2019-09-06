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

    def unparse(self):
        obj = self.obj
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        self.var_name = "body_" + self.name.lower()
        text = []
        text.extend([
            f"{self.var_name} = App.activeDocument().addObject('PartDesign::Body', '{self.name}')",
            f"{self.var_name}.Label = '{self.label}'",
        ])

        if self.tip:
            var_name, sub_text = self.unparse_obj(self.tip)
            text.extend(sub_text)
            text.extend([
                f"{self.var_name}.Tip = {var_name}"
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

        text.append("FreeCAD.ActiveDocument.recompute()")

        return text

    def unparse_obj(self, obj):
        var_name = "obj_" + obj.Name.lower()
        obj_to_var[obj] = var_name
        if obj.TypeId == 'PartDesign::Pocket':
            text = self.unparse_pad_or_pocket(var_name, obj)
        elif obj.TypeId == 'PartDesign::Pad':
            text = self.unparse_pad_or_pocket(var_name, obj)
        elif obj.TypeId == 'Sketcher::SketchObject':
            text = self.unparse_sketch(var_name, obj)
        elif obj.TypeId == 'PartDesign::ShapeBinder':
            text = self.unparse_shapebinder(var_name, obj)
        elif obj.TypeId == 'App::Plane':
            text = self.unparse_plane(var_name, obj)
        else:
            raise RuntimeError(f"Unknown TypeId {obj.TypeId} at unparse")

        if text:
            text.append("FreeCAD.ActiveDocument.recompute()")
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

        sketch_var_name, sketch_text = self.unparse_obj(obj.Profile[0])
        text.extend(sketch_text)
        text.extend([
            f"{var_name} = {self.var_name}.newObject('{obj.TypeId}', '{obj.Name}')",
            f"{var_name}.Label = '{obj.Label}'",
            f"{var_name}.Profile = ({sketch_var_name}, '')",
            f"{var_name}.Length = '{obj.Length}'",
            f"{var_name}.Length2 = '{obj.Length2}'",
            f"{var_name}.Type = '{obj.Type}'",
            f"{var_name}.UpToFace = {obj.UpToFace}",
            f"{var_name}.Reversed = {obj.Reversed}",
            f"{var_name}.Midplane = {obj.Midplane}",
            f"{var_name}.Offset = '{obj.Offset}'",
        ])
        if base_var_name:
            text.extend([
                f"{var_name}.BaseFeature = {base_var_name}",
            ])

        return text

    def unparse_sketch(self, var_name, obj):
        """
>>> App.activeDocument().Body.newObject('Sketcher::SketchObject','Sketch006')
>>> App.activeDocument().Sketch006.Support = (App.ActiveDocument.Pocket002,["Face5"])
>>> App.activeDocument().Sketch006.MapMode = 'FlatFace'

>>> geoList = []
>>> geoList.append(Part.LineSegment(App.Vector(-6.205385,81.502983,0),App.Vector(13.953376,81.502983,0)))
>>> geoList.append(Part.LineSegment(App.Vector(13.953376,81.502983,0),App.Vector(13.953376,50.348553,0)))
>>> geoList.append(Part.LineSegment(App.Vector(13.953376,50.348553,0),App.Vector(-6.205385,50.348553,0)))
>>> geoList.append(Part.LineSegment(App.Vector(-6.205385,50.348553,0),App.Vector(-6.205385,81.502983,0)))
>>> App.ActiveDocument.Sketch007.addGeometry(Part.Circle(App.Vector(52.265846,24.476919,0),App.Vector(0,0,1),11.189683),False)
>>> App.ActiveDocument.Sketch006.addGeometry(geoList,False)

>>> conList = []
>>> conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
>>> conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
>>> conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
>>> conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
>>> conList.append(Sketcher.Constraint('Horizontal',0))
>>> conList.append(Sketcher.Constraint('Horizontal',2))
>>> conList.append(Sketcher.Constraint('Vertical',1))
>>> conList.append(Sketcher.Constraint('Vertical',3))
>>> App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Symmetric',0,1,1,2,4,3))

>>> App.ActiveDocument.Sketch006.addConstraint(conList)
>>>
>>> App.ActiveDocument.Sketch006.addExternal("Pocket002","Edge4")
>>> App.ActiveDocument.Sketch006.addExternal("FrontVSlot_bind","Edge211")

>>> App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-4))

>>> App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Radius',4,11.189683))
>>> App.ActiveDocument.Sketch007.setDatum(13,App.Units.Quantity('5.000000 mm'))

>>> App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,16.205385))
>>> App.ActiveDocument.Sketch006.setDatum(9,App.Units.Quantity('11.000000 mm'))
        """
        text = []
        print(f"----------- {obj.Label} ------------")
        for prop in obj.PropertiesList:
            print(prop, getattr(obj, prop))

        ext_geom = []
        ext_geoms_text = []
        if obj.ExternalGeometry:
            for ext_obj, ext_features in obj.ExternalGeometry:
                ext_obj_var = obj_to_var.get(ext_obj, None)
                if not ext_obj_var:
                    ext_obj_var, ext_text = self.unparse_obj(ext_obj)
                    text.extend(ext_text)
                for ext_feature in ext_features:
                    ext_geom.append([ext_obj_var, ext_feature])
                    ext_geoms_text.append(f"{var_name}.addExternal({ext_obj_var}.Name, '{ext_feature}')")

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
        text.append(f"{var_name}.addGeometry([{all_geoms}],False)")
        text.extend(ext_geoms_text)

        constraints = []
        if obj.Constraints:
            for constr in obj.Constraints:
                if constr.Type == "Coincident":
                    pass
                elif constr.Type == "Horizontal":
                    pass
                elif constr.Type == "Vertical":
                    pass
                elif constr.Type == "DistanceY":
                    pass
                elif constr.Type == "DistanceX":
                    pass
                elif constr.Type == "Symmetric":
                    pass
                elif constr.Type == "Radius":
                    pass
                elif constr.Type == "PointOnObject":
                    pass
                elif constr.Type == "Equal":
                    pass
                else:
                    print(constr.Type)
                    raise RuntimeError(f"Unknown constraint type {constr.Type} at sketch unparse")


        return text

    def get_vector(self, vector, numbers, var_name, vectors, vectors_text):
        start_point = vectors.get(str(vector), None)
        if not start_point:
            numbers["vector"] += 1
            v_n = numbers["vector"]
            vector_var_name = f"{var_name}_vector_{v_n}"
            vectors_text.append(f"{vector_var_name} = App." + str(vector))
            vectors[str(vector)] = vector_var_name
            start_point = vector_var_name
        return start_point


d = FreeCAD.open('left_y_motor_plate.FCStd')
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
    else:
        raise RuntimeError(f"Unknown TypeId {obj.TypeId} on top-level")

for body in bodies:
    text = body.unparse()
    print("\n".join(text))




