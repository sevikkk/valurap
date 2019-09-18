
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
body_left_z_rod_support_debug = False
body_left_z_rod_support = App.activeDocument().addObject('PartDesign::Body', 'left_z_rod_support')
body_left_z_rod_support.Label = 'left_z_rod_support'
obj_framefrontvslot_bind = body_left_z_rod_support.newObject('PartDesign::ShapeBinder', 'FrameFrontVSlot_bind')
obj_framefrontvslot_bind_orig = App.getDocument('frame').getObject('FrameFrontVSlot')
obj_framefrontvslot_bind.TraceSupport = False
obj_framefrontvslot_bind.Support = [(obj_framefrontvslot_bind_orig, '')]
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_framefrontvslot_bind
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-001-FrameFrontVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFrontVSlot_bind')

obj_frameflvslot_bind = body_left_z_rod_support.newObject('PartDesign::ShapeBinder', 'FrameFLVSlot_bind')
obj_frameflvslot_bind_orig = App.getDocument('frame').getObject('FrameFLVSlot')
obj_frameflvslot_bind.TraceSupport = False
obj_frameflvslot_bind.Support = [(obj_frameflvslot_bind_orig, '')]
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_frameflvslot_bind
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-002-FrameFLVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLVSlot_bind')

obj_frameflbottombb_bind = body_left_z_rod_support.newObject('PartDesign::ShapeBinder', 'FrameFLBottomBB_bind')
obj_frameflbottombb_bind_orig = App.getDocument('frame').getObject('FrameFLBottomBB')
obj_frameflbottombb_bind.TraceSupport = False
obj_frameflbottombb_bind.Support = [(obj_frameflbottombb_bind_orig, '')]
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_frameflbottombb_bind
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-003-FrameFLBottomBB_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLBottomBB_bind')

obj_sketch = body_left_z_rod_support.newObject('Sketcher::SketchObject', 'Sketch')
obj_sketch.Support = (obj_framefrontvslot_bind, ['Face38'])
obj_sketch.MapMode = 'FlatFace'
obj_sketch_vector_1 = App.Vector(-23.500, 59.000, 0.000)
obj_sketch_vector_2 = App.Vector(-16.500, 59.000, 0.000)
obj_sketch_vector_3 = App.Vector(-23.500, 70.000, 0.000)
obj_sketch_vector_4 = App.Vector(-16.500, 70.000, 0.000)
obj_sketch_vector_5 = App.Vector(-30.000, 96.000, 0.000)
obj_sketch_vector_6 = App.Vector(-10.000, 96.000, 0.000)
obj_sketch_vector_7 = App.Vector(-10.000, -20.000, 0.000)
obj_sketch_vector_8 = App.Vector(-30.000, -20.000, 0.000)
obj_sketch_line_1 = Part.LineSegment(obj_sketch_vector_1, obj_sketch_vector_2)
obj_sketch_line_1.Construction = True
obj_sketch_line_2 = Part.LineSegment(obj_sketch_vector_3, obj_sketch_vector_4)
obj_sketch_line_2.Construction = True
obj_sketch_line_3 = Part.LineSegment(obj_sketch_vector_5, obj_sketch_vector_6)
obj_sketch_line_4 = Part.LineSegment(obj_sketch_vector_6, obj_sketch_vector_7)
obj_sketch_line_5 = Part.LineSegment(obj_sketch_vector_8, obj_sketch_vector_5)
obj_sketch_line_6 = Part.LineSegment(obj_sketch_vector_8, obj_sketch_vector_7)
obj_sketch_all_geoms = [obj_sketch_line_1, obj_sketch_line_2, obj_sketch_line_3, obj_sketch_line_4, obj_sketch_line_5, obj_sketch_line_6]
obj_sketch.addGeometry(obj_sketch_all_geoms, False)
obj_sketch_all_ext_geoms = [[obj_frameflbottombb_bind, 'Face1'], [obj_frameflbottombb_bind, 'Face8'], [obj_frameflbottombb_bind, 'Edge7'], [obj_framefrontvslot_bind, 'Edge168'], [obj_frameflvslot_bind, 'Edge170']]
for a, b in obj_sketch_all_ext_geoms:
    obj_sketch.addExternal(a.Name, b)
