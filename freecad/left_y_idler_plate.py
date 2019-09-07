
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
body_left_y_idler_plate_debug = False
body_left_y_idler_plate = App.activeDocument().addObject('PartDesign::Body', 'left_y_idler_plate')
body_left_y_idler_plate.Label = 'left_y_idler_plate'
obj_backvslot_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'BackVSlot_bind')
obj_backvslot_bind_orig = App.getDocument('frame').getObject('BackVSlot')
obj_backvslot_bind.TraceSupport = False
obj_backvslot_bind.Support = [(obj_backvslot_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_backvslot_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-001-BackVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('BackVSlot_bind')

obj_leftvslot_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'LeftVSlot_bind')
obj_leftvslot_bind_orig = App.getDocument('frame').getObject('LeftVSlot')
obj_leftvslot_bind.TraceSupport = False
obj_leftvslot_bind.Support = [(obj_leftvslot_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_leftvslot_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-002-LeftVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftVSlot_bind')

obj_leftrail_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'LeftRail_bind')
obj_leftrail_bind_orig = App.getDocument('frame').getObject('LeftRail')
obj_leftrail_bind.TraceSupport = False
obj_leftrail_bind.Support = [(obj_leftrail_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_leftrail_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-003-LeftRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftRail_bind')

obj_leftidler_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'LeftIdler_bind')
obj_leftidler_bind_orig = App.getDocument('frame').getObject('LeftIdler')
obj_leftidler_bind.TraceSupport = False
obj_leftidler_bind.Support = [(obj_leftidler_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_leftidler_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-004-LeftIdler_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftIdler_bind')

obj_frameblmotor_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'FrameBLMotor_bind')
obj_frameblmotor_bind_orig = App.getDocument('frame').getObject('FrameBLMotor')
obj_frameblmotor_bind.TraceSupport = False
obj_frameblmotor_bind.Support = [(obj_frameblmotor_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_frameblmotor_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-005-FrameBLMotor_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameBLMotor_bind')

obj_framebltopbb_bind = body_left_y_idler_plate.newObject('PartDesign::ShapeBinder', 'FrameBLTopBB_bind')
obj_framebltopbb_bind_orig = App.getDocument('frame').getObject('FrameBLTopBB')
obj_framebltopbb_bind.TraceSupport = False
obj_framebltopbb_bind.Support = [(obj_framebltopbb_bind_orig, '')]
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_framebltopbb_bind
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-006-FrameBLTopBB_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameBLTopBB_bind')

obj_sketch = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch')
obj_sketch.Support = (obj_backvslot_bind, ['Face86'])
obj_sketch.MapMode = 'FlatFace'
obj_sketch_vector_1 = App.Vector(35.000, 96.150, 0.000)
obj_sketch_vector_2 = App.Vector(35.000, 91.150, 0.000)
obj_sketch_vector_3 = App.Vector(-10.000, -34.750, 0.000)
obj_sketch_vector_4 = App.Vector(-10.000, -39.750, 0.000)
obj_sketch_vector_5 = App.Vector(55.000, 91.150, 0.000)
obj_sketch_vector_6 = App.Vector(55.000, 96.150, 0.000)
obj_sketch_vector_7 = App.Vector(-10.000, 96.150, 0.000)
obj_sketch_vector_8 = App.Vector(55.000, -39.750, 0.000)
obj_sketch_point_1 = Part.Point(obj_sketch_vector_1)
obj_sketch_point_2 = Part.Point(obj_sketch_vector_2)
obj_sketch_line_1 = Part.LineSegment(obj_sketch_vector_1, obj_sketch_vector_2)
obj_sketch_line_1.Construction = True
obj_sketch_point_3 = Part.Point(obj_sketch_vector_3)
obj_sketch_point_4 = Part.Point(obj_sketch_vector_4)
obj_sketch_line_2 = Part.LineSegment(obj_sketch_vector_4, obj_sketch_vector_3)
obj_sketch_line_2.Construction = True
obj_sketch_point_5 = Part.Point(obj_sketch_vector_5)
obj_sketch_line_3 = Part.LineSegment(obj_sketch_vector_6, obj_sketch_vector_7)
obj_sketch_line_4 = Part.LineSegment(obj_sketch_vector_7, obj_sketch_vector_4)
obj_sketch_line_5 = Part.LineSegment(obj_sketch_vector_4, obj_sketch_vector_8)
obj_sketch_line_6 = Part.LineSegment(obj_sketch_vector_8, obj_sketch_vector_6)
obj_sketch_all_geoms = [obj_sketch_point_1, obj_sketch_point_2, obj_sketch_line_1, obj_sketch_point_3, obj_sketch_point_4, obj_sketch_line_2, obj_sketch_point_5, obj_sketch_line_3, obj_sketch_line_4, obj_sketch_line_5, obj_sketch_line_6]
obj_sketch.addGeometry(obj_sketch_all_geoms, False)
obj_sketch_all_ext_geoms = [[obj_frameblmotor_bind, 'Face4'], [obj_frameblmotor_bind, 'Face12'], [obj_frameblmotor_bind, 'Face8'], [obj_backvslot_bind, 'Face5'], [obj_leftvslot_bind, 'Face86'], [obj_leftidler_bind, 'Face45'], [obj_leftidler_bind, 'Face49'], [obj_leftidler_bind, 'Edge64'], [obj_leftidler_bind, 'Edge62']]
for a, b in obj_sketch_all_ext_geoms:
    obj_sketch.addExternal(a.Name, b)
obj_sketch_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameblmotor_bind, 'Face4'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameblmotor_bind, 'Face12'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameblmotor_bind, 'Face12'])-3,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
    ),
    # 5
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        5.0,
    ),
    # 6
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftidler_bind, 'Face49'])-3,
    ),
    # 7
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_backvslot_bind, 'Face5'])-3,
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_4), 1,
        -obj_sketch_all_ext_geoms.index([obj_backvslot_bind, 'Face5'])-3,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_4), 1,
    ),
    # 11
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_line_1),
        obj_sketch_all_geoms.index(obj_sketch_line_2),
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_5), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameblmotor_bind, 'Face4'])-3,
    ),
    # 13
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_5), 1,
        20.0,
    ),
    # 14
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 1,
    ),
    # 15
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
    ),
    # 16
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 1,
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
    ),
    # 18
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_3),
    ),
    # 19
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 20
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 21
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_4), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 23
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        -obj_sketch_all_ext_geoms.index([obj_backvslot_bind, 'Face5'])-3,
    ),
    # 24
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_3),
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_5), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 26
]
obj_sketch.addConstraint(obj_sketch_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-007-Sketch.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch')

obj_pad = body_left_y_idler_plate.newObject('PartDesign::Pad', 'Pad')
obj_pad.Label = 'Pad'
obj_pad.Profile = (obj_sketch, [])
obj_pad.Length = '5 mm'
obj_pad.Length2 = '100 mm'
obj_pad.Type = 'Length'
obj_pad.UpToFace = None
obj_pad.Reversed = False
obj_pad.Midplane = False
obj_pad.Offset = '0 mm'
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pad
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-008-Pad.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad')

obj_sketch001 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch001')
obj_sketch001.Support = (obj_pad, ['Face6'])
obj_sketch001.MapMode = 'FlatFace'
obj_sketch001_vector_1 = App.Vector(29.401, -26.450, 0.000)
obj_sketch001_vector_2 = App.Vector(30.599, -34.050, 0.000)
obj_sketch001_vector_3 = App.Vector(30.599, -26.450, 0.000)
obj_sketch001_vector_4 = App.Vector(29.401, -34.050, 0.000)
obj_sketch001_vector_5 = App.Vector(30.000, -30.250, 0.000)
obj_sketch001_vector_6 = App.Vector(14.000, -20.750, 0.000)
obj_sketch001_vector_7 = App.Vector(46.000, -20.750, 0.000)
obj_sketch001_vector_8 = App.Vector(46.000, -39.750, 0.000)
obj_sketch001_vector_9 = App.Vector(14.000, -39.750, 0.000)
obj_sketch001_line_1 = Part.LineSegment(obj_sketch001_vector_1, obj_sketch001_vector_2)
obj_sketch001_line_1.Construction = True
obj_sketch001_line_2 = Part.LineSegment(obj_sketch001_vector_3, obj_sketch001_vector_4)
obj_sketch001_line_2.Construction = True
obj_sketch001_point_1 = Part.Point(obj_sketch001_vector_5)
obj_sketch001_line_3 = Part.LineSegment(obj_sketch001_vector_6, obj_sketch001_vector_7)
obj_sketch001_line_4 = Part.LineSegment(obj_sketch001_vector_7, obj_sketch001_vector_8)
obj_sketch001_line_5 = Part.LineSegment(obj_sketch001_vector_8, obj_sketch001_vector_9)
obj_sketch001_line_6 = Part.LineSegment(obj_sketch001_vector_9, obj_sketch001_vector_6)
obj_sketch001_all_geoms = [obj_sketch001_line_1, obj_sketch001_line_2, obj_sketch001_point_1, obj_sketch001_line_3, obj_sketch001_line_4, obj_sketch001_line_5, obj_sketch001_line_6]
obj_sketch001.addGeometry(obj_sketch001_all_geoms, False)
obj_sketch001_all_ext_geoms = [[obj_leftidler_bind, 'Face49'], [obj_leftidler_bind, 'Face45'], [obj_leftidler_bind, 'Edge62'], [obj_leftidler_bind, 'Edge64'], [obj_pad, 'Edge10']]
for a, b in obj_sketch001_all_ext_geoms:
    obj_sketch001.addExternal(a.Name, b)
obj_sketch001_constraints = [
    Sketcher.Constraint('Coincident',
        -obj_sketch001_all_ext_geoms.index([obj_leftidler_bind, 'Edge62'])-3, 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        -obj_sketch001_all_ext_geoms.index([obj_leftidler_bind, 'Edge64'])-3, 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        -obj_sketch001_all_ext_geoms.index([obj_leftidler_bind, 'Edge62'])-3, 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftidler_bind, 'Edge64'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1),
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 1,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 1,
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3),
    ),
    # 11
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4),
    ),
    # 12
    Sketcher.Constraint('Symmetric',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
    ),
    # 13
    Sketcher.Constraint('Symmetric',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
    ),
    # 14
    Sketcher.Constraint('DistanceX',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        32.0,
    ),
    # 15
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge10'])-3,
    ),
    # 16
]
obj_sketch001.addConstraint(obj_sketch001_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch001
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-009-Sketch001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch001')

obj_pad001 = body_left_y_idler_plate.newObject('PartDesign::Pad', 'Pad001')
obj_pad001.Label = 'Pad001'
obj_pad001.Profile = (obj_sketch001, [])
obj_pad001.Length = '40 mm'
obj_pad001.Length2 = '100 mm'
obj_pad001.Type = 'Length'
obj_pad001.UpToFace = None
obj_pad001.Reversed = False
obj_pad001.Midplane = False
obj_pad001.Offset = '0 mm'
obj_pad001.BaseFeature = obj_pad
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pad001
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-010-Pad001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad001')

obj_sketch002 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch002')
obj_sketch002.Support = (obj_pad001, ['Face11'])
obj_sketch002.MapMode = 'FlatFace'
obj_sketch002_vector_1 = App.Vector(18.804, -25.566, 0.000)
obj_sketch002_vector_2 = App.Vector(41.196, -25.566, 0.000)
obj_sketch002_vector_3 = App.Vector(41.196, -34.934, 0.000)
obj_sketch002_vector_4 = App.Vector(18.804, -34.934, 0.000)
obj_sketch002_vector_5 = App.Vector(14.000, -20.750, 0.000)
obj_sketch002_vector_6 = App.Vector(46.000, -39.750, 0.000)
obj_sketch002_vector_7 = App.Vector(46.000, -20.750, 0.000)
obj_sketch002_vector_8 = App.Vector(14.000, -39.750, 0.000)
obj_sketch002_vector_9 = App.Vector(30.000, -30.250, 0.000)
obj_sketch002_line_1 = Part.LineSegment(obj_sketch002_vector_1, obj_sketch002_vector_2)
obj_sketch002_line_2 = Part.LineSegment(obj_sketch002_vector_2, obj_sketch002_vector_3)
obj_sketch002_line_3 = Part.LineSegment(obj_sketch002_vector_3, obj_sketch002_vector_4)
obj_sketch002_line_4 = Part.LineSegment(obj_sketch002_vector_4, obj_sketch002_vector_1)
obj_sketch002_line_5 = Part.LineSegment(obj_sketch002_vector_5, obj_sketch002_vector_6)
obj_sketch002_line_5.Construction = True
obj_sketch002_line_6 = Part.LineSegment(obj_sketch002_vector_7, obj_sketch002_vector_8)
obj_sketch002_line_6.Construction = True
obj_sketch002_point_1 = Part.Point(obj_sketch002_vector_9)
obj_sketch002_all_geoms = [obj_sketch002_line_1, obj_sketch002_line_2, obj_sketch002_line_3, obj_sketch002_line_4, obj_sketch002_line_5, obj_sketch002_line_6, obj_sketch002_point_1]
obj_sketch002.addGeometry(obj_sketch002_all_geoms, False)
obj_sketch002_all_ext_geoms = [[obj_pad001, 'Edge22'], [obj_pad001, 'Edge25']]
for a, b in obj_sketch002_all_ext_geoms:
    obj_sketch002.addExternal(a.Name, b)
obj_sketch002_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_4), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_line_4),
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 1,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge22'])-3, 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_6), 1,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge22'])-3, 2,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 2,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge25'])-3, 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_6), 2,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge25'])-3, 2,
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_5),
    ),
    # 13
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_6),
    ),
    # 14
    Sketcher.Constraint('Symmetric',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
    ),
    # 15
    Sketcher.Constraint('DistanceY',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        9.367815,
    ),
    # 16
    Sketcher.Constraint('DistanceX',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        22.392282,
    ),
    # 17
]
obj_sketch002.addConstraint(obj_sketch002_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch002
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-011-Sketch002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch002')

obj_pocket = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket')
obj_pocket.Label = 'Pocket'
obj_pocket.Profile = (obj_sketch002, [])
obj_pocket.Length = '70 mm'
obj_pocket.Length2 = '100 mm'
obj_pocket.Type = 'Length'
obj_pocket.UpToFace = None
obj_pocket.Reversed = False
obj_pocket.Midplane = False
obj_pocket.Offset = '0 mm'
obj_pocket.BaseFeature = obj_pad001
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-012-Pocket.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket')

obj_sketch003 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch003')
obj_sketch003.Support = (obj_pocket, ['Face14'])
obj_sketch003.MapMode = 'FlatFace'
obj_sketch003_vector_1 = App.Vector(-30.000, -20.000, 0.000)
obj_sketch003_vector_2 = App.Vector(-30.000, -15.000, 0.000)
obj_sketch003_vector_3 = App.Vector(-30.000, -55.000, 0.000)
obj_sketch003_vector_4 = App.Vector(-30.000, -40.000, 0.000)
obj_sketch003_vector_5 = App.Vector(-30.000, -25.000, 0.000)
obj_sketch003_vector_6 = App.Vector(-30.000, -30.000, 0.000)
obj_sketch003_vector_7 = App.Vector(-30.000, -35.000, 0.000)
obj_sketch003_circle_1 = Part.Circle(obj_sketch003_vector_1, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_line_1 = Part.LineSegment(obj_sketch003_vector_2, obj_sketch003_vector_3)
obj_sketch003_line_1.Construction = True
obj_sketch003_point_1 = Part.Point(obj_sketch003_vector_4)
obj_sketch003_circle_2 = Part.Circle(obj_sketch003_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_circle_3 = Part.Circle(obj_sketch003_vector_5, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_circle_4 = Part.Circle(obj_sketch003_vector_6, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_circle_5 = Part.Circle(obj_sketch003_vector_7, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_line_2 = Part.LineSegment(obj_sketch003_vector_1, obj_sketch003_vector_5)
obj_sketch003_line_2.Construction = True
obj_sketch003_line_3 = Part.LineSegment(obj_sketch003_vector_5, obj_sketch003_vector_6)
obj_sketch003_line_3.Construction = True
obj_sketch003_line_4 = Part.LineSegment(obj_sketch003_vector_6, obj_sketch003_vector_7)
obj_sketch003_line_4.Construction = True
obj_sketch003_line_5 = Part.LineSegment(obj_sketch003_vector_7, obj_sketch003_vector_4)
obj_sketch003_line_5.Construction = True
obj_sketch003_all_geoms = [obj_sketch003_circle_1, obj_sketch003_line_1, obj_sketch003_point_1, obj_sketch003_circle_2, obj_sketch003_circle_3, obj_sketch003_circle_4, obj_sketch003_circle_5, obj_sketch003_line_2, obj_sketch003_line_3, obj_sketch003_line_4, obj_sketch003_line_5]
obj_sketch003.addGeometry(obj_sketch003_all_geoms, False)
obj_sketch003_all_ext_geoms = [[obj_pocket, 'Edge21'], [obj_pocket, 'Edge37']]
for a, b in obj_sketch003_all_ext_geoms:
    obj_sketch003.addExternal(a.Name, b)
obj_sketch003_constraints = [
    Sketcher.Constraint('Symmetric',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge21'])-3, 1,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge21'])-3, 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 0,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge21'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge37'])-3,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 4
    Sketcher.Constraint('DistanceY',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 3,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge21'])-3, 1,
        5.0,
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 6
    Sketcher.Constraint('DistanceY',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
        15.0,
    ),
    # 7
    Sketcher.Constraint('Radius',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 1.6,
    ),
    # 8
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_2),
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1),
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_2), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
    ),
    # 10
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_3), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 11
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_4), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_5), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 13
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_3),
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1),
    ),
    # 14
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1),
        obj_sketch003_all_geoms.index(obj_sketch003_circle_4),
    ),
    # 15
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_4),
        obj_sketch003_all_geoms.index(obj_sketch003_circle_5),
    ),
    # 16
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 1,
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_4), 1,
    ),
    # 18
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_4), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_5), 1,
    ),
    # 19
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2),
        obj_sketch003_all_geoms.index(obj_sketch003_line_3),
    ),
    # 20
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_line_3),
        obj_sketch003_all_geoms.index(obj_sketch003_line_4),
    ),
    # 21
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_line_4),
        obj_sketch003_all_geoms.index(obj_sketch003_line_5),
    ),
    # 22
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_5), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_point_1), 1,
    ),
    # 23
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_5), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_4), 2,
    ),
    # 24
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_4), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 2,
    ),
    # 25
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 3,
    ),
    # 26
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_3), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
    ),
    # 27
]
obj_sketch003.addConstraint(obj_sketch003_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch003
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-013-Sketch003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch003')

obj_pocket001 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket001')
obj_pocket001.Label = 'Pocket001'
obj_pocket001.Profile = (obj_sketch003, [])
obj_pocket001.Length = '50 mm'
obj_pocket001.Length2 = '100 mm'
obj_pocket001.Type = 'Length'
obj_pocket001.UpToFace = None
obj_pocket001.Reversed = False
obj_pocket001.Midplane = False
obj_pocket001.Offset = '0 mm'
obj_pocket001.BaseFeature = obj_pocket
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket001
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-014-Pocket001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket001')

obj_sketch004 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch004')
obj_sketch004.Support = (obj_pocket001, ['Face5'])
obj_sketch004.MapMode = 'FlatFace'
obj_sketch004_vector_1 = App.Vector(35.000, 91.150, 0.000)
obj_sketch004_vector_2 = App.Vector(35.000, 48.850, 0.000)
obj_sketch004_vector_3 = App.Vector(30.000, 43.850, 0.000)
obj_sketch004_vector_4 = App.Vector(55.000, 96.150, 0.000)
obj_sketch004_vector_5 = App.Vector(30.000, 96.150, 0.000)
obj_sketch004_vector_6 = App.Vector(55.000, 43.850, 0.000)
obj_sketch004_vector_7 = App.Vector(55.000, 48.850, 0.000)
obj_sketch004_vector_8 = App.Vector(55.000, 91.150, 0.000)
obj_sketch004_point_1 = Part.Point(obj_sketch004_vector_1)
obj_sketch004_point_2 = Part.Point(obj_sketch004_vector_2)
obj_sketch004_point_3 = Part.Point(obj_sketch004_vector_3)
obj_sketch004_line_1 = Part.LineSegment(obj_sketch004_vector_4, obj_sketch004_vector_5)
obj_sketch004_line_2 = Part.LineSegment(obj_sketch004_vector_5, obj_sketch004_vector_3)
obj_sketch004_line_3 = Part.LineSegment(obj_sketch004_vector_3, obj_sketch004_vector_6)
obj_sketch004_line_4 = Part.LineSegment(obj_sketch004_vector_6, obj_sketch004_vector_7)
obj_sketch004_line_5 = Part.LineSegment(obj_sketch004_vector_7, obj_sketch004_vector_2)
obj_sketch004_line_6 = Part.LineSegment(obj_sketch004_vector_2, obj_sketch004_vector_1)
obj_sketch004_line_7 = Part.LineSegment(obj_sketch004_vector_1, obj_sketch004_vector_8)
obj_sketch004_line_8 = Part.LineSegment(obj_sketch004_vector_8, obj_sketch004_vector_4)
obj_sketch004_all_geoms = [obj_sketch004_point_1, obj_sketch004_point_2, obj_sketch004_point_3, obj_sketch004_line_1, obj_sketch004_line_2, obj_sketch004_line_3, obj_sketch004_line_4, obj_sketch004_line_5, obj_sketch004_line_6, obj_sketch004_line_7, obj_sketch004_line_8]
obj_sketch004.addGeometry(obj_sketch004_all_geoms, False)
obj_sketch004_all_ext_geoms = [[obj_frameblmotor_bind, 'Face8'], [obj_frameblmotor_bind, 'Face12'], [obj_frameblmotor_bind, 'Face4'], [obj_pocket001, 'Edge4'], [obj_pocket001, 'Edge7']]
for a, b in obj_sketch004_all_ext_geoms:
    obj_sketch004.addExternal(a.Name, b)
obj_sketch004_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_point_2), 1,
        -obj_sketch004_all_ext_geoms.index([obj_frameblmotor_bind, 'Face8'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_point_2), 1,
        -obj_sketch004_all_ext_geoms.index([obj_frameblmotor_bind, 'Face12'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_point_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_frameblmotor_bind, 'Face4'])-3,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_point_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_frameblmotor_bind, 'Face12'])-3,
    ),
    # 4
    Sketcher.Constraint('DistanceY',
        obj_sketch004_all_geoms.index(obj_sketch004_point_3), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_point_2), 1,
        5.0,
    ),
    # 5
    Sketcher.Constraint('DistanceX',
        obj_sketch004_all_geoms.index(obj_sketch004_point_3), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_point_2), 1,
        5.0,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 1,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_7), 1,
    ),
    # 12
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_7), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_8), 1,
    ),
    # 13
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_8), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
    ),
    # 14
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5),
    ),
    # 15
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3),
    ),
    # 16
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_7),
    ),
    # 17
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1),
    ),
    # 18
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_8),
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2),
    ),
    # 20
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4),
    ),
    # 21
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_point_2), 1,
    ),
    # 22
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_point_1), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 2,
    ),
    # 23
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge7'])-3, 2,
    ),
    # 24
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_point_3), 1,
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge7'])-3,
    ),
    # 26
]
obj_sketch004.addConstraint(obj_sketch004_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch004
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-015-Sketch004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch004')

obj_pad002 = body_left_y_idler_plate.newObject('PartDesign::Pad', 'Pad002')
obj_pad002.Label = 'Pad002'
obj_pad002.Profile = (obj_sketch004, [])
obj_pad002.Length = '42 mm'
obj_pad002.Length2 = '100 mm'
obj_pad002.Type = 'Length'
obj_pad002.UpToFace = None
obj_pad002.Reversed = False
obj_pad002.Midplane = False
obj_pad002.Offset = '0 mm'
obj_pad002.BaseFeature = obj_pocket001
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pad002
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-016-Pad002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad002')

obj_sketch005 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch005')
obj_sketch005.Support = (obj_pad002, ['Face15'])
obj_sketch005.MapMode = 'FlatFace'
obj_sketch005_vector_1 = App.Vector(57.000, 96.150, 0.000)
obj_sketch005_vector_2 = App.Vector(15.000, 43.850, 0.000)
obj_sketch005_vector_3 = App.Vector(57.000, 43.850, 0.000)
obj_sketch005_vector_4 = App.Vector(15.000, 96.150, 0.000)
obj_sketch005_vector_5 = App.Vector(36.000, 70.000, 0.000)
obj_sketch005_vector_6 = App.Vector(51.500, 85.500, 0.000)
obj_sketch005_vector_7 = App.Vector(20.500, 85.500, 0.000)
obj_sketch005_vector_8 = App.Vector(20.500, 54.500, 0.000)
obj_sketch005_vector_9 = App.Vector(51.500, 54.500, 0.000)
obj_sketch005_line_1 = Part.LineSegment(obj_sketch005_vector_1, obj_sketch005_vector_2)
obj_sketch005_line_1.Construction = True
obj_sketch005_line_2 = Part.LineSegment(obj_sketch005_vector_3, obj_sketch005_vector_4)
obj_sketch005_line_2.Construction = True
obj_sketch005_point_1 = Part.Point(obj_sketch005_vector_5)
obj_sketch005_circle_1 = Part.Circle(obj_sketch005_vector_5, App.Vector (0.0, 0.0, 1.0), 12.0)
obj_sketch005_line_3 = Part.LineSegment(obj_sketch005_vector_6, obj_sketch005_vector_7)
obj_sketch005_line_3.Construction = True
obj_sketch005_line_4 = Part.LineSegment(obj_sketch005_vector_7, obj_sketch005_vector_8)
obj_sketch005_line_4.Construction = True
obj_sketch005_line_5 = Part.LineSegment(obj_sketch005_vector_8, obj_sketch005_vector_9)
obj_sketch005_line_5.Construction = True
obj_sketch005_line_6 = Part.LineSegment(obj_sketch005_vector_9, obj_sketch005_vector_6)
obj_sketch005_line_6.Construction = True
obj_sketch005_circle_2 = Part.Circle(obj_sketch005_vector_6, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_3 = Part.Circle(obj_sketch005_vector_7, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_4 = Part.Circle(obj_sketch005_vector_8, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_5 = Part.Circle(obj_sketch005_vector_9, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_all_geoms = [obj_sketch005_line_1, obj_sketch005_line_2, obj_sketch005_point_1, obj_sketch005_circle_1, obj_sketch005_line_3, obj_sketch005_line_4, obj_sketch005_line_5, obj_sketch005_line_6, obj_sketch005_circle_2, obj_sketch005_circle_3, obj_sketch005_circle_4, obj_sketch005_circle_5]
obj_sketch005.addGeometry(obj_sketch005_all_geoms, False)
obj_sketch005_all_ext_geoms = [[obj_pad002, 'Edge58'], [obj_pad002, 'Edge28']]
for a, b in obj_sketch005_all_ext_geoms:
    obj_sketch005.addExternal(a.Name, b)
obj_sketch005_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_2), 1,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge58'])-3, 2,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 1,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge58'])-3, 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_2), 2,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge28'])-3, 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 2,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge28'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_point_1), 1,
        obj_sketch005_all_geoms.index(obj_sketch005_line_1),
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_point_1), 1,
        obj_sketch005_all_geoms.index(obj_sketch005_line_2),
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_point_1), 1,
    ),
    # 7
    Sketcher.Constraint('Radius',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 12.0,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_5), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_5), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_6), 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_6), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 1,
    ),
    # 12
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3),
    ),
    # 13
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_line_5),
    ),
    # 14
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_line_4),
    ),
    # 15
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_line_6),
    ),
    # 16
    Sketcher.Constraint('Symmetric',
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 1,
        obj_sketch005_all_geoms.index(obj_sketch005_point_1), 1,
    ),
    # 17
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3),
        obj_sketch005_all_geoms.index(obj_sketch005_line_6),
    ),
    # 18
    Sketcher.Constraint('DistanceY',
        obj_sketch005_all_geoms.index(obj_sketch005_line_5), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 1,
        31.0,
    ),
    # 19
    Sketcher.Constraint('Radius',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3), 1.6,
    ),
    # 20
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2),
    ),
    # 21
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5),
    ),
    # 22
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4),
    ),
    # 23
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 2,
    ),
    # 24
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 1,
    ),
    # 25
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_line_5), 2,
    ),
    # 26
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 2,
    ),
    # 27
]
obj_sketch005.addConstraint(obj_sketch005_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch005
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-017-Sketch005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch005')

obj_pocket002 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket002')
obj_pocket002.Label = 'Pocket002'
obj_pocket002.Profile = (obj_sketch005, [])
obj_pocket002.Length = '7 mm'
obj_pocket002.Length2 = '100 mm'
obj_pocket002.Type = 'Length'
obj_pocket002.UpToFace = None
obj_pocket002.Reversed = False
obj_pocket002.Midplane = False
obj_pocket002.Offset = '0 mm'
obj_pocket002.BaseFeature = obj_pad002
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket002
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-018-Pocket002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket002')

obj_sketch006 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch006')
obj_sketch006.Support = (obj_pocket002, ['Face6'])
obj_sketch006.MapMode = 'FlatFace'
obj_sketch006_vector_1 = App.Vector(-10.000, 70.000, 0.000)
obj_sketch006_vector_2 = App.Vector(30.000, 70.000, 0.000)
obj_sketch006_vector_3 = App.Vector(2.000, 84.000, 0.000)
obj_sketch006_vector_4 = App.Vector(-10.000, 84.000, 0.000)
obj_sketch006_vector_5 = App.Vector(-10.000, 56.000, 0.000)
obj_sketch006_vector_6 = App.Vector(2.000, 56.000, 0.000)
obj_sketch006_line_1 = Part.LineSegment(obj_sketch006_vector_1, obj_sketch006_vector_2)
obj_sketch006_line_1.Construction = True
obj_sketch006_line_2 = Part.LineSegment(obj_sketch006_vector_3, obj_sketch006_vector_4)
obj_sketch006_line_3 = Part.LineSegment(obj_sketch006_vector_4, obj_sketch006_vector_5)
obj_sketch006_line_4 = Part.LineSegment(obj_sketch006_vector_5, obj_sketch006_vector_6)
obj_sketch006_line_5 = Part.LineSegment(obj_sketch006_vector_6, obj_sketch006_vector_3)
obj_sketch006_all_geoms = [obj_sketch006_line_1, obj_sketch006_line_2, obj_sketch006_line_3, obj_sketch006_line_4, obj_sketch006_line_5]
obj_sketch006.addGeometry(obj_sketch006_all_geoms, False)
obj_sketch006_all_ext_geoms = [[obj_framebltopbb_bind, 'Face1'], [obj_framebltopbb_bind, 'Face8'], [obj_pocket002, 'Edge14'], [obj_pocket002, 'Edge28']]
for a, b in obj_sketch006_all_ext_geoms:
    obj_sketch006.addExternal(a.Name, b)
obj_sketch006_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge28'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge14'])-3,
    ),
    # 2
    Sketcher.Constraint('Symmetric',
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge28'])-3, 1,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge28'])-3, 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 0,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 1,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 1,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 1,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
    ),
    # 7
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2),
    ),
    # 8
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4),
    ),
    # 9
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3),
    ),
    # 10
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge14'])-3,
    ),
    # 11
    Sketcher.Constraint('Symmetric',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 0,
    ),
    # 12
    Sketcher.Constraint('DistanceX',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
        12.0,
    ),
    # 13
    Sketcher.Constraint('DistanceY',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
        28.0,
    ),
    # 14
]
obj_sketch006.addConstraint(obj_sketch006_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch006
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-019-Sketch006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch006')

obj_pad003 = body_left_y_idler_plate.newObject('PartDesign::Pad', 'Pad003')
obj_pad003.Label = 'Pad003'
obj_pad003.Profile = (obj_sketch006, [])
obj_pad003.Length = '40 mm'
obj_pad003.Length2 = '100 mm'
obj_pad003.Type = 'Length'
obj_pad003.UpToFace = None
obj_pad003.Reversed = False
obj_pad003.Midplane = False
obj_pad003.Offset = '0 mm'
obj_pad003.BaseFeature = obj_pocket002
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pad003
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-020-Pad003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad003')

obj_sketch007 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch007')
obj_sketch007.Support = (obj_pad003, ['Face22'])
obj_sketch007.MapMode = 'FlatFace'
obj_sketch007_vector_1 = App.Vector(-36.000, 70.000, 0.000)
obj_sketch007_vector_2 = App.Vector(-15.000, 70.000, 0.000)
obj_sketch007_line_1 = Part.LineSegment(obj_sketch007_vector_1, obj_sketch007_vector_2)
obj_sketch007_line_1.Construction = True
obj_sketch007_circle_1 = Part.Circle(obj_sketch007_vector_1, App.Vector (0.0, 0.0, 1.0), 11.0)
obj_sketch007_all_geoms = [obj_sketch007_line_1, obj_sketch007_circle_1]
obj_sketch007.addGeometry(obj_sketch007_all_geoms, False)
obj_sketch007_all_ext_geoms = [[obj_pad003, 'Edge30']]
for a, b in obj_sketch007_all_ext_geoms:
    obj_sketch007.addExternal(a.Name, b)
obj_sketch007_constraints = [
    Sketcher.Constraint('Symmetric',
        -obj_sketch007_all_ext_geoms.index([obj_pad003, 'Edge30'])-3, 2,
        -obj_sketch007_all_ext_geoms.index([obj_pad003, 'Edge30'])-3, 1,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
    ),
    # 1
    Sketcher.Constraint('Horizontal',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1),
    ),
    # 2
    Sketcher.Constraint('DistanceX',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 1,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
        21.0,
    ),
    # 3
    Sketcher.Constraint('Radius',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 11.0,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 1,
    ),
    # 5
]
obj_sketch007.addConstraint(obj_sketch007_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch007
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-021-Sketch007.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch007')

obj_pocket003 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket003')
obj_pocket003.Label = 'Pocket003'
obj_pocket003.Profile = (obj_sketch007, [])
obj_pocket003.Length = '8 mm'
obj_pocket003.Length2 = '100 mm'
obj_pocket003.Type = 'Length'
obj_pocket003.UpToFace = None
obj_pocket003.Reversed = False
obj_pocket003.Midplane = False
obj_pocket003.Offset = '0 mm'
obj_pocket003.BaseFeature = obj_pad003
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket003
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-022-Pocket003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket003')

obj_sketch008 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch008')
obj_sketch008.Support = (obj_pocket003, ['Face11'])
obj_sketch008.MapMode = 'FlatFace'
obj_sketch008_vector_1 = App.Vector(36.000, 70.000, 0.000)
obj_sketch008_vector_2 = App.Vector(15.000, 70.000, 0.000)
obj_sketch008_line_1 = Part.LineSegment(obj_sketch008_vector_1, obj_sketch008_vector_2)
obj_sketch008_line_1.Construction = True
obj_sketch008_circle_1 = Part.Circle(obj_sketch008_vector_1, App.Vector (0.0, 0.0, 1.0), 8.0)
obj_sketch008_all_geoms = [obj_sketch008_line_1, obj_sketch008_circle_1]
obj_sketch008.addGeometry(obj_sketch008_all_geoms, False)
obj_sketch008_all_ext_geoms = [[obj_pocket003, 'Edge15']]
for a, b in obj_sketch008_all_ext_geoms:
    obj_sketch008.addExternal(a.Name, b)
obj_sketch008_constraints = [
    Sketcher.Constraint('Symmetric',
        -obj_sketch008_all_ext_geoms.index([obj_pocket003, 'Edge15'])-3, 1,
        -obj_sketch008_all_ext_geoms.index([obj_pocket003, 'Edge15'])-3, 2,
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 2,
    ),
    # 1
    Sketcher.Constraint('Horizontal',
        obj_sketch008_all_geoms.index(obj_sketch008_line_1),
    ),
    # 2
    Sketcher.Constraint('DistanceX',
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 2,
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 1,
        21.0,
    ),
    # 3
    Sketcher.Constraint('Radius',
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 8.0,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 3,
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 1,
    ),
    # 5
]
obj_sketch008.addConstraint(obj_sketch008_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch008
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-023-Sketch008.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch008')

obj_pocket004 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket004')
obj_pocket004.Label = 'Pocket004'
obj_pocket004.Profile = (obj_sketch008, [])
obj_pocket004.Length = '5 mm'
obj_pocket004.Length2 = '100 mm'
obj_pocket004.Type = 'Length'
obj_pocket004.UpToFace = None
obj_pocket004.Reversed = False
obj_pocket004.Midplane = False
obj_pocket004.Offset = '0 mm'
obj_pocket004.BaseFeature = obj_pocket003
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket004
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-024-Pocket004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket004')

obj_sketch009 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch009')
obj_sketch009.Support = (obj_pocket004, ['Face6'])
obj_sketch009.MapMode = 'FlatFace'
obj_sketch009_vector_1 = App.Vector(0.000, 96.150, 0.000)
obj_sketch009_vector_2 = App.Vector(0.000, -39.750, 0.000)
obj_sketch009_vector_3 = App.Vector(20.000, 96.150, 0.000)
obj_sketch009_vector_4 = App.Vector(20.000, -20.000, 0.000)
obj_sketch009_vector_5 = App.Vector(0.000, 84.000, 0.000)
obj_sketch009_vector_6 = App.Vector(0.000, 56.000, 0.000)
obj_sketch009_vector_7 = App.Vector(0.000, 90.075, 0.000)
obj_sketch009_vector_8 = App.Vector(0.000, 49.925, 0.000)
obj_sketch009_vector_9 = App.Vector(20.000, 90.075, 0.000)
obj_sketch009_vector_10 = App.Vector(20.000, 49.925, 0.000)
obj_sketch009_vector_11 = App.Vector(-10.000, -10.000, 0.000)
obj_sketch009_vector_12 = App.Vector(30.000, -10.000, 0.000)
obj_sketch009_vector_13 = App.Vector(0.000, -20.000, 0.000)
obj_sketch009_vector_14 = App.Vector(0.000, -10.000, 0.000)
obj_sketch009_vector_15 = App.Vector(0.000, 0.000, 0.000)
obj_sketch009_vector_16 = App.Vector(20.000, -10.000, 0.000)
obj_sketch009_vector_17 = App.Vector(0.000, 19.963, 0.000)
obj_sketch009_vector_18 = App.Vector(20.000, 19.963, 0.000)
obj_sketch009_line_1 = Part.LineSegment(obj_sketch009_vector_1, obj_sketch009_vector_2)
obj_sketch009_line_1.Construction = True
obj_sketch009_line_2 = Part.LineSegment(obj_sketch009_vector_3, obj_sketch009_vector_4)
obj_sketch009_line_2.Construction = True
obj_sketch009_point_1 = Part.Point(obj_sketch009_vector_5)
obj_sketch009_point_2 = Part.Point(obj_sketch009_vector_6)
obj_sketch009_circle_1 = Part.Circle(obj_sketch009_vector_7, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_line_3 = Part.LineSegment(obj_sketch009_vector_7, obj_sketch009_vector_5)
obj_sketch009_line_3.Construction = True
obj_sketch009_line_4 = Part.LineSegment(obj_sketch009_vector_8, obj_sketch009_vector_6)
obj_sketch009_line_4.Construction = True
obj_sketch009_circle_2 = Part.Circle(obj_sketch009_vector_8, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_circle_3 = Part.Circle(obj_sketch009_vector_9, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_circle_4 = Part.Circle(obj_sketch009_vector_10, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_line_5 = Part.LineSegment(obj_sketch009_vector_11, obj_sketch009_vector_12)
obj_sketch009_line_5.Construction = True
obj_sketch009_point_3 = Part.Point(obj_sketch009_vector_13)
obj_sketch009_point_4 = Part.Point(obj_sketch009_vector_14)
obj_sketch009_point_5 = Part.Point(obj_sketch009_vector_15)
obj_sketch009_circle_5 = Part.Circle(obj_sketch009_vector_16, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_circle_6 = Part.Circle(obj_sketch009_vector_14, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_circle_7 = Part.Circle(obj_sketch009_vector_17, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_circle_8 = Part.Circle(obj_sketch009_vector_18, App.Vector (0.0, 0.0, 1.0), 2.5)
obj_sketch009_all_geoms = [obj_sketch009_line_1, obj_sketch009_line_2, obj_sketch009_point_1, obj_sketch009_point_2, obj_sketch009_circle_1, obj_sketch009_line_3, obj_sketch009_line_4, obj_sketch009_circle_2, obj_sketch009_circle_3, obj_sketch009_circle_4, obj_sketch009_line_5, obj_sketch009_point_3, obj_sketch009_point_4, obj_sketch009_point_5, obj_sketch009_circle_5, obj_sketch009_circle_6, obj_sketch009_circle_7, obj_sketch009_circle_8]
obj_sketch009.addGeometry(obj_sketch009_all_geoms, False)
obj_sketch009_all_ext_geoms = [[obj_leftvslot_bind, 'Face7'], [obj_leftvslot_bind, 'Face5'], [obj_leftvslot_bind, 'Face55'], [obj_backvslot_bind, 'Face27'], [obj_pocket004, 'Edge28'], [obj_pocket004, 'Edge5'], [obj_pocket004, 'Edge31'], [obj_pocket004, 'Edge29']]
for a, b in obj_sketch009_all_ext_geoms:
    obj_sketch009.addExternal(a.Name, b)
obj_sketch009_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 1,
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge5'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 2,
        -obj_sketch009_all_ext_geoms.index([obj_leftvslot_bind, 'Face7'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 2,
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge28'])-3,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 1,
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge5'])-3,
    ),
    # 4
    Sketcher.Constraint('Vertical',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
    ),
    # 5
    Sketcher.Constraint('Vertical',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge5'])-3, 2,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 1,
        10.0,
    ),
    # 7
    Sketcher.Constraint('DistanceX',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 1,
        20.0,
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_2), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_1), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 10
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_1), 1,
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge31'])-3,
    ),
    # 11
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_2), 1,
        -obj_sketch009_all_ext_geoms.index([obj_pocket004, 'Edge29'])-3,
    ),
    # 12
    Sketcher.Constraint('Radius',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 2.5,
    ),
    # 13
    Sketcher.Constraint('Symmetric',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_point_1), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
    ),
    # 14
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_3), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
    ),
    # 15
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_3), 2,
        obj_sketch009_all_geoms.index(obj_sketch009_point_1), 1,
    ),
    # 16
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_4), 2,
        obj_sketch009_all_geoms.index(obj_sketch009_point_2), 1,
    ),
    # 17
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_4), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 18
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_line_3),
        obj_sketch009_all_geoms.index(obj_sketch009_line_4),
    ),
    # 19
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_2), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_4), 1,
    ),
    # 20
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_2),
    ),
    # 21
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_3), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_4), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
    ),
    # 23
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_3),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_4),
    ),
    # 24
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_4),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1),
    ),
    # 25
    Sketcher.Constraint('Horizontal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_2), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_4), 3,
    ),
    # 26
    Sketcher.Constraint('Horizontal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_3), 3,
    ),
    # 27
    Sketcher.Constraint('Horizontal',
        obj_sketch009_all_geoms.index(obj_sketch009_line_5),
    ),
    # 28
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_5), 1,
        -obj_sketch009_all_ext_geoms.index([obj_leftvslot_bind, 'Face5'])-3,
    ),
    # 29
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_line_5), 2,
        -obj_sketch009_all_ext_geoms.index([obj_backvslot_bind, 'Face27'])-3,
    ),
    # 30
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_5), 1,
        -obj_sketch009_all_ext_geoms.index([obj_leftvslot_bind, 'Face55'])-3,
    ),
    # 31
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_4), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_5),
    ),
    # 32
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_3), 1,
        -obj_sketch009_all_ext_geoms.index([obj_leftvslot_bind, 'Face7'])-3,
    ),
    # 33
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_3), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 34
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_point_4), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 35
    Sketcher.Constraint('Symmetric',
        obj_sketch009_all_geoms.index(obj_sketch009_point_5), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_point_3), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_point_4), 1,
    ),
    # 36
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_6),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_5),
    ),
    # 37
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_5),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_4),
    ),
    # 38
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_6), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_point_4), 1,
    ),
    # 39
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_5), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
    ),
    # 40
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_5), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_5),
    ),
    # 41
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_8),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_7),
    ),
    # 42
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_7),
        obj_sketch009_all_geoms.index(obj_sketch009_circle_2),
    ),
    # 43
    Sketcher.Constraint('PointOnObject',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_8), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
    ),
    # 44
    Sketcher.Constraint('Horizontal',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_7), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_8), 3,
    ),
    # 45
    Sketcher.Constraint('Symmetric',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_2), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_point_4), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_7), 3,
    ),
    # 46
]
obj_sketch009.addConstraint(obj_sketch009_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch009
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-025-Sketch009.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch009')

obj_pocket005 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket005')
obj_pocket005.Label = 'Pocket005'
obj_pocket005.Profile = (obj_sketch009, [])
obj_pocket005.Length = '5 mm'
obj_pocket005.Length2 = '100 mm'
obj_pocket005.Type = 'Length'
obj_pocket005.UpToFace = None
obj_pocket005.Reversed = False
obj_pocket005.Midplane = False
obj_pocket005.Offset = '0 mm'
obj_pocket005.BaseFeature = obj_pocket004
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket005
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-026-Pocket005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket005')

obj_sketch010 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch010')
obj_sketch010.Support = (obj_pocket005, ['Face6'])
obj_sketch010.MapMode = 'FlatFace'
obj_sketch010_vector_1 = App.Vector(41.000, -0.750, 0.000)
obj_sketch010_vector_2 = App.Vector(46.000, -0.750, 0.000)
obj_sketch010_vector_3 = App.Vector(46.000, -20.750, 0.000)
obj_sketch010_vector_4 = App.Vector(41.000, -20.750, 0.000)
obj_sketch010_line_1 = Part.LineSegment(obj_sketch010_vector_1, obj_sketch010_vector_2)
obj_sketch010_line_2 = Part.LineSegment(obj_sketch010_vector_2, obj_sketch010_vector_3)
obj_sketch010_line_3 = Part.LineSegment(obj_sketch010_vector_3, obj_sketch010_vector_4)
obj_sketch010_line_4 = Part.LineSegment(obj_sketch010_vector_4, obj_sketch010_vector_1)
obj_sketch010_all_geoms = [obj_sketch010_line_1, obj_sketch010_line_2, obj_sketch010_line_3, obj_sketch010_line_4]
obj_sketch010.addGeometry(obj_sketch010_all_geoms, False)
obj_sketch010_all_ext_geoms = [[obj_pocket005, 'Edge103'], [obj_pocket005, 'Edge105']]
for a, b in obj_sketch010_all_ext_geoms:
    obj_sketch010.addExternal(a.Name, b)
obj_sketch010_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_2), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_3), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_4), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch010_all_geoms.index(obj_sketch010_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch010_all_geoms.index(obj_sketch010_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch010_all_geoms.index(obj_sketch010_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch010_all_geoms.index(obj_sketch010_line_4),
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_2), 2,
        -obj_sketch010_all_ext_geoms.index([obj_pocket005, 'Edge105'])-3, 2,
    ),
    # 9
    Sketcher.Constraint('DistanceX',
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 1,
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 2,
        5.0,
    ),
    # 10
    Sketcher.Constraint('DistanceY',
        obj_sketch010_all_geoms.index(obj_sketch010_line_2), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 2,
        20.0,
    ),
    # 11
]
obj_sketch010.addConstraint(obj_sketch010_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch010
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005, obj_sketch010]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-027-Sketch010.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch010')

