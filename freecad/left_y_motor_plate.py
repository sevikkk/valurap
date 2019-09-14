
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
body_leftymotorplate_debug = False
body_leftymotorplate = App.activeDocument().addObject('PartDesign::Body', 'LeftYMotorPlate')
body_leftymotorplate.Label = 'LeftYMotorPlate'
obj_frontvslot_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'FrontVSlot_bind')
obj_frontvslot_bind_orig = App.getDocument('frame').getObject('FrontVSlot')
obj_frontvslot_bind.TraceSupport = False
obj_frontvslot_bind.Support = [(obj_frontvslot_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_frontvslot_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-001-FrontVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrontVSlot_bind')

obj_leftvslot_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'LeftVSlot_bind')
obj_leftvslot_bind_orig = App.getDocument('frame').getObject('LeftVSlot')
obj_leftvslot_bind.TraceSupport = False
obj_leftvslot_bind.Support = [(obj_leftvslot_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_leftvslot_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-002-LeftVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftVSlot_bind')

obj_leftrail_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'LeftRail_bind')
obj_leftrail_bind_orig = App.getDocument('frame').getObject('LeftRail')
obj_leftrail_bind.TraceSupport = False
obj_leftrail_bind.Support = [(obj_leftrail_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_leftrail_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-003-LeftRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftRail_bind')

obj_leftmotor_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'LeftMotor_bind')
obj_leftmotor_bind_orig = App.getDocument('frame').getObject('LeftMotor')
obj_leftmotor_bind.TraceSupport = False
obj_leftmotor_bind.Support = [(obj_leftmotor_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_leftmotor_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-004-LeftMotor_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftMotor_bind')

obj_frameflmotor_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'FrameFLMotor_bind')
obj_frameflmotor_bind_orig = App.getDocument('frame').getObject('FrameFLMotor')
obj_frameflmotor_bind.TraceSupport = False
obj_frameflmotor_bind.Support = [(obj_frameflmotor_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_frameflmotor_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-005-FrameFLMotor_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLMotor_bind')

obj_framefltopbb_bind = body_leftymotorplate.newObject('PartDesign::ShapeBinder', 'FrameFLTopBB_bind')
obj_framefltopbb_bind_orig = App.getDocument('frame').getObject('FrameFLTopBB')
obj_framefltopbb_bind.TraceSupport = False
obj_framefltopbb_bind.Support = [(obj_framefltopbb_bind_orig, '')]
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_framefltopbb_bind
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-006-FrameFLTopBB_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLTopBB_bind')

obj_sketch = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch')
obj_sketch.Support = (obj_frontvslot_bind, ['Face55'])
obj_sketch.MapMode = 'FlatFace'
obj_sketch_vector_1 = App.Vector(10.000, 96.150, 0.000)
obj_sketch_vector_2 = App.Vector(-56.150, 96.150, 0.000)
obj_sketch_vector_3 = App.Vector(10.000, -20.000, 0.000)
obj_sketch_vector_4 = App.Vector(-51.150, -20.000, 0.000)
obj_sketch_vector_5 = App.Vector(-56.150, -20.000, 0.000)
obj_sketch_vector_6 = App.Vector(-56.150, -13.250, 0.000)
obj_sketch_vector_7 = App.Vector(-56.150, 91.150, 0.000)
obj_sketch_vector_8 = App.Vector(0.000, -10.000, 0.000)
obj_sketch_vector_9 = App.Vector(0.000, 19.925, 0.000)
obj_sketch_vector_10 = App.Vector(0.000, 49.850, 0.000)
obj_sketch_vector_11 = App.Vector(-20.000, 49.850, 0.000)
obj_sketch_vector_12 = App.Vector(0.000, 90.150, 0.000)
obj_sketch_vector_13 = App.Vector(-20.000, 90.150, 0.000)
obj_sketch_vector_14 = App.Vector(-8.850, 91.150, 0.000)
obj_sketch_vector_15 = App.Vector(-8.850, 48.850, 0.000)
obj_sketch_line_1 = Part.LineSegment(obj_sketch_vector_1, obj_sketch_vector_2)
obj_sketch_line_2 = Part.LineSegment(obj_sketch_vector_3, obj_sketch_vector_1)
obj_sketch_line_3 = Part.LineSegment(obj_sketch_vector_3, obj_sketch_vector_4)
obj_sketch_line_4 = Part.LineSegment(obj_sketch_vector_4, obj_sketch_vector_5)
obj_sketch_line_5 = Part.LineSegment(obj_sketch_vector_5, obj_sketch_vector_6)
obj_sketch_line_6 = Part.LineSegment(obj_sketch_vector_6, obj_sketch_vector_7)
obj_sketch_line_7 = Part.LineSegment(obj_sketch_vector_7, obj_sketch_vector_2)
obj_sketch_circle_1 = Part.Circle(obj_sketch_vector_8, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_2 = Part.Circle(obj_sketch_vector_9, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_3 = Part.Circle(obj_sketch_vector_10, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_4 = Part.Circle(obj_sketch_vector_11, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_5 = Part.Circle(obj_sketch_vector_12, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_6 = Part.Circle(obj_sketch_vector_13, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_point_1 = Part.Point(obj_sketch_vector_14)
obj_sketch_point_2 = Part.Point(obj_sketch_vector_15)
obj_sketch_line_8 = Part.LineSegment(obj_sketch_vector_14, obj_sketch_vector_10)
obj_sketch_line_8.Construction = True
obj_sketch_line_9 = Part.LineSegment(obj_sketch_vector_12, obj_sketch_vector_15)
obj_sketch_line_9.Construction = True
obj_sketch_line_10 = Part.LineSegment(obj_sketch_vector_10, obj_sketch_vector_9)
obj_sketch_line_10.Construction = True
obj_sketch_line_11 = Part.LineSegment(obj_sketch_vector_9, obj_sketch_vector_8)
obj_sketch_line_11.Construction = True
obj_sketch_all_geoms = [obj_sketch_line_1, obj_sketch_line_2, obj_sketch_line_3, obj_sketch_line_4, obj_sketch_line_5, obj_sketch_line_6, obj_sketch_line_7, obj_sketch_circle_1, obj_sketch_circle_2, obj_sketch_circle_3, obj_sketch_circle_4, obj_sketch_circle_5, obj_sketch_circle_6, obj_sketch_point_1, obj_sketch_point_2, obj_sketch_line_8, obj_sketch_line_9, obj_sketch_line_10, obj_sketch_line_11]
obj_sketch.addGeometry(obj_sketch_all_geoms, False)
obj_sketch_all_ext_geoms = [[obj_framefltopbb_bind, 'Face8'], [obj_framefltopbb_bind, 'Face1'], [obj_framefltopbb_bind, 'Edge7'], [obj_leftmotor_bind, 'Face4'], [obj_leftrail_bind, 'Face430'], [obj_leftvslot_bind, 'Face25'], [obj_leftrail_bind, 'Face442'], [obj_leftmotor_bind, 'Face12'], [obj_leftmotor_bind, 'Face41'], [obj_frameflmotor_bind, 'Face41'], [obj_frameflmotor_bind, 'Face8'], [obj_frontvslot_bind, 'Face57'], [obj_frameflmotor_bind, 'Face12'], [obj_leftmotor_bind, 'Face8'], [obj_frameflmotor_bind, 'Face47']]
for a, b in obj_sketch_all_ext_geoms:
    obj_sketch.addExternal(a.Name, b)
obj_sketch_constraints = [
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 1
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_2),
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frontvslot_bind, 'Face57'])-3,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_7), 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_7), 1,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 1,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 1,
    ),
    # 9
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 10
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 11
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_7),
    ),
    # 12
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_3),
    ),
    # 13
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 14
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        -obj_sketch_all_ext_geoms.index([obj_leftmotor_bind, 'Face12'])-3,
    ),
    # 15
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        -obj_sketch_all_ext_geoms.index([obj_leftmotor_bind, 'Face8'])-3,
    ),
    # 16
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        5.0,
    ),
    # 17
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflmotor_bind, 'Face47'])-3,
    ),
    # 18
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        5.0,
    ),
    # 19
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
    ),
    # 20
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftvslot_bind, 'Face25'])-3,
    ),
    # 21
    Sketcher.Constraint('Radius',
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 2.6,
    ),
    # 22
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
        obj_sketch_all_geoms.index(obj_sketch_circle_1),
    ),
    # 23
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
        obj_sketch_all_geoms.index(obj_sketch_circle_3),
    ),
    # 24
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
        obj_sketch_all_geoms.index(obj_sketch_circle_4),
    ),
    # 25
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
        obj_sketch_all_geoms.index(obj_sketch_circle_6),
    ),
    # 26
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
        obj_sketch_all_geoms.index(obj_sketch_circle_5),
    ),
    # 27
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
    ),
    # 28
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
    ),
    # 29
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 3,
    ),
    # 30
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_circle_4), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_6), 3,
    ),
    # 31
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_4), 3,
    ),
    # 32
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_6), 3,
    ),
    # 33
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 3,
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        6.0,
    ),
    # 34
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
        10.0,
    ),
    # 35
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
        10.0,
    ),
    # 36
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_circle_4), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
        20.0,
    ),
    # 37
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmotor_bind, 'Face47'])-3,
    ),
    # 38
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmotor_bind, 'Face4'])-3,
    ),
    # 39
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmotor_bind, 'Face4'])-3,
    ),
    # 40
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmotor_bind, 'Face8'])-3,
    ),
    # 41
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_8), 1,
    ),
    # 42
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_9), 2,
    ),
    # 43
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_9), 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 3,
    ),
    # 44
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_8), 2,
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
    ),
    # 45
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_line_8),
        obj_sketch_all_geoms.index(obj_sketch_line_9),
    ),
    # 46
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_10), 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
    ),
    # 47
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_10), 2,
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
    ),
    # 48
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_11), 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
    ),
    # 49
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_11), 2,
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
    ),
    # 50
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_line_10),
        obj_sketch_all_geoms.index(obj_sketch_line_11),
    ),
    # 51
]
obj_sketch.addConstraint(obj_sketch_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-007-Sketch.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch')

obj_pad = body_leftymotorplate.newObject('PartDesign::Pad', 'Pad')
obj_pad.Label = 'Pad'
obj_pad.Profile = (obj_sketch, [])
obj_pad.Length = '5 mm'
obj_pad.Length2 = '100 mm'
obj_pad.Type = 'Length'
obj_pad.Reversed = False
obj_pad.Midplane = False
obj_pad.Offset = '0 mm'
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pad
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-008-Pad.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad')

obj_sketch001 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch001')
obj_sketch001.Support = (obj_pad, ['Face15'])
obj_sketch001.MapMode = 'FlatFace'
obj_sketch001_vector_1 = App.Vector(-56.150, 11.750, 0.000)
obj_sketch001_vector_2 = App.Vector(-56.150, -13.250, 0.000)
obj_sketch001_vector_3 = App.Vector(-56.150, -18.250, 0.000)
obj_sketch001_vector_4 = App.Vector(-51.150, -18.250, 0.000)
obj_sketch001_vector_5 = App.Vector(-8.850, -18.250, 0.000)
obj_sketch001_vector_6 = App.Vector(-3.850, -18.250, 0.000)
obj_sketch001_vector_7 = App.Vector(-3.850, 11.750, 0.000)
obj_sketch001_vector_8 = App.Vector(-8.850, 11.750, 0.000)
obj_sketch001_vector_9 = App.Vector(-8.850, -13.250, 0.000)
obj_sketch001_vector_10 = App.Vector(-51.150, -13.250, 0.000)
obj_sketch001_vector_11 = App.Vector(-51.150, 11.750, 0.000)
obj_sketch001_line_1 = Part.LineSegment(obj_sketch001_vector_1, obj_sketch001_vector_2)
obj_sketch001_line_2 = Part.LineSegment(obj_sketch001_vector_2, obj_sketch001_vector_3)
obj_sketch001_line_3 = Part.LineSegment(obj_sketch001_vector_3, obj_sketch001_vector_4)
obj_sketch001_line_4 = Part.LineSegment(obj_sketch001_vector_4, obj_sketch001_vector_5)
obj_sketch001_line_5 = Part.LineSegment(obj_sketch001_vector_5, obj_sketch001_vector_6)
obj_sketch001_line_6 = Part.LineSegment(obj_sketch001_vector_6, obj_sketch001_vector_7)
obj_sketch001_line_7 = Part.LineSegment(obj_sketch001_vector_7, obj_sketch001_vector_8)
obj_sketch001_line_8 = Part.LineSegment(obj_sketch001_vector_8, obj_sketch001_vector_9)
obj_sketch001_line_9 = Part.LineSegment(obj_sketch001_vector_9, obj_sketch001_vector_10)
obj_sketch001_line_10 = Part.LineSegment(obj_sketch001_vector_10, obj_sketch001_vector_11)
obj_sketch001_line_11 = Part.LineSegment(obj_sketch001_vector_11, obj_sketch001_vector_1)
obj_sketch001_all_geoms = [obj_sketch001_line_1, obj_sketch001_line_2, obj_sketch001_line_3, obj_sketch001_line_4, obj_sketch001_line_5, obj_sketch001_line_6, obj_sketch001_line_7, obj_sketch001_line_8, obj_sketch001_line_9, obj_sketch001_line_10, obj_sketch001_line_11]
obj_sketch001.addGeometry(obj_sketch001_all_geoms, False)
obj_sketch001_all_ext_geoms = [[obj_pad, 'Edge10'], [obj_pad, 'Edge4'], [obj_frameflmotor_bind, 'Face4'], [obj_frameflmotor_bind, 'Face12'], [obj_frameflmotor_bind, 'Face8'], [obj_leftmotor_bind, 'Face8'], [obj_leftmotor_bind, 'Face12'], [obj_leftmotor_bind, 'Face4'], [obj_pad, 'Edge19']]
for a, b in obj_sketch001_all_ext_geoms:
    obj_sketch001.addExternal(a.Name, b)
obj_sketch001_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 2,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_11), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_11), 2,
    ),
    # 11
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 12
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1),
    ),
    # 13
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10),
    ),
    # 14
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6),
    ),
    # 15
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8),
    ),
    # 16
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_11),
    ),
    # 17
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3),
    ),
    # 18
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4),
    ),
    # 19
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5),
    ),
    # 20
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7),
    ),
    # 21
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9),
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmotor_bind, 'Face12'])-3,
    ),
    # 23
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmotor_bind, 'Face8'])-3,
    ),
    # 24
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge10'])-3,
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmotor_bind, 'Face4'])-3,
    ),
    # 26
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmotor_bind, 'Face12'])-3,
    ),
    # 27
    Sketcher.Constraint('Equal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5),
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 28
    Sketcher.Constraint('Equal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3),
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 29
    Sketcher.Constraint('Equal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7),
        obj_sketch001_all_geoms.index(obj_sketch001_line_5),
    ),
    # 30
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
    ),
    # 31
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        30.0,
    ),
    # 32
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmotor_bind, 'Face8'])-3,
    ),
    # 33
]
obj_sketch001.addConstraint(obj_sketch001_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch001
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-009-Sketch001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch001')

obj_pad001 = body_leftymotorplate.newObject('PartDesign::Pad', 'Pad001')
obj_pad001.Label = 'Pad001'
obj_pad001.Profile = (obj_sketch001, [])
obj_pad001.Length = '42 mm'
obj_pad001.Length2 = '100 mm'
obj_pad001.Type = 'Length'
obj_pad001.Reversed = False
obj_pad001.Midplane = False
obj_pad001.Offset = '0 mm'
obj_pad001.BaseFeature = obj_pad
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pad001
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-010-Pad001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad001')

obj_sketch002 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch002')
obj_sketch002.Support = (obj_pad001, ['Face17'])
obj_sketch002.MapMode = 'FlatFace'
obj_sketch002_vector_1 = App.Vector(-30.150, 36.000, 0.000)
obj_sketch002_vector_2 = App.Vector(-45.650, 51.500, 0.000)
obj_sketch002_vector_3 = App.Vector(-14.650, 51.500, 0.000)
obj_sketch002_vector_4 = App.Vector(-45.650, 20.500, 0.000)
obj_sketch002_vector_5 = App.Vector(-14.650, 20.500, 0.000)
obj_sketch002_circle_1 = Part.Circle(obj_sketch002_vector_1, App.Vector (0.0, 0.0, 1.0), 15.0)
obj_sketch002_circle_2 = Part.Circle(obj_sketch002_vector_2, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch002_circle_3 = Part.Circle(obj_sketch002_vector_3, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch002_circle_4 = Part.Circle(obj_sketch002_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch002_circle_5 = Part.Circle(obj_sketch002_vector_5, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch002_all_geoms = [obj_sketch002_circle_1, obj_sketch002_circle_2, obj_sketch002_circle_3, obj_sketch002_circle_4, obj_sketch002_circle_5]
obj_sketch002.addGeometry(obj_sketch002_all_geoms, False)
obj_sketch002_all_ext_geoms = [[obj_pad001, 'Edge52'], [obj_pad001, 'Edge54'], [obj_pad001, 'Edge55'], [obj_pad001, 'Edge21']]
for a, b in obj_sketch002_all_ext_geoms:
    obj_sketch002.addExternal(a.Name, b)
obj_sketch002_constraints = [
    Sketcher.Constraint('Radius',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 15.0,
    ),
    # 1
    Sketcher.Constraint('DistanceY',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge55'])-3, 1,
        21.0,
    ),
    # 2
    Sketcher.Constraint('DistanceX',
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge55'])-3, 1,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
        21.0,
    ),
    # 3
    Sketcher.Constraint('Radius',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4), 1.6,
    ),
    # 4
    Sketcher.Constraint('Equal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4),
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2),
    ),
    # 5
    Sketcher.Constraint('Equal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4),
        obj_sketch002_all_geoms.index(obj_sketch002_circle_3),
    ),
    # 6
    Sketcher.Constraint('Equal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4),
        obj_sketch002_all_geoms.index(obj_sketch002_circle_5),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4), 3,
    ),
    # 8
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_3), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_5), 3,
    ),
    # 9
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_3), 3,
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_4), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_5), 3,
    ),
    # 11
    Sketcher.Constraint('DistanceX',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
        15.5,
    ),
    # 12
    Sketcher.Constraint('DistanceY',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        15.5,
    ),
    # 13
    Sketcher.Constraint('Symmetric',
        obj_sketch002_all_geoms.index(obj_sketch002_circle_2), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_5), 3,
        obj_sketch002_all_geoms.index(obj_sketch002_circle_1), 3,
    ),
    # 14
]
obj_sketch002.addConstraint(obj_sketch002_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch002
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-011-Sketch002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch002')

obj_pocket = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket')
obj_pocket.Label = 'Pocket'
obj_pocket.Profile = (obj_sketch002, [])
obj_pocket.Length = '5 mm'
obj_pocket.Length2 = '100 mm'
obj_pocket.Type = 'ThroughAll'
obj_pocket.Reversed = False
obj_pocket.Midplane = False
obj_pocket.Offset = '0 mm'
obj_pocket.BaseFeature = obj_pad001
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-012-Pocket.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket')

obj_sketch003 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch003')
obj_sketch003.Support = (obj_pocket, ['Face19'])
obj_sketch003.MapMode = 'FlatFace'
obj_sketch003_vector_1 = App.Vector(-57.000, -13.250, 0.000)
obj_sketch003_vector_2 = App.Vector(-57.000, 11.750, 0.000)
obj_sketch003_vector_3 = App.Vector(-20.000, 11.750, 0.000)
obj_sketch003_line_1 = Part.LineSegment(obj_sketch003_vector_1, obj_sketch003_vector_2)
obj_sketch003_line_2 = Part.LineSegment(obj_sketch003_vector_2, obj_sketch003_vector_3)
obj_sketch003_line_3 = Part.LineSegment(obj_sketch003_vector_3, obj_sketch003_vector_1)
obj_sketch003_all_geoms = [obj_sketch003_line_1, obj_sketch003_line_2, obj_sketch003_line_3]
obj_sketch003.addGeometry(obj_sketch003_all_geoms, False)
obj_sketch003_all_ext_geoms = [[obj_pocket, 'Edge64'], [obj_pocket, 'Edge63']]
for a, b in obj_sketch003_all_ext_geoms:
    obj_sketch003.addExternal(a.Name, b)
obj_sketch003_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 1,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge63'])-3,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge64'])-3,
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 7
    Sketcher.Constraint('DistanceY',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge64'])-3, 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
        5.0,
    ),
    # 8
    Sketcher.Constraint('DistanceX',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge63'])-3, 1,
        5.0,
    ),
    # 9
]
obj_sketch003.addConstraint(obj_sketch003_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch003
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-013-Sketch003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch003')

obj_pocket001 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket001')
obj_pocket001.Label = 'Pocket001'
obj_pocket001.Profile = (obj_sketch003, [])
obj_pocket001.Length = '70 mm'
obj_pocket001.Length2 = '100 mm'
obj_pocket001.Type = 'Length'
obj_pocket001.Reversed = False
obj_pocket001.Midplane = False
obj_pocket001.Offset = '0 mm'
obj_pocket001.BaseFeature = obj_pocket
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket001
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-014-Pocket001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket001')

obj_sketch004 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch004')
obj_sketch004.Support = (obj_pocket001, ['Face5'])
obj_sketch004.MapMode = 'FlatFace'
obj_sketch004_vector_1 = App.Vector(-56.150, 43.850, 0.000)
obj_sketch004_vector_2 = App.Vector(-30.000, 43.850, 0.000)
obj_sketch004_vector_3 = App.Vector(-30.000, 96.150, 0.000)
obj_sketch004_vector_4 = App.Vector(-56.150, 96.150, 0.000)
obj_sketch004_vector_5 = App.Vector(-56.150, 91.150, 0.000)
obj_sketch004_vector_6 = App.Vector(-35.000, 91.150, 0.000)
obj_sketch004_vector_7 = App.Vector(-35.000, 48.850, 0.000)
obj_sketch004_vector_8 = App.Vector(-56.150, 48.850, 0.000)
obj_sketch004_vector_9 = App.Vector(-30.000, 91.150, 0.000)
obj_sketch004_vector_10 = App.Vector(-30.000, 70.000, 0.000)
obj_sketch004_vector_11 = App.Vector(-30.000, 48.850, 0.000)
obj_sketch004_line_1 = Part.LineSegment(obj_sketch004_vector_1, obj_sketch004_vector_2)
obj_sketch004_line_2 = Part.LineSegment(obj_sketch004_vector_3, obj_sketch004_vector_4)
obj_sketch004_line_3 = Part.LineSegment(obj_sketch004_vector_4, obj_sketch004_vector_5)
obj_sketch004_line_4 = Part.LineSegment(obj_sketch004_vector_5, obj_sketch004_vector_6)
obj_sketch004_line_5 = Part.LineSegment(obj_sketch004_vector_6, obj_sketch004_vector_7)
obj_sketch004_line_6 = Part.LineSegment(obj_sketch004_vector_7, obj_sketch004_vector_8)
obj_sketch004_line_7 = Part.LineSegment(obj_sketch004_vector_8, obj_sketch004_vector_1)
obj_sketch004_line_8 = Part.LineSegment(obj_sketch004_vector_3, obj_sketch004_vector_9)
obj_sketch004_line_9 = Part.LineSegment(obj_sketch004_vector_9, obj_sketch004_vector_10)
obj_sketch004_line_10 = Part.LineSegment(obj_sketch004_vector_10, obj_sketch004_vector_11)
obj_sketch004_line_11 = Part.LineSegment(obj_sketch004_vector_11, obj_sketch004_vector_2)
obj_sketch004_all_geoms = [obj_sketch004_line_1, obj_sketch004_line_2, obj_sketch004_line_3, obj_sketch004_line_4, obj_sketch004_line_5, obj_sketch004_line_6, obj_sketch004_line_7, obj_sketch004_line_8, obj_sketch004_line_9, obj_sketch004_line_10, obj_sketch004_line_11]
obj_sketch004.addGeometry(obj_sketch004_all_geoms, False)
obj_sketch004_all_ext_geoms = [[obj_frameflmotor_bind, 'Face8'], [obj_frameflmotor_bind, 'Face12'], [obj_pocket001, 'Edge33'], [obj_frameflmotor_bind, 'Face4'], [obj_pocket001, 'Edge4'], [obj_pocket001, 'Edge10'], [obj_framefltopbb_bind, 'Face1'], [obj_framefltopbb_bind, 'Face8'], [obj_pocket001, 'Edge7']]
for a, b in obj_sketch004_all_ext_geoms:
    obj_sketch004.addExternal(a.Name, b)
obj_sketch004_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_7), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 2,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_7), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_7),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5),
    ),
    # 8
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3),
    ),
    # 9
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1),
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_6),
    ),
    # 11
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4),
    ),
    # 12
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2),
    ),
    # 13
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
        -obj_sketch004_all_ext_geoms.index([obj_frameflmotor_bind, 'Face4'])-3,
    ),
    # 14
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge10'])-3,
    ),
    # 15
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
    ),
    # 16
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_6), 2,
        -obj_sketch004_all_ext_geoms.index([obj_frameflmotor_bind, 'Face8'])-3,
    ),
    # 17
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_5), 2,
        -obj_sketch004_all_ext_geoms.index([obj_frameflmotor_bind, 'Face12'])-3,
    ),
    # 18
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge4'])-3,
    ),
    # 19
    Sketcher.Constraint('Equal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3),
        obj_sketch004_all_geoms.index(obj_sketch004_line_7),
    ),
    # 20
    Sketcher.Constraint('DistanceX',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 1,
        5.0,
    ),
    # 21
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_8), 1,
    ),
    # 22
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_9), 1,
        obj_sketch004_all_geoms.index(obj_sketch004_line_8), 2,
    ),
    # 23
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_9), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_10), 1,
    ),
    # 24
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_10), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_11), 1,
    ),
    # 25
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_11), 2,
    ),
    # 26
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_8),
    ),
    # 27
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_9),
    ),
    # 28
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_10),
    ),
    # 29
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_11),
    ),
    # 30
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_8), 2,
        -obj_sketch004_all_ext_geoms.index([obj_frameflmotor_bind, 'Face4'])-3,
    ),
    # 31
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_10), 2,
        -obj_sketch004_all_ext_geoms.index([obj_frameflmotor_bind, 'Face8'])-3,
    ),
    # 32
    Sketcher.Constraint('Equal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_9),
        obj_sketch004_all_geoms.index(obj_sketch004_line_10),
    ),
    # 33
]
obj_sketch004.addConstraint(obj_sketch004_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch004
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-015-Sketch004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch004')

obj_pad002 = body_leftymotorplate.newObject('PartDesign::Pad', 'Pad002')
obj_pad002.Label = 'Pad002'
obj_pad002.Profile = (obj_sketch004, [])
obj_pad002.Length = '42 mm'
obj_pad002.Length2 = '100 mm'
obj_pad002.Type = 'Length'
obj_pad002.Reversed = False
obj_pad002.Midplane = False
obj_pad002.Offset = '0 mm'
obj_pad002.BaseFeature = obj_pocket001
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pad002
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-016-Pad002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad002')

obj_sketch005 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch005')
obj_sketch005.Support = (obj_pad002, ['Face28'])
obj_sketch005.MapMode = 'FlatFace'
obj_sketch005_vector_1 = App.Vector(-36.000, 70.000, 0.000)
obj_sketch005_vector_2 = App.Vector(-51.500, 54.500, 0.000)
obj_sketch005_vector_3 = App.Vector(-51.500, 85.500, 0.000)
obj_sketch005_vector_4 = App.Vector(-20.500, 54.500, 0.000)
obj_sketch005_vector_5 = App.Vector(-20.500, 85.500, 0.000)
obj_sketch005_circle_1 = Part.Circle(obj_sketch005_vector_1, App.Vector (0.0, 0.0, 1.0), 15.0)
obj_sketch005_circle_2 = Part.Circle(obj_sketch005_vector_2, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_3 = Part.Circle(obj_sketch005_vector_3, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_4 = Part.Circle(obj_sketch005_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_5 = Part.Circle(obj_sketch005_vector_5, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_all_geoms = [obj_sketch005_circle_1, obj_sketch005_circle_2, obj_sketch005_circle_3, obj_sketch005_circle_4, obj_sketch005_circle_5]
obj_sketch005.addGeometry(obj_sketch005_all_geoms, False)
obj_sketch005_all_ext_geoms = [[obj_pad002, 'Vertex66'], [obj_pad002, 'Vertex2'], [obj_pad002, 'Vertex39'], [obj_pad002, 'Edge8'], [obj_pad002, 'Edge99']]
for a, b in obj_sketch005_all_ext_geoms:
    obj_sketch005.addExternal(a.Name, b)
obj_sketch005_constraints = [
    Sketcher.Constraint('Radius',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 15.0,
    ),
    # 1
    Sketcher.Constraint('Radius',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 1.6,
    ),
    # 2
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3),
    ),
    # 3
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5),
    ),
    # 4
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4),
    ),
    # 5
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5), 3,
    ),
    # 7
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4), 3,
    ),
    # 8
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5), 3,
    ),
    # 9
    Sketcher.Constraint('Symmetric',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_5), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
    ),
    # 10
    Sketcher.Constraint('DistanceX',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
        15.5,
    ),
    # 11
    Sketcher.Constraint('DistanceY',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
        15.5,
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge99'])-3,
    ),
    # 13
    Sketcher.Constraint('DistanceX',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge99'])-3, 1,
        21.0,
    ),
    # 14
]
obj_sketch005.addConstraint(obj_sketch005_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch005
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-017-Sketch005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch005')

obj_pocket002 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket002')
obj_pocket002.Label = 'Pocket002'
obj_pocket002.Profile = (obj_sketch005, [])
obj_pocket002.Length = '5 mm'
obj_pocket002.Length2 = '100 mm'
obj_pocket002.Type = 'Length'
obj_pocket002.Reversed = False
obj_pocket002.Midplane = False
obj_pocket002.Offset = '0 mm'
obj_pocket002.BaseFeature = obj_pad002
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket002
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-018-Pocket002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket002')

obj_sketch006 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch006')
obj_sketch006.Support = (obj_pocket002, ['Face5'])
obj_sketch006.MapMode = 'FlatFace'
obj_sketch006_vector_1 = App.Vector(-1.000, 83.000, 0.000)
obj_sketch006_vector_2 = App.Vector(10.000, 83.000, 0.000)
obj_sketch006_vector_3 = App.Vector(10.000, 57.000, 0.000)
obj_sketch006_vector_4 = App.Vector(-1.000, 57.000, 0.000)
obj_sketch006_vector_5 = App.Vector(-30.000, 70.000, 0.000)
obj_sketch006_line_1 = Part.LineSegment(obj_sketch006_vector_1, obj_sketch006_vector_2)
obj_sketch006_line_2 = Part.LineSegment(obj_sketch006_vector_2, obj_sketch006_vector_3)
obj_sketch006_line_3 = Part.LineSegment(obj_sketch006_vector_3, obj_sketch006_vector_4)
obj_sketch006_line_4 = Part.LineSegment(obj_sketch006_vector_4, obj_sketch006_vector_1)
obj_sketch006_point_1 = Part.Point(obj_sketch006_vector_5)
obj_sketch006_all_geoms = [obj_sketch006_line_1, obj_sketch006_line_2, obj_sketch006_line_3, obj_sketch006_line_4, obj_sketch006_point_1]
obj_sketch006.addGeometry(obj_sketch006_all_geoms, False)
obj_sketch006_all_ext_geoms = [[obj_pocket002, 'Edge4'], [obj_frontvslot_bind, 'Edge211'], [obj_pocket002, 'Vertex69'], [obj_pocket002, 'Edge110'], [obj_pocket002, 'Vertex42']]
for a, b in obj_sketch006_all_ext_geoms:
    obj_sketch006.addExternal(a.Name, b)
obj_sketch006_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4),
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
        -obj_sketch006_all_ext_geoms.index([obj_frontvslot_bind, 'Edge211'])-3,
    ),
    # 9
    Sketcher.Constraint('DistanceX',
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
        11.0,
    ),
    # 10
    Sketcher.Constraint('Symmetric',
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Vertex42'])-3, 1,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Vertex69'])-3, 1,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
    ),
    # 11
    Sketcher.Constraint('DistanceY',
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
        13.0,
    ),
    # 12
    Sketcher.Constraint('DistanceY',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
        13.0,
    ),
    # 13
]
obj_sketch006.addConstraint(obj_sketch006_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch006
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-019-Sketch006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch006')

obj_pad003 = body_leftymotorplate.newObject('PartDesign::Pad', 'Pad003')
obj_pad003.Label = 'Pad003'
obj_pad003.Profile = (obj_sketch006, [])
obj_pad003.Length = '40 mm'
obj_pad003.Length2 = '100 mm'
obj_pad003.Type = 'Length'
obj_pad003.Reversed = False
obj_pad003.Midplane = False
obj_pad003.Offset = '0 mm'
obj_pad003.BaseFeature = obj_pocket002
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pad003
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-020-Pad003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad003')

obj_fillet = body_leftymotorplate.newObject('PartDesign::Fillet', 'Fillet')
obj_fillet.Label = 'Fillet'
obj_fillet.BaseFeature = obj_pad003
obj_fillet.Radius = '10 mm'
obj_fillet.Base = (obj_pad003, ['Edge123', 'Edge120'])
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_fillet
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-021-Fillet.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Fillet')

obj_sketch008 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch008')
obj_sketch008.Support = (obj_fillet, ['Face8'])
obj_sketch008.MapMode = 'FlatFace'
obj_sketch008_vector_1 = App.Vector(36.000, 70.000, 0.000)
obj_sketch008_vector_2 = App.Vector(15.000, 83.000, 0.000)
obj_sketch008_vector_3 = App.Vector(15.000, 57.000, 0.000)
obj_sketch008_circle_1 = Part.Circle(obj_sketch008_vector_1, App.Vector (0.0, 0.0, 1.0), 11.0)
obj_sketch008_line_1 = Part.LineSegment(obj_sketch008_vector_2, obj_sketch008_vector_1)
obj_sketch008_line_1.Construction = True
obj_sketch008_line_2 = Part.LineSegment(obj_sketch008_vector_1, obj_sketch008_vector_3)
obj_sketch008_line_2.Construction = True
obj_sketch008_all_geoms = [obj_sketch008_circle_1, obj_sketch008_line_1, obj_sketch008_line_2]
obj_sketch008.addGeometry(obj_sketch008_all_geoms, False)
obj_sketch008_all_ext_geoms = [[obj_fillet, 'Edge23']]
for a, b in obj_sketch008_all_ext_geoms:
    obj_sketch008.addExternal(a.Name, b)
obj_sketch008_constraints = [
    Sketcher.Constraint('Radius',
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 11.0,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        -obj_sketch008_all_ext_geoms.index([obj_fillet, 'Edge23'])-3, 1,
        obj_sketch008_all_geoms.index(obj_sketch008_line_2), 2,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 3,
        obj_sketch008_all_geoms.index(obj_sketch008_line_2), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 2,
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 3,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        -obj_sketch008_all_ext_geoms.index([obj_fillet, 'Edge23'])-3, 2,
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 1,
    ),
    # 5
    Sketcher.Constraint('Equal',
        obj_sketch008_all_geoms.index(obj_sketch008_line_1),
        obj_sketch008_all_geoms.index(obj_sketch008_line_2),
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        obj_sketch008_all_geoms.index(obj_sketch008_line_1), 1,
        obj_sketch008_all_geoms.index(obj_sketch008_circle_1), 3,
        21.0,
    ),
    # 7
]
obj_sketch008.addConstraint(obj_sketch008_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch008
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-022-Sketch008.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch008')

obj_pocket003 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket003')
obj_pocket003.Label = 'Pocket003'
obj_pocket003.Profile = (obj_sketch008, [])
obj_pocket003.Length = '8 mm'
obj_pocket003.Length2 = '100 mm'
obj_pocket003.Type = 'Length'
obj_pocket003.Reversed = False
obj_pocket003.Midplane = False
obj_pocket003.Offset = '0 mm'
obj_pocket003.BaseFeature = obj_fillet
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket003
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-023-Pocket003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket003')

obj_sketch009 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch009')
obj_sketch009.Support = (obj_pocket003, ['Face1'])
obj_sketch009.MapMode = 'FlatFace'
obj_sketch009_vector_1 = App.Vector(-36.000, 70.000, 0.000)
obj_sketch009_vector_2 = App.Vector(-15.000, 83.000, 0.000)
obj_sketch009_vector_3 = App.Vector(-15.000, 57.000, 0.000)
obj_sketch009_circle_1 = Part.Circle(obj_sketch009_vector_1, App.Vector (0.0, 0.0, 1.0), 8.0)
obj_sketch009_line_1 = Part.LineSegment(obj_sketch009_vector_1, obj_sketch009_vector_2)
obj_sketch009_line_1.Construction = True
obj_sketch009_line_2 = Part.LineSegment(obj_sketch009_vector_1, obj_sketch009_vector_3)
obj_sketch009_line_2.Construction = True
obj_sketch009_all_geoms = [obj_sketch009_circle_1, obj_sketch009_line_1, obj_sketch009_line_2]
obj_sketch009.addGeometry(obj_sketch009_all_geoms, False)
obj_sketch009_all_ext_geoms = [[obj_pocket003, 'Edge23']]
for a, b in obj_sketch009_all_ext_geoms:
    obj_sketch009.addExternal(a.Name, b)
obj_sketch009_constraints = [
    Sketcher.Constraint('Radius',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 8.0,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 1,
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 2,
        -obj_sketch009_all_ext_geoms.index([obj_pocket003, 'Edge23'])-3, 1,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch009_all_geoms.index(obj_sketch009_line_1), 2,
        -obj_sketch009_all_ext_geoms.index([obj_pocket003, 'Edge23'])-3, 2,
    ),
    # 5
    Sketcher.Constraint('Equal',
        obj_sketch009_all_geoms.index(obj_sketch009_line_2),
        obj_sketch009_all_geoms.index(obj_sketch009_line_1),
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        obj_sketch009_all_geoms.index(obj_sketch009_circle_1), 3,
        obj_sketch009_all_geoms.index(obj_sketch009_line_2), 2,
        21.0,
    ),
    # 7
]
obj_sketch009.addConstraint(obj_sketch009_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch009
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-024-Sketch009.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch009')

obj_pocket004 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket004')
obj_pocket004.Label = 'Pocket004'
obj_pocket004.Profile = (obj_sketch009, [])
obj_pocket004.Length = '5 mm'
obj_pocket004.Length2 = '100 mm'
obj_pocket004.Type = 'Length'
obj_pocket004.Reversed = False
obj_pocket004.Midplane = False
obj_pocket004.Offset = '0 mm'
obj_pocket004.BaseFeature = obj_pocket003
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket004
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-025-Pocket004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket004')

obj_sketch010 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch010')
obj_sketch010.Support = (obj_pocket004, ['Face53'])
obj_sketch010.MapMode = 'FlatFace'
obj_sketch010_vector_1 = App.Vector(-56.150, 91.650, 0.000)
obj_sketch010_vector_2 = App.Vector(-35.000, 91.650, 0.000)
obj_sketch010_vector_3 = App.Vector(-35.000, 48.350, 0.000)
obj_sketch010_vector_4 = App.Vector(-56.150, 48.350, 0.000)
obj_sketch010_vector_5 = App.Vector(-51.850, 11.750, 0.000)
obj_sketch010_vector_6 = App.Vector(-8.150, 11.750, 0.000)
obj_sketch010_vector_7 = App.Vector(-8.150, -13.250, 0.000)
obj_sketch010_vector_8 = App.Vector(-51.850, -13.250, 0.000)
obj_sketch010_line_1 = Part.LineSegment(obj_sketch010_vector_1, obj_sketch010_vector_2)
obj_sketch010_line_2 = Part.LineSegment(obj_sketch010_vector_2, obj_sketch010_vector_3)
obj_sketch010_line_3 = Part.LineSegment(obj_sketch010_vector_3, obj_sketch010_vector_4)
obj_sketch010_line_4 = Part.LineSegment(obj_sketch010_vector_4, obj_sketch010_vector_1)
obj_sketch010_line_5 = Part.LineSegment(obj_sketch010_vector_5, obj_sketch010_vector_6)
obj_sketch010_line_6 = Part.LineSegment(obj_sketch010_vector_6, obj_sketch010_vector_7)
obj_sketch010_line_7 = Part.LineSegment(obj_sketch010_vector_7, obj_sketch010_vector_8)
obj_sketch010_line_8 = Part.LineSegment(obj_sketch010_vector_8, obj_sketch010_vector_5)
obj_sketch010_all_geoms = [obj_sketch010_line_1, obj_sketch010_line_2, obj_sketch010_line_3, obj_sketch010_line_4, obj_sketch010_line_5, obj_sketch010_line_6, obj_sketch010_line_7, obj_sketch010_line_8]
obj_sketch010.addGeometry(obj_sketch010_all_geoms, False)
obj_sketch010_all_ext_geoms = [[obj_pocket004, 'Edge150'], [obj_pocket004, 'Edge152'], [obj_pocket004, 'Edge100'], [obj_pocket004, 'Edge91']]
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
    Sketcher.Constraint('PointOnObject',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge150'])-3, 1,
        obj_sketch010_all_geoms.index(obj_sketch010_line_4),
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge150'])-3, 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_2),
    ),
    # 10
    Sketcher.Constraint('DistanceY',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge150'])-3, 1,
        obj_sketch010_all_geoms.index(obj_sketch010_line_1), 1,
        0.5,
    ),
    # 11
    Sketcher.Constraint('DistanceY',
        obj_sketch010_all_geoms.index(obj_sketch010_line_3), 2,
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge152'])-3, 2,
        0.5,
    ),
    # 12
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_5), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_6), 1,
    ),
    # 13
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_6), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_7), 1,
    ),
    # 14
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_7), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_8), 1,
    ),
    # 15
    Sketcher.Constraint('Coincident',
        obj_sketch010_all_geoms.index(obj_sketch010_line_8), 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_5), 1,
    ),
    # 16
    Sketcher.Constraint('Horizontal',
        obj_sketch010_all_geoms.index(obj_sketch010_line_5),
    ),
    # 17
    Sketcher.Constraint('Horizontal',
        obj_sketch010_all_geoms.index(obj_sketch010_line_7),
    ),
    # 18
    Sketcher.Constraint('Vertical',
        obj_sketch010_all_geoms.index(obj_sketch010_line_6),
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch010_all_geoms.index(obj_sketch010_line_8),
    ),
    # 20
    Sketcher.Constraint('PointOnObject',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge100'])-3, 1,
        obj_sketch010_all_geoms.index(obj_sketch010_line_7),
    ),
    # 21
    Sketcher.Constraint('PointOnObject',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge100'])-3, 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_5),
    ),
    # 22
    Sketcher.Constraint('DistanceX',
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge91'])-3, 2,
        obj_sketch010_all_geoms.index(obj_sketch010_line_6), 2,
        0.7,
    ),
    # 23
    Sketcher.Constraint('DistanceX',
        obj_sketch010_all_geoms.index(obj_sketch010_line_7), 2,
        -obj_sketch010_all_ext_geoms.index([obj_pocket004, 'Edge100'])-3, 1,
        0.7,
    ),
    # 24
]
obj_sketch010.addConstraint(obj_sketch010_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch010
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004, obj_sketch010]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-026-Sketch010.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch010')