obj_sketch_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Face8'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Face1'])-3,
    ),
    # 2
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 3
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Edge7'])-3, 2,
        22.0,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Face8'])-3,
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_2),
    ),
    # 6
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Face1'])-3,
    ),
    # 7
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        11.0,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_3),
    ),
    # 11
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_framefrontvslot_bind, 'Edge168'])-3,
    ),
    # 13
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        20.0,
    ),
    # 14
    Sketcher.Constraint('DistanceY',
        -obj_sketch_all_ext_geoms.index([obj_frameflbottombb_bind, 'Edge7'])-3, 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
        15.0,
    ),
    # 15
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflvslot_bind, 'Edge170'])-3,
    ),
    # 16
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 1,
    ),
    # 18
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 20
]
obj_sketch.addConstraint(obj_sketch_constraints)
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_sketch
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-004-Sketch.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch')

obj_pad = body_left_z_rod_support.newObject('PartDesign::Pad', 'Pad')
obj_pad.Label = 'Pad'
obj_pad.Profile = (obj_sketch, [])
obj_pad.Length = '6 mm'
obj_pad.Length2 = '100 mm'
obj_pad.Type = 'Length'
obj_pad.Reversed = False
obj_pad.Midplane = False
obj_pad.Offset = '0 mm'
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_pad
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-005-Pad.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad')

obj_fillet = body_left_z_rod_support.newObject('PartDesign::Fillet', 'Fillet')
obj_fillet.Label = 'Fillet'
obj_fillet.BaseFeature = obj_pad
obj_fillet.Radius = '5 mm'
obj_fillet.Base = (obj_pad, ['Edge5', 'Edge8', 'Edge1', 'Edge2'])
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_fillet
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-006-Fillet.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Fillet')

obj_sketch001 = body_left_z_rod_support.newObject('Sketcher::SketchObject', 'Sketch001')
obj_sketch001.Support = (obj_fillet, ['Face5'])
obj_sketch001.MapMode = 'FlatFace'
obj_sketch001_vector_1 = App.Vector(-30.000, 85.000, 0.000)
obj_sketch001_vector_2 = App.Vector(-10.000, 85.000, 0.000)
obj_sketch001_vector_3 = App.Vector(-10.000, 55.000, 0.000)
obj_sketch001_vector_4 = App.Vector(-30.000, 55.000, 0.000)
obj_sketch001_vector_5 = App.Vector(-30.000, 91.000, 0.000)
obj_sketch001_vector_6 = App.Vector(-30.000, -15.000, 0.000)
obj_sketch001_line_1 = Part.LineSegment(obj_sketch001_vector_1, obj_sketch001_vector_2)
obj_sketch001_line_2 = Part.LineSegment(obj_sketch001_vector_2, obj_sketch001_vector_3)
obj_sketch001_line_3 = Part.LineSegment(obj_sketch001_vector_3, obj_sketch001_vector_4)
obj_sketch001_line_4 = Part.LineSegment(obj_sketch001_vector_4, obj_sketch001_vector_1)
obj_sketch001_line_5 = Part.LineSegment(obj_sketch001_vector_5, obj_sketch001_vector_1)
obj_sketch001_line_5.Construction = True
obj_sketch001_line_6 = Part.LineSegment(obj_sketch001_vector_4, obj_sketch001_vector_6)
obj_sketch001_line_6.Construction = True
obj_sketch001_all_geoms = [obj_sketch001_line_1, obj_sketch001_line_2, obj_sketch001_line_3, obj_sketch001_line_4, obj_sketch001_line_5, obj_sketch001_line_6]
obj_sketch001.addGeometry(obj_sketch001_all_geoms, False)
obj_sketch001_all_ext_geoms = [[obj_fillet, 'Edge16'], [obj_fillet, 'Edge17'], [obj_frameflbottombb_bind, 'Edge7']]
for a, b in obj_sketch001_all_ext_geoms:
    obj_sketch001.addExternal(a.Name, b)