obj_pad004 = body_left_y_idler_plate.newObject('PartDesign::Pad', 'Pad004')
obj_pad004.Label = 'Pad004'
obj_pad004.Profile = (obj_sketch010, [])
obj_pad004.Length = '40 mm'
obj_pad004.Length2 = '100 mm'
obj_pad004.Type = 'Length'
obj_pad004.UpToFace = None
obj_pad004.Reversed = False
obj_pad004.Midplane = False
obj_pad004.Offset = '0 mm'
obj_pad004.BaseFeature = obj_pocket005
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pad004
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005, obj_sketch010, obj_pad004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-028-Pad004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad004')

obj_sketch011 = body_left_y_idler_plate.newObject('Sketcher::SketchObject', 'Sketch011')
obj_sketch011.Support = (obj_pad004, ['Face26'])
obj_sketch011.MapMode = 'FlatFace'
obj_sketch011_vector_1 = App.Vector(-55.000, -20.750, 0.000)
obj_sketch011_vector_2 = App.Vector(-55.000, -0.750, 0.000)
obj_sketch011_vector_3 = App.Vector(-15.000, -0.750, 0.000)
obj_sketch011_line_1 = Part.LineSegment(obj_sketch011_vector_1, obj_sketch011_vector_2)
obj_sketch011_line_2 = Part.LineSegment(obj_sketch011_vector_2, obj_sketch011_vector_3)
obj_sketch011_line_3 = Part.LineSegment(obj_sketch011_vector_3, obj_sketch011_vector_1)
obj_sketch011_all_geoms = [obj_sketch011_line_1, obj_sketch011_line_2, obj_sketch011_line_3]
obj_sketch011.addGeometry(obj_sketch011_all_geoms, False)
obj_sketch011_all_ext_geoms = [[obj_pad004, 'Edge105'], [obj_pad004, 'Edge33']]
for a, b in obj_sketch011_all_ext_geoms:
    obj_sketch011.addExternal(a.Name, b)