obj_pocket005 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket005')
obj_pocket005.Label = 'Pocket005'
obj_pocket005.Profile = (obj_sketch010, [])
obj_pocket005.Length = '0 mm'
obj_pocket005.Length2 = '100 mm'
obj_pocket005.Type = 'UpToFace'
obj_pocket005.Reversed = False
obj_pocket005.Midplane = False
obj_pocket005.Offset = '0 mm'
obj_pocket005.BaseFeature = obj_pocket004
obj_pocket005.UpToFace = (obj_pocket004, ['Face10'])
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket005
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004, obj_sketch010, obj_pocket005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-027-Pocket005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket005')

obj_sketch011 = body_leftymotorplate.newObject('Sketcher::SketchObject', 'Sketch011')
obj_sketch011.Support = (obj_pocket005, ['Face40'])
obj_sketch011.MapMode = 'FlatFace'
obj_sketch011_vector_1 = App.Vector(-35.000, -57.000, 0.000)
obj_sketch011_vector_2 = App.Vector(-56.150, -57.000, 0.000)
obj_sketch011_vector_3 = App.Vector(-56.150, -15.000, 0.000)
obj_sketch011_line_1 = Part.LineSegment(obj_sketch011_vector_1, obj_sketch011_vector_2)
obj_sketch011_line_2 = Part.LineSegment(obj_sketch011_vector_2, obj_sketch011_vector_3)
obj_sketch011_line_3 = Part.LineSegment(obj_sketch011_vector_3, obj_sketch011_vector_1)
obj_sketch011_all_geoms = [obj_sketch011_line_1, obj_sketch011_line_2, obj_sketch011_line_3]
obj_sketch011.addGeometry(obj_sketch011_all_geoms, False)
obj_sketch011_all_ext_geoms = [[obj_pocket005, 'Edge129'], [obj_pocket005, 'Edge130']]
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
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 1,
        obj_sketch011_all_geoms.index(obj_sketch011_line_3), 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 2,
        -obj_sketch011_all_ext_geoms.index([obj_pocket005, 'Edge130'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch011_all_geoms.index(obj_sketch011_line_2), 2,
        -obj_sketch011_all_ext_geoms.index([obj_pocket005, 'Edge129'])-3, 1,
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 1,
        -obj_sketch011_all_ext_geoms.index([obj_pocket005, 'Edge130'])-3,
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        obj_sketch011_all_geoms.index(obj_sketch011_line_1), 1,
        -obj_sketch011_all_ext_geoms.index([obj_pocket005, 'Edge130'])-3, 1,
        5.0,
    ),
    # 7
]
obj_sketch011.addConstraint(obj_sketch011_constraints)
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_sketch011
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004, obj_sketch010, obj_pocket005, obj_sketch011]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-028-Sketch011.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch011')