obj_sketch001_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4),
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        -obj_sketch001_all_ext_geoms.index([obj_fillet, 'Edge16'])-3,
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
        -obj_sketch001_all_ext_geoms.index([obj_fillet, 'Edge17'])-3,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        -obj_sketch001_all_ext_geoms.index([obj_fillet, 'Edge16'])-3, 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
    ),
    # 12
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 1,
        -obj_sketch001_all_ext_geoms.index([obj_fillet, 'Edge16'])-3, 2,
    ),
    # 13
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
    ),
    # 14
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        30.0,
    ),
    # 15
    Sketcher.Constraint('DistanceY',
        -obj_sketch001_all_ext_geoms.index([obj_frameflbottombb_bind, 'Edge7'])-3, 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        4.0,
    ),
    # 16
]
obj_sketch001.addConstraint(obj_sketch001_constraints)
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_sketch001
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-007-Sketch001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch001')

obj_pad001 = body_left_z_rod_support.newObject('PartDesign::Pad', 'Pad001')
obj_pad001.Label = 'Pad001'
obj_pad001.Profile = (obj_sketch001, [])
obj_pad001.Length = '38 mm'
obj_pad001.Length2 = '100 mm'
obj_pad001.Type = 'Length'
obj_pad001.Reversed = False
obj_pad001.Midplane = False
obj_pad001.Offset = '0 mm'
obj_pad001.BaseFeature = obj_fillet
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_pad001
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-008-Pad001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad001')

obj_fillet001 = body_left_z_rod_support.newObject('PartDesign::Fillet', 'Fillet001')
obj_fillet001.Label = 'Fillet001'
obj_fillet001.BaseFeature = obj_pad001
obj_fillet001.Radius = '10 mm'
obj_fillet001.Base = (obj_pad001, ['Edge38', 'Edge32'])
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_fillet001
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-009-Fillet001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Fillet001')