obj_sketch011_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 2,
        obj_sketch011_all_geoms.index(obj_sketch011_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_2), 2,
        obj_sketch011_all_geoms.index(obj_sketch011_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_3), 2,
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 1,
        -obj_sketch011_all_ext_geoms.index([obj_pad004, 'Edge105'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_2), 2,
        -obj_sketch011_all_ext_geoms.index([obj_pad004, 'Edge33'])-3, 1,
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch011_all_geoms.index(obj_sketch011_line_2),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1),
    ),
    # 7
]
obj_sketch011.addConstraint(obj_sketch011_constraints)
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_sketch011
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005, obj_sketch010, obj_pad004, obj_sketch011]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-029-Sketch011.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch011')

obj_pocket006 = body_left_y_idler_plate.newObject('PartDesign::Pocket', 'Pocket006')
obj_pocket006.Label = 'Pocket006'
obj_pocket006.Profile = (obj_sketch011, [])
obj_pocket006.Length = '7 mm'
obj_pocket006.Length2 = '100 mm'
obj_pocket006.Type = 'Length'
obj_pocket006.UpToFace = None
obj_pocket006.Reversed = False
obj_pocket006.Midplane = False
obj_pocket006.Offset = '0 mm'
obj_pocket006.BaseFeature = obj_pad004
if body_left_y_idler_plate_debug:
    body_left_y_idler_plate.Tip = obj_pocket006
    body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005, obj_sketch010, obj_pad004, obj_sketch011, obj_pocket006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_idler_plate-030-Pocket006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket006')

body_left_y_idler_plate.Group = [obj_backvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftidler_bind, obj_frameblmotor_bind, obj_framebltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_sketch007, obj_pocket003, obj_sketch008, obj_pocket004, obj_sketch009, obj_pocket005, obj_sketch010, obj_pad004, obj_sketch011, obj_pocket006]
body_left_y_idler_plate.Tip = obj_pocket006
FreeCAD.ActiveDocument.recompute()

App.ActiveDocument.saveAs("plate.FCStd")