obj_pocket006 = body_leftymotorplate.newObject('PartDesign::Pocket', 'Pocket006')
obj_pocket006.Label = 'Pocket006'
obj_pocket006.Profile = (obj_sketch011, [])
obj_pocket006.Length = '0 mm'
obj_pocket006.Length2 = '100 mm'
obj_pocket006.Type = 'UpToFace'
obj_pocket006.Reversed = False
obj_pocket006.Midplane = False
obj_pocket006.Offset = '0 mm'
obj_pocket006.BaseFeature = obj_pocket005
obj_pocket006.UpToFace = (obj_pocket005, ['Face28'])
if body_leftymotorplate_debug:
    body_leftymotorplate.Tip = obj_pocket006
    body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004, obj_sketch010, obj_pocket005, obj_sketch011, obj_pocket006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-LeftYMotorPlate-029-Pocket006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket006')

body_leftymotorplate.Group = [obj_frontvslot_bind, obj_leftvslot_bind, obj_leftrail_bind, obj_leftmotor_bind, obj_frameflmotor_bind, obj_framefltopbb_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pad003, obj_fillet, obj_sketch008, obj_pocket003, obj_sketch009, obj_pocket004, obj_sketch010, obj_pocket005, obj_sketch011, obj_pocket006]
body_leftymotorplate.Tip = obj_pocket006
FreeCAD.ActiveDocument.recompute()
Part.export([body_leftymotorplate], 'LeftYMotorPlate.brep')

App.ActiveDocument.saveAs("plate.FCStd")