obj_sketch002 = body_left_z_rod_support.newObject('Sketcher::SketchObject', 'Sketch002')
obj_sketch002.Support = (obj_fillet001, ['Face4'])
obj_sketch002.MapMode = 'FlatFace'
obj_sketch002_vector_1 = App.Vector(-10.000, 85.000, 0.000)
obj_sketch002_vector_2 = App.Vector(-30.000, 55.000, 0.000)
obj_sketch002_vector_3 = App.Vector(-10.000, 55.000, 0.000)
obj_sketch002_vector_4 = App.Vector(-30.000, 85.000, 0.000)
obj_sketch002_vector_5 = App.Vector(-20.000, 70.000, 0.000)
obj_sketch002_vector_6 = App.Vector(-20.000, 50.000, 0.000)
obj_sketch002_vector_7 = App.Vector(-20.000, 90.000, 0.000)
obj_sketch002_vector_8 = App.Vector(-20.000, -20.000, 0.000)
obj_sketch002_vector_9 = App.Vector(-20.000, 0.000, 0.000)
obj_sketch002_vector_10 = App.Vector(-20.000, -10.000, 0.000)
obj_sketch002_line_1 = Part.LineSegment(obj_sketch002_vector_1, obj_sketch002_vector_2)
obj_sketch002_line_1.Construction = True
obj_sketch002_line_2 = Part.LineSegment(obj_sketch002_vector_3, obj_sketch002_vector_4)
obj_sketch002_line_2.Construction = True
obj_sketch002_point_1 = Part.Point(obj_sketch002_vector_5)
obj_sketch002_line_3 = Part.LineSegment(obj_sketch002_vector_6, obj_sketch002_vector_7)
obj_sketch002_line_3.Construction = True
obj_sketch002_circle_1 = Part.Circle(obj_sketch002_vector_7, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch002_circle_2 = Part.Circle(obj_sketch002_vector_6, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch002_point_2 = Part.Point(obj_sketch002_vector_8)
obj_sketch002_point_3 = Part.Point(obj_sketch002_vector_9)
obj_sketch002_circle_3 = Part.Circle(obj_sketch002_vector_10, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch002_all_geoms = [obj_sketch002_line_1, obj_sketch002_line_2, obj_sketch002_point_1, obj_sketch002_line_3, obj_sketch002_circle_1, obj_sketch002_circle_2, obj_sketch002_point_2, obj_sketch002_point_3, obj_sketch002_circle_3]
obj_sketch002.addGeometry(obj_sketch002_all_geoms, False)
obj_sketch002_all_ext_geoms = [[obj_fillet001, 'Edge3'], [obj_sketch001, 'Edge3'], [obj_frameflvslot_bind, 'Face38'], [obj_frameflvslot_bind, 'Face25']]
for a, b in obj_sketch002_all_ext_geoms:
    obj_sketch002.addExternal(a.Name, b)
obj_sketch002_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_2),
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1),
    ),
    # 2
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3),
    ),
    # 3
    Sketcher.Constraint('Symmetric',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
    ),
    # 4
    Sketcher.Constraint('DistanceY',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        40.0,
    ),
    # 5
    Sketcher.Constraint('Radius',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 2.6,
    ),
    # 6
    Sketcher.Constraint('Equal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2),
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1),
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        -obj_sketch002_all_ext_geoms.index([obj_fillet001, 'Edge3'])-3, 2,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 2,
        -obj_sketch002_all_ext_geoms.index([obj_fillet001, 'Edge3'])-3, 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        -obj_sketch002_all_ext_geoms.index([obj_sketch001, 'Edge3'])-3, 2,
    ),
    # 12
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 1,
        -obj_sketch002_all_ext_geoms.index([obj_sketch001, 'Edge3'])-3, 1,
    ),
    # 13
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_point_3), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
    ),
    # 14
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_point_2), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_point_3), 1,
    ),
    # 15
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_3), 1,
        -obj_sketch002_all_ext_geoms.index([obj_frameflvslot_bind, 'Face25'])-3,
    ),
    # 16
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_2), 1,
        -obj_sketch002_all_ext_geoms.index([obj_frameflvslot_bind, 'Face38'])-3,
    ),
    # 17
    Sketcher.Constraint('Symmetric',
        obj_sketch002_all_geoms.index(obj_sketch002_point_3), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_point_2), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_3), 3,
    ),
    # 18
    Sketcher.Constraint('Equal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_3),
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2),
    ),
    # 19
]
obj_sketch002.addConstraint(obj_sketch002_constraints)
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_sketch002
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-010-Sketch002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch002')

obj_pocket = body_left_z_rod_support.newObject('PartDesign::Pocket', 'Pocket')
obj_pocket.Label = 'Pocket'
obj_pocket.Profile = (obj_sketch002, [])
obj_pocket.Length = '6 mm'
obj_pocket.Length2 = '100 mm'
obj_pocket.Type = 'Length'
obj_pocket.Reversed = False
obj_pocket.Midplane = False
obj_pocket.Offset = '0 mm'
obj_pocket.BaseFeature = obj_fillet001
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_pocket
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-011-Pocket.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket')

obj_sketch003 = body_left_z_rod_support.newObject('Sketcher::SketchObject', 'Sketch003')
obj_sketch003.Support = (obj_pocket, ['Face2'])
obj_sketch003.MapMode = 'FlatFace'
obj_sketch003_vector_1 = App.Vector(37.000, 81.000, 0.000)
obj_sketch003_vector_2 = App.Vector(37.000, 59.000, 0.000)
obj_sketch003_vector_3 = App.Vector(37.000, 70.000, 0.000)
obj_sketch003_line_1 = Part.LineSegment(obj_sketch003_vector_1, obj_sketch003_vector_2)
obj_sketch003_line_1.Construction = True
obj_sketch003_point_1 = Part.Point(obj_sketch003_vector_3)
obj_sketch003_circle_1 = Part.Circle(obj_sketch003_vector_3, App.Vector (0.0, 0.0, 1.0), 7.0)
obj_sketch003_all_geoms = [obj_sketch003_line_1, obj_sketch003_point_1, obj_sketch003_circle_1]
obj_sketch003.addGeometry(obj_sketch003_all_geoms, False)
obj_sketch003_all_ext_geoms = [[obj_frameflbottombb_bind, 'Edge7']]
for a, b in obj_sketch003_all_ext_geoms:
    obj_sketch003.addExternal(a.Name, b)
obj_sketch003_constraints = [
    Sketcher.Constraint('Coincident',
        -obj_sketch003_all_ext_geoms.index([obj_frameflbottombb_bind, 'Edge7'])-3, 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
    ),
    # 1
    Sketcher.Constraint('DistanceY',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
        22.0,
    ),
    # 2
    Sketcher.Constraint('Vertical',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 3
    Sketcher.Constraint('Symmetric',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
    ),
    # 4
    Sketcher.Constraint('Radius',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 7.0,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
    ),
    # 6
]
obj_sketch003.addConstraint(obj_sketch003_constraints)
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_sketch003
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket, obj_sketch003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-012-Sketch003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch003')

obj_pocket001 = body_left_z_rod_support.newObject('PartDesign::Pocket', 'Pocket001')
obj_pocket001.Label = 'Pocket001'
obj_pocket001.Profile = (obj_sketch003, [])
obj_pocket001.Length = '20 mm'
obj_pocket001.Length2 = '100 mm'
obj_pocket001.Type = 'Length'
obj_pocket001.Reversed = False
obj_pocket001.Midplane = False
obj_pocket001.Offset = '0 mm'
obj_pocket001.BaseFeature = obj_pocket
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_pocket001
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-013-Pocket001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket001')

obj_sketch004 = body_left_z_rod_support.newObject('Sketcher::SketchObject', 'Sketch004')
obj_sketch004.Support = (obj_pocket001, ['Face2'])
obj_sketch004.MapMode = 'FlatFace'
obj_sketch004_vector_1 = App.Vector(37.000, 70.000, 0.000)
obj_sketch004_circle_1 = Part.Circle(obj_sketch004_vector_1, App.Vector (0.0, 0.0, 1.0), 11.5)
obj_sketch004_all_geoms = [obj_sketch004_circle_1]
obj_sketch004.addGeometry(obj_sketch004_all_geoms, False)
obj_sketch004_all_ext_geoms = [[obj_pocket001, 'Edge10']]
for a, b in obj_sketch004_all_ext_geoms:
    obj_sketch004.addExternal(a.Name, b)
obj_sketch004_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_circle_1), 3,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge10'])-3, 3,
    ),
    # 1
    Sketcher.Constraint('Radius',
        obj_sketch004_all_geoms.index(obj_sketch004_circle_1), 11.5,
    ),
    # 2
]
obj_sketch004.addConstraint(obj_sketch004_constraints)
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_sketch004
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-014-Sketch004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch004')

obj_pocket002 = body_left_z_rod_support.newObject('PartDesign::Pocket', 'Pocket002')
obj_pocket002.Label = 'Pocket002'
obj_pocket002.Profile = (obj_sketch004, [])
obj_pocket002.Length = '8 mm'
obj_pocket002.Length2 = '100 mm'
obj_pocket002.Type = 'Length'
obj_pocket002.Reversed = False
obj_pocket002.Midplane = False
obj_pocket002.Offset = '0 mm'
obj_pocket002.BaseFeature = obj_pocket001
if body_left_z_rod_support_debug:
    body_left_z_rod_support.Tip = obj_pocket002
    body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_support-015-Pocket002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket002')

body_left_z_rod_support.Group = [obj_framefrontvslot_bind, obj_frameflvslot_bind, obj_frameflbottombb_bind, obj_sketch, obj_pad, obj_fillet, obj_sketch001, obj_pad001, obj_fillet001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002]
body_left_z_rod_support.Tip = obj_pocket002
FreeCAD.ActiveDocument.recompute()
Part.export([body_left_z_rod_support], 'left_z_rod_support.brep')

App.ActiveDocument.saveAs("plate.FCStd")
