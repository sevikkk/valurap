
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
body_left_y_carriage_plate_debug = False
body_left_y_carriage_plate = App.activeDocument().addObject('PartDesign::Body', 'left_y_carriage_plate')
body_left_y_carriage_plate.Label = 'left_y_carriage_plate'
obj_leftvslot_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'LeftVSlot_bind')
obj_leftvslot_bind_orig = App.getDocument('frame').getObject('LeftVSlot')
obj_leftvslot_bind.TraceSupport = False
obj_leftvslot_bind.Support = [(obj_leftvslot_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_leftvslot_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-001-LeftVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftVSlot_bind')

obj_leftrail_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'LeftRail_bind')
obj_leftrail_bind_orig = App.getDocument('frame').getObject('LeftRail')
obj_leftrail_bind.TraceSupport = False
obj_leftrail_bind.Support = [(obj_leftrail_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_leftrail_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-002-LeftRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftRail_bind')

obj_leftmgn_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'LeftMGN_bind')
obj_leftmgn_bind_orig = App.getDocument('frame').getObject('LeftMGN')
obj_leftmgn_bind.TraceSupport = False
obj_leftmgn_bind.Support = [(obj_leftmgn_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_leftmgn_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-003-LeftMGN_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftMGN_bind')

obj_lefttopbelt_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'LeftTopBelt_bind')
obj_lefttopbelt_bind_orig = App.getDocument('frame').getObject('LeftTopBelt')
obj_lefttopbelt_bind.TraceSupport = False
obj_lefttopbelt_bind.Support = [(obj_lefttopbelt_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_lefttopbelt_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-004-LeftTopBelt_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftTopBelt_bind')

obj_leftbottombelt_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'LeftBottomBelt_bind')
obj_leftbottombelt_bind_orig = App.getDocument('frame').getObject('LeftBottomBelt')
obj_leftbottombelt_bind.TraceSupport = False
obj_leftbottombelt_bind.Support = [(obj_leftbottombelt_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_leftbottombelt_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-005-LeftBottomBelt_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('LeftBottomBelt_bind')

obj_xleftmotor_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XLeftMotor_bind')
obj_xleftmotor_bind_orig = App.getDocument('frame').getObject('XLeftMotor')
obj_xleftmotor_bind.TraceSupport = False
obj_xleftmotor_bind.Support = [(obj_xleftmotor_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xleftmotor_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-006-XLeftMotor_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XLeftMotor_bind')

obj_xleftidler_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XLeftIdler_bind')
obj_xleftidler_bind_orig = App.getDocument('frame').getObject('XLeftIdler')
obj_xleftidler_bind.TraceSupport = False
obj_xleftidler_bind.Support = [(obj_xleftidler_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xleftidler_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-007-XLeftIdler_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XLeftIdler_bind')

obj_xvslot_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XVSlot_bind')
obj_xvslot_bind_orig = App.getDocument('frame').getObject('XVSlot')
obj_xvslot_bind.TraceSupport = False
obj_xvslot_bind.Support = [(obj_xvslot_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xvslot_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-008-XVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XVSlot_bind')

obj_xfrontrail_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XFrontRail_bind')
obj_xfrontrail_bind_orig = App.getDocument('frame').getObject('XFrontRail')
obj_xfrontrail_bind.TraceSupport = False
obj_xfrontrail_bind.Support = [(obj_xfrontrail_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xfrontrail_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-009-XFrontRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XFrontRail_bind')

obj_xbackrail_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XBackRail_bind')
obj_xbackrail_bind_orig = App.getDocument('frame').getObject('XBackRail')
obj_xbackrail_bind.TraceSupport = False
obj_xbackrail_bind.Support = [(obj_xbackrail_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xbackrail_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-010-XBackRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XBackRail_bind')

obj_xleftpulley_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XLeftPulley_bind')
obj_xleftpulley_bind_orig = App.getDocument('frame').getObject('XLeftPulley')
obj_xleftpulley_bind.TraceSupport = False
obj_xleftpulley_bind.Support = [(obj_xleftpulley_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xleftpulley_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-011-XLeftPulley_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XLeftPulley_bind')

obj_sketch = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch')
obj_sketch.Support = (obj_leftmgn_bind, ['Face491'])
obj_sketch.MapMode = 'FlatFace'
obj_sketch_vector_1 = App.Vector(-23.000, 44.401, 0.000)
obj_sketch_vector_2 = App.Vector(61.150, 44.401, 0.000)
obj_sketch_vector_3 = App.Vector(61.150, 0.001, 0.000)
obj_sketch_vector_4 = App.Vector(-10.000, 12.201, 0.000)
obj_sketch_vector_5 = App.Vector(10.000, 12.201, 0.000)
obj_sketch_vector_6 = App.Vector(10.000, 32.201, 0.000)
obj_sketch_vector_7 = App.Vector(-10.000, 32.201, 0.000)
obj_sketch_vector_8 = App.Vector(90.599, 58.500, 0.000)
obj_sketch_vector_9 = App.Vector(61.150, 58.500, 0.000)
obj_sketch_vector_10 = App.Vector(61.150, 63.500, 0.000)
obj_sketch_vector_11 = App.Vector(-31.000, 44.401, 0.000)
obj_sketch_vector_12 = App.Vector(-31.000, 63.500, 0.000)
obj_sketch_vector_13 = App.Vector(-31.000, -6.000, 0.000)
obj_sketch_vector_14 = App.Vector(50.000, -6.000, 0.000)
obj_sketch_vector_15 = App.Vector(50.000, 2.000, 0.000)
obj_sketch_vector_16 = App.Vector(90.599, 2.000, 0.000)
obj_sketch_vector_17 = App.Vector(90.599, 63.500, 0.000)
obj_sketch_point_1 = Part.Point(obj_sketch_vector_1)
obj_sketch_point_2 = Part.Point(obj_sketch_vector_2)
obj_sketch_point_3 = Part.Point(obj_sketch_vector_3)
obj_sketch_point_4 = Part.Point(obj_sketch_vector_4)
obj_sketch_point_5 = Part.Point(obj_sketch_vector_5)
obj_sketch_point_6 = Part.Point(obj_sketch_vector_6)
obj_sketch_point_7 = Part.Point(obj_sketch_vector_7)
obj_sketch_circle_1 = Part.Circle(obj_sketch_vector_6, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_2 = Part.Circle(obj_sketch_vector_7, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_3 = Part.Circle(obj_sketch_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_4 = Part.Circle(obj_sketch_vector_5, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_point_8 = Part.Point(obj_sketch_vector_8)
obj_sketch_point_9 = Part.Point(obj_sketch_vector_9)
obj_sketch_point_10 = Part.Point(obj_sketch_vector_10)
obj_sketch_point_11 = Part.Point(obj_sketch_vector_11)
obj_sketch_line_1 = Part.LineSegment(obj_sketch_vector_12, obj_sketch_vector_13)
obj_sketch_line_2 = Part.LineSegment(obj_sketch_vector_13, obj_sketch_vector_14)
obj_sketch_line_3 = Part.LineSegment(obj_sketch_vector_14, obj_sketch_vector_15)
obj_sketch_line_4 = Part.LineSegment(obj_sketch_vector_15, obj_sketch_vector_16)
obj_sketch_line_5 = Part.LineSegment(obj_sketch_vector_16, obj_sketch_vector_17)
obj_sketch_line_6 = Part.LineSegment(obj_sketch_vector_17, obj_sketch_vector_12)
obj_sketch_all_geoms = [obj_sketch_point_1, obj_sketch_point_2, obj_sketch_point_3, obj_sketch_point_4, obj_sketch_point_5, obj_sketch_point_6, obj_sketch_point_7, obj_sketch_circle_1, obj_sketch_circle_2, obj_sketch_circle_3, obj_sketch_circle_4, obj_sketch_point_8, obj_sketch_point_9, obj_sketch_point_10, obj_sketch_point_11, obj_sketch_line_1, obj_sketch_line_2, obj_sketch_line_3, obj_sketch_line_4, obj_sketch_line_5, obj_sketch_line_6]
obj_sketch.addGeometry(obj_sketch_all_geoms, False)
obj_sketch_all_ext_geoms = [[obj_leftmgn_bind, 'Edge9'], [obj_leftmgn_bind, 'Edge11'], [obj_leftmgn_bind, 'Edge25'], [obj_leftmgn_bind, 'Edge23'], [obj_leftmgn_bind, 'Edge16'], [obj_leftmgn_bind, 'Edge18'], [obj_leftmgn_bind, 'Edge4'], [obj_leftmgn_bind, 'Edge2'], [obj_leftmgn_bind, 'Face326'], [obj_leftmgn_bind, 'Face177'], [obj_leftmgn_bind, 'Face489'], [obj_leftmgn_bind, 'Face493'], [obj_xleftmotor_bind, 'Face4'], [obj_xleftmotor_bind, 'Face12'], [obj_xleftmotor_bind, 'Face8'], [obj_lefttopbelt_bind, 'Face4'], [obj_lefttopbelt_bind, 'Face3'], [obj_xvslot_bind, 'Face36'], [obj_xvslot_bind, 'Face57'], [obj_xvslot_bind, 'Face12'], [obj_xleftidler_bind, 'Face49'], [obj_xleftidler_bind, 'Edge64'], [obj_xleftidler_bind, 'Edge62'], [obj_xfrontrail_bind, 'Face175'], [obj_xfrontrail_bind, 'Face244']]
for a, b in obj_sketch_all_ext_geoms:
    obj_sketch.addExternal(a.Name, b)
obj_sketch_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Face177'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftmotor_bind, 'Face8'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_lefttopbelt_bind, 'Face4'])-3,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Face177'])-3,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Face326'])-3,
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftmotor_bind, 'Face8'])-3,
    ),
    # 6
    Sketcher.Constraint('Symmetric',
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge9'])-3, 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge11'])-3, 1,
        obj_sketch_all_geoms.index(obj_sketch_point_7), 1,
    ),
    # 7
    Sketcher.Constraint('Symmetric',
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge25'])-3, 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge23'])-3, 1,
        obj_sketch_all_geoms.index(obj_sketch_point_6), 1,
    ),
    # 8
    Sketcher.Constraint('Symmetric',
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge2'])-3, 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge4'])-3, 1,
        obj_sketch_all_geoms.index(obj_sketch_point_4), 1,
    ),
    # 9
    Sketcher.Constraint('Symmetric',
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge16'])-3, 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Edge18'])-3, 1,
        obj_sketch_all_geoms.index(obj_sketch_point_5), 1,
    ),
    # 10
    Sketcher.Constraint('Radius',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 1.6,
    ),
    # 11
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_1),
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
    ),
    # 12
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_1),
        obj_sketch_all_geoms.index(obj_sketch_circle_3),
    ),
    # 13
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_1),
        obj_sketch_all_geoms.index(obj_sketch_circle_4),
    ),
    # 14
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
        obj_sketch_all_geoms.index(obj_sketch_point_7), 1,
    ),
    # 15
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
        obj_sketch_all_geoms.index(obj_sketch_point_6), 1,
    ),
    # 16
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_point_4), 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_4), 3,
        obj_sketch_all_geoms.index(obj_sketch_point_5), 1,
    ),
    # 18
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_8), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftidler_bind, 'Face49'])-3,
    ),
    # 19
    Sketcher.Constraint('DistanceX',
        -obj_sketch_all_ext_geoms.index([obj_xleftidler_bind, 'Edge62'])-3, 2,
        obj_sketch_all_geoms.index(obj_sketch_point_8), 1,
        10.0,
    ),
    # 20
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_point_9), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_10), 1,
        5.0,
    ),
    # 21
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_9), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftmotor_bind, 'Face8'])-3,
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_9), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftidler_bind, 'Face49'])-3,
    ),
    # 23
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_10), 1,
        -obj_sketch_all_ext_geoms.index([obj_xleftmotor_bind, 'Face8'])-3,
    ),
    # 24
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_point_11), 1,
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        8.0,
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_11), 1,
        -obj_sketch_all_ext_geoms.index([obj_leftmgn_bind, 'Face177'])-3,
    ),
    # 26
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
    ),
    # 27
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
    ),
    # 28
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 1,
    ),
    # 29
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
    ),
    # 30
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 1,
    ),
    # 31
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        -obj_sketch_all_ext_geoms.index([obj_xfrontrail_bind, 'Face175'])-3,
    ),
    # 32
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        -obj_sketch_all_ext_geoms.index([obj_xfrontrail_bind, 'Face244'])-3,
    ),
    # 33
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
    ),
    # 34
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_11), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 35
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 36
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_2),
    ),
    # 37
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_3),
    ),
    # 38
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        -obj_sketch_all_ext_geoms.index([obj_xvslot_bind, 'Face36'])-3,
    ),
    # 39
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 40
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 41
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_8), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 42
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_10), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 43
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_6),
    ),
    # 44
]
obj_sketch.addConstraint(obj_sketch_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-012-Sketch.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch')

obj_pad = body_left_y_carriage_plate.newObject('PartDesign::Pad', 'Pad')
obj_pad.Label = 'Pad'
obj_pad.Profile = (obj_sketch, [])
obj_pad.Length = '5 mm'
obj_pad.Length2 = '100 mm'
obj_pad.Type = 'Length'
obj_pad.UpToFace = None
obj_pad.Reversed = False
obj_pad.Midplane = False
obj_pad.Offset = '0 mm'
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pad
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-013-Pad.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad')

obj_sketch001 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch001')
obj_sketch001.Support = (obj_pad, ['Face11'])
obj_sketch001.MapMode = 'FlatFace'
obj_sketch001_vector_1 = App.Vector(66.150, -44.500, 0.000)
obj_sketch001_vector_2 = App.Vector(90.599, -44.500, 0.000)
obj_sketch001_vector_3 = App.Vector(90.599, -63.500, 0.000)
obj_sketch001_vector_4 = App.Vector(61.150, -63.500, 0.000)
obj_sketch001_vector_5 = App.Vector(61.150, -7.000, 0.000)
obj_sketch001_vector_6 = App.Vector(18.850, -7.000, 0.000)
obj_sketch001_vector_7 = App.Vector(18.850, -37.000, 0.000)
obj_sketch001_vector_8 = App.Vector(13.295, -37.000, 0.000)
obj_sketch001_vector_9 = App.Vector(13.295, -2.000, 0.000)
obj_sketch001_vector_10 = App.Vector(66.150, -2.000, 0.000)
obj_sketch001_vector_11 = App.Vector(90.599, -49.500, 0.000)
obj_sketch001_line_1 = Part.LineSegment(obj_sketch001_vector_1, obj_sketch001_vector_2)
obj_sketch001_line_2 = Part.LineSegment(obj_sketch001_vector_2, obj_sketch001_vector_3)
obj_sketch001_line_3 = Part.LineSegment(obj_sketch001_vector_3, obj_sketch001_vector_4)
obj_sketch001_line_4 = Part.LineSegment(obj_sketch001_vector_4, obj_sketch001_vector_5)
obj_sketch001_line_5 = Part.LineSegment(obj_sketch001_vector_5, obj_sketch001_vector_6)
obj_sketch001_line_6 = Part.LineSegment(obj_sketch001_vector_6, obj_sketch001_vector_7)
obj_sketch001_line_7 = Part.LineSegment(obj_sketch001_vector_7, obj_sketch001_vector_8)
obj_sketch001_line_8 = Part.LineSegment(obj_sketch001_vector_8, obj_sketch001_vector_9)
obj_sketch001_line_9 = Part.LineSegment(obj_sketch001_vector_9, obj_sketch001_vector_10)
obj_sketch001_line_10 = Part.LineSegment(obj_sketch001_vector_10, obj_sketch001_vector_1)
obj_sketch001_point_1 = Part.Point(obj_sketch001_vector_11)
obj_sketch001_all_geoms = [obj_sketch001_line_1, obj_sketch001_line_2, obj_sketch001_line_3, obj_sketch001_line_4, obj_sketch001_line_5, obj_sketch001_line_6, obj_sketch001_line_7, obj_sketch001_line_8, obj_sketch001_line_9, obj_sketch001_line_10, obj_sketch001_point_1]
obj_sketch001.addGeometry(obj_sketch001_all_geoms, False)
obj_sketch001_all_ext_geoms = [[obj_xleftidler_bind, 'Face45'], [obj_xleftidler_bind, 'Face49'], [obj_pad, 'Edge15'], [obj_xleftmotor_bind, 'Face45'], [obj_xleftmotor_bind, 'Face12'], [obj_xleftmotor_bind, 'Face47'], [obj_leftmgn_bind, 'Face446']]
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
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 1,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 1,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 1,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 1,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1),
    ),
    # 11
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3),
    ),
    # 12
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5),
    ),
    # 13
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9),
    ),
    # 14
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7),
    ),
    # 15
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8),
    ),
    # 16
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6),
    ),
    # 17
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4),
    ),
    # 18
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10),
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 20
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge15'])-3, 2,
    ),
    # 21
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        -obj_sketch001_all_ext_geoms.index([obj_xleftmotor_bind, 'Face45'])-3,
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        -obj_sketch001_all_ext_geoms.index([obj_xleftmotor_bind, 'Face12'])-3,
    ),
    # 23
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge15'])-3, 1,
    ),
    # 24
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        -obj_sketch001_all_ext_geoms.index([obj_xleftmotor_bind, 'Face47'])-3,
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
        -obj_sketch001_all_ext_geoms.index([obj_leftmgn_bind, 'Face446'])-3,
    ),
    # 26
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_5), 2,
        30.0,
    ),
    # 27
    Sketcher.Constraint('DistanceX',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        5.0,
    ),
    # 28
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 29
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
        -obj_sketch001_all_ext_geoms.index([obj_xleftidler_bind, 'Face45'])-3,
    ),
    # 30
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_point_1), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
        5.0,
    ),
    # 31
]
obj_sketch001.addConstraint(obj_sketch001_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch001
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-014-Sketch001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch001')

obj_pad001 = body_left_y_carriage_plate.newObject('PartDesign::Pad', 'Pad001')
obj_pad001.Label = 'Pad001'
obj_pad001.Profile = (obj_sketch001, [])
obj_pad001.Length = '42 mm'
obj_pad001.Length2 = '100 mm'
obj_pad001.Type = 'Length'
obj_pad001.UpToFace = None
obj_pad001.Reversed = False
obj_pad001.Midplane = False
obj_pad001.Offset = '0 mm'
obj_pad001.BaseFeature = obj_pad
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pad001
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-015-Pad001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad001')

obj_sketch002 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch002')
obj_sketch002.Support = (obj_pad001, ['Face21'])
obj_sketch002.MapMode = 'FlatFace'
obj_sketch002_vector_1 = App.Vector(50.200, -7.401, 0.000)
obj_sketch002_vector_2 = App.Vector(57.800, -8.599, 0.000)
obj_sketch002_vector_3 = App.Vector(57.800, -7.401, 0.000)
obj_sketch002_vector_4 = App.Vector(50.200, -8.599, 0.000)
obj_sketch002_vector_5 = App.Vector(54.000, -8.000, 0.000)
obj_sketch002_vector_6 = App.Vector(47.500, 3.000, 0.000)
obj_sketch002_vector_7 = App.Vector(60.500, 3.000, 0.000)
obj_sketch002_vector_8 = App.Vector(60.500, -19.000, 0.000)
obj_sketch002_vector_9 = App.Vector(47.500, -19.000, 0.000)
obj_sketch002_line_1 = Part.LineSegment(obj_sketch002_vector_1, obj_sketch002_vector_2)
obj_sketch002_line_1.Construction = True
obj_sketch002_line_2 = Part.LineSegment(obj_sketch002_vector_3, obj_sketch002_vector_4)
obj_sketch002_line_2.Construction = True
obj_sketch002_point_1 = Part.Point(obj_sketch002_vector_5)
obj_sketch002_line_3 = Part.LineSegment(obj_sketch002_vector_6, obj_sketch002_vector_7)
obj_sketch002_line_4 = Part.LineSegment(obj_sketch002_vector_7, obj_sketch002_vector_8)
obj_sketch002_line_5 = Part.LineSegment(obj_sketch002_vector_8, obj_sketch002_vector_9)
obj_sketch002_line_6 = Part.LineSegment(obj_sketch002_vector_9, obj_sketch002_vector_6)
obj_sketch002_all_geoms = [obj_sketch002_line_1, obj_sketch002_line_2, obj_sketch002_point_1, obj_sketch002_line_3, obj_sketch002_line_4, obj_sketch002_line_5, obj_sketch002_line_6]
obj_sketch002.addGeometry(obj_sketch002_all_geoms, False)
obj_sketch002_all_ext_geoms = [[obj_xleftidler_bind, 'Face45'], [obj_xleftidler_bind, 'Face49'], [obj_xleftidler_bind, 'Edge121'], [obj_xleftidler_bind, 'Edge45']]
for a, b in obj_sketch002_all_ext_geoms:
    obj_sketch002.addExternal(a.Name, b)
obj_sketch002_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        -obj_sketch002_all_ext_geoms.index([obj_xleftidler_bind, 'Edge121'])-3, 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 2,
        -obj_sketch002_all_ext_geoms.index([obj_xleftidler_bind, 'Edge45'])-3, 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 1,
        -obj_sketch002_all_ext_geoms.index([obj_xleftidler_bind, 'Edge121'])-3, 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        -obj_sketch002_all_ext_geoms.index([obj_xleftidler_bind, 'Edge45'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1),
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_2),
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_4), 1,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_4), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_6), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_6), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
    ),
    # 10
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3),
    ),
    # 11
    Sketcher.Constraint('Horizontal',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5),
    ),
    # 12
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_line_4),
    ),
    # 13
    Sketcher.Constraint('Vertical',
        obj_sketch002_all_geoms.index(obj_sketch002_line_6),
    ),
    # 14
    Sketcher.Constraint('Symmetric',
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_point_1), 1,
    ),
    # 15
    Sketcher.Constraint('DistanceX',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_4), 2,
        13.0,
    ),
    # 16
    Sketcher.Constraint('DistanceY',
        obj_sketch002_all_geoms.index(obj_sketch002_line_5), 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 1,
        22.0,
    ),
    # 17
]
obj_sketch002.addConstraint(obj_sketch002_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch002
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-016-Sketch002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch002')

obj_pocket = body_left_y_carriage_plate.newObject('PartDesign::Pocket', 'Pocket')
obj_pocket.Label = 'Pocket'
obj_pocket.Profile = (obj_sketch002, [])
obj_pocket.Length = '30 mm'
obj_pocket.Length2 = '100 mm'
obj_pocket.Type = 'Length'
obj_pocket.UpToFace = None
obj_pocket.Reversed = False
obj_pocket.Midplane = False
obj_pocket.Offset = '0 mm'
obj_pocket.BaseFeature = obj_pad001
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pocket
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-017-Pocket.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket')

obj_sketch003 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch003')
obj_sketch003.Support = (obj_pocket, ['Face7'])
obj_sketch003.MapMode = 'FlatFace'
obj_sketch003_vector_1 = App.Vector(-75.875, 13.000, 0.000)
obj_sketch003_vector_2 = App.Vector(-75.875, -8.000, 0.000)
obj_sketch003_vector_3 = App.Vector(-85.599, -8.000, 0.000)
obj_sketch003_vector_4 = App.Vector(-75.599, -8.000, 0.000)
obj_sketch003_line_1 = Part.LineSegment(obj_sketch003_vector_1, obj_sketch003_vector_2)
obj_sketch003_line_1.Construction = True
obj_sketch003_line_2 = Part.LineSegment(obj_sketch003_vector_3, obj_sketch003_vector_4)
obj_sketch003_line_2.Construction = True
obj_sketch003_circle_1 = Part.Circle(obj_sketch003_vector_3, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_circle_2 = Part.Circle(obj_sketch003_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch003_all_geoms = [obj_sketch003_line_1, obj_sketch003_line_2, obj_sketch003_circle_1, obj_sketch003_circle_2]
obj_sketch003.addGeometry(obj_sketch003_all_geoms, False)
obj_sketch003_all_ext_geoms = [[obj_pocket, 'Edge6']]
for a, b in obj_sketch003_all_ext_geoms:
    obj_sketch003.addExternal(a.Name, b)
obj_sketch003_constraints = [
    Sketcher.Constraint('Vertical',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1),
    ),
    # 1
    Sketcher.Constraint('Symmetric',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge6'])-3, 1,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge6'])-3, 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
    ),
    # 2
    Sketcher.Constraint('DistanceY',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge6'])-3, 1,
        21.0,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2),
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2),
    ),
    # 5
    Sketcher.Constraint('DistanceX',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge6'])-3, 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
        5.0,
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        10.0,
    ),
    # 7
    Sketcher.Constraint('Radius',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_2), 1.6,
    ),
    # 8
    Sketcher.Constraint('Equal',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_2),
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1),
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_1), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_circle_2), 3,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
    ),
    # 11
]
obj_sketch003.addConstraint(obj_sketch003_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch003
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-018-Sketch003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch003')

obj_pocket001 = body_left_y_carriage_plate.newObject('PartDesign::Pocket', 'Pocket001')
obj_pocket001.Label = 'Pocket001'
obj_pocket001.Profile = (obj_sketch003, [])
obj_pocket001.Length = '5 mm'
obj_pocket001.Length2 = '100 mm'
obj_pocket001.Type = 'Length'
obj_pocket001.UpToFace = None
obj_pocket001.Reversed = False
obj_pocket001.Midplane = False
obj_pocket001.Offset = '0 mm'
obj_pocket001.BaseFeature = obj_pocket
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pocket001
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-019-Pocket001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket001')

obj_sketch004 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch004')
obj_sketch004.Support = (obj_pocket001, ['Face4'])
obj_sketch004.MapMode = 'FlatFace'
obj_sketch004_vector_1 = App.Vector(-31.000, 6.000, 0.000)
obj_sketch004_vector_2 = App.Vector(-13.295, 6.000, 0.000)
obj_sketch004_vector_3 = App.Vector(-13.295, -63.500, 0.000)
obj_sketch004_vector_4 = App.Vector(-31.000, -63.500, 0.000)
obj_sketch004_line_1 = Part.LineSegment(obj_sketch004_vector_1, obj_sketch004_vector_2)
obj_sketch004_line_2 = Part.LineSegment(obj_sketch004_vector_2, obj_sketch004_vector_3)
obj_sketch004_line_3 = Part.LineSegment(obj_sketch004_vector_3, obj_sketch004_vector_4)
obj_sketch004_line_4 = Part.LineSegment(obj_sketch004_vector_4, obj_sketch004_vector_1)
obj_sketch004_all_geoms = [obj_sketch004_line_1, obj_sketch004_line_2, obj_sketch004_line_3, obj_sketch004_line_4]
obj_sketch004.addGeometry(obj_sketch004_all_geoms, False)
obj_sketch004_all_ext_geoms = [[obj_lefttopbelt_bind, 'Face4'], [obj_pocket001, 'Edge3'], [obj_lefttopbelt_bind, 'Face3'], [obj_leftmgn_bind, 'Face442'], [obj_pocket001, 'Edge10'], [obj_pocket001, 'Edge7']]
for a, b in obj_sketch004_all_ext_geoms:
    obj_sketch004.addExternal(a.Name, b)
obj_sketch004_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4), 2,
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_4),
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        -obj_sketch004_all_ext_geoms.index([obj_leftmgn_bind, 'Face442'])-3,
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge7'])-3,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Edge10'])-3, 1,
    ),
    # 11
]
obj_sketch004.addConstraint(obj_sketch004_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch004
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-020-Sketch004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch004')

obj_pad002 = body_left_y_carriage_plate.newObject('PartDesign::Pad', 'Pad002')
obj_pad002.Label = 'Pad002'
obj_pad002.Profile = (obj_sketch004, [])
obj_pad002.Length = '10 mm'
obj_pad002.Length2 = '100 mm'
obj_pad002.Type = 'Length'
obj_pad002.UpToFace = None
obj_pad002.Reversed = False
obj_pad002.Midplane = False
obj_pad002.Offset = '0 mm'
obj_pad002.BaseFeature = obj_pocket001
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pad002
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-021-Pad002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad002')

obj_sketch005 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch005')
obj_sketch005.Support = (obj_pad002, ['Face12'])
obj_sketch005.MapMode = 'FlatFace'
obj_sketch005_vector_1 = App.Vector(-23.000, 6.000, 0.000)
obj_sketch005_vector_2 = App.Vector(-17.000, 6.000, 0.000)
obj_sketch005_vector_3 = App.Vector(-17.000, -63.500, 0.000)
obj_sketch005_vector_4 = App.Vector(-23.000, -63.500, 0.000)
obj_sketch005_line_1 = Part.LineSegment(obj_sketch005_vector_1, obj_sketch005_vector_2)
obj_sketch005_line_2 = Part.LineSegment(obj_sketch005_vector_2, obj_sketch005_vector_3)
obj_sketch005_line_3 = Part.LineSegment(obj_sketch005_vector_3, obj_sketch005_vector_4)
obj_sketch005_line_4 = Part.LineSegment(obj_sketch005_vector_4, obj_sketch005_vector_1)
obj_sketch005_all_geoms = [obj_sketch005_line_1, obj_sketch005_line_2, obj_sketch005_line_3, obj_sketch005_line_4]
obj_sketch005.addGeometry(obj_sketch005_all_geoms, False)
obj_sketch005_all_ext_geoms = [[obj_lefttopbelt_bind, 'Edge9'], [obj_lefttopbelt_bind, 'Edge11'], [obj_pad002, 'Edge48'], [obj_pad002, 'Edge45']]
for a, b in obj_sketch005_all_ext_geoms:
    obj_sketch005.addExternal(a.Name, b)
obj_sketch005_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_2), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch005_all_geoms.index(obj_sketch005_line_4), 2,
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 1,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3),
    ),
    # 6
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_line_2),
    ),
    # 7
    Sketcher.Constraint('Vertical',
        obj_sketch005_all_geoms.index(obj_sketch005_line_4),
    ),
    # 8
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 1,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge48'])-3,
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 2,
        -obj_sketch005_all_ext_geoms.index([obj_pad002, 'Edge45'])-3,
    ),
    # 10
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_line_3), 2,
        -obj_sketch005_all_ext_geoms.index([obj_lefttopbelt_bind, 'Edge11'])-3,
    ),
    # 11
    Sketcher.Constraint('PointOnObject',
        obj_sketch005_all_geoms.index(obj_sketch005_line_1), 2,
        -obj_sketch005_all_ext_geoms.index([obj_lefttopbelt_bind, 'Edge9'])-3,
    ),
    # 12
]
obj_sketch005.addConstraint(obj_sketch005_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch005
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-022-Sketch005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch005')

obj_pocket002 = body_left_y_carriage_plate.newObject('PartDesign::Pocket', 'Pocket002')
obj_pocket002.Label = 'Pocket002'
obj_pocket002.Profile = (obj_sketch005, [])
obj_pocket002.Length = '5 mm'
obj_pocket002.Length2 = '100 mm'
obj_pocket002.Type = 'Length'
obj_pocket002.UpToFace = None
obj_pocket002.Reversed = False
obj_pocket002.Midplane = False
obj_pocket002.Offset = '0 mm'
obj_pocket002.BaseFeature = obj_pad002
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pocket002
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-023-Pocket002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket002')

obj_sketch006 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch006')
obj_sketch006.Support = (obj_pocket002, ['Face31'])
obj_sketch006.MapMode = 'FlatFace'
obj_sketch006_vector_1 = App.Vector(-23.000, 6.000, 0.000)
obj_sketch006_vector_2 = App.Vector(-17.000, -63.500, 0.000)
obj_sketch006_vector_3 = App.Vector(-23.000, -63.500, 0.000)
obj_sketch006_vector_4 = App.Vector(-17.000, 6.000, 0.000)
obj_sketch006_vector_5 = App.Vector(-20.000, -28.750, 0.000)
obj_sketch006_vector_6 = App.Vector(-23.000, -18.750, 0.000)
obj_sketch006_vector_7 = App.Vector(-17.000, -18.750, 0.000)
obj_sketch006_vector_8 = App.Vector(-17.000, -23.750, 0.000)
obj_sketch006_vector_9 = App.Vector(-23.000, -23.750, 0.000)
obj_sketch006_vector_10 = App.Vector(-23.000, -33.750, 0.000)
obj_sketch006_vector_11 = App.Vector(-17.000, -33.750, 0.000)
obj_sketch006_vector_12 = App.Vector(-17.000, -38.750, 0.000)
obj_sketch006_vector_13 = App.Vector(-23.000, -38.750, 0.000)
obj_sketch006_line_1 = Part.LineSegment(obj_sketch006_vector_1, obj_sketch006_vector_2)
obj_sketch006_line_1.Construction = True
obj_sketch006_line_2 = Part.LineSegment(obj_sketch006_vector_3, obj_sketch006_vector_4)
obj_sketch006_line_2.Construction = True
obj_sketch006_point_1 = Part.Point(obj_sketch006_vector_5)
obj_sketch006_circle_1 = Part.Circle(obj_sketch006_vector_5, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch006_line_3 = Part.LineSegment(obj_sketch006_vector_6, obj_sketch006_vector_7)
obj_sketch006_line_4 = Part.LineSegment(obj_sketch006_vector_7, obj_sketch006_vector_8)
obj_sketch006_line_5 = Part.LineSegment(obj_sketch006_vector_8, obj_sketch006_vector_9)
obj_sketch006_line_6 = Part.LineSegment(obj_sketch006_vector_9, obj_sketch006_vector_6)
obj_sketch006_line_7 = Part.LineSegment(obj_sketch006_vector_10, obj_sketch006_vector_11)
obj_sketch006_line_8 = Part.LineSegment(obj_sketch006_vector_11, obj_sketch006_vector_12)
obj_sketch006_line_9 = Part.LineSegment(obj_sketch006_vector_12, obj_sketch006_vector_13)
obj_sketch006_line_10 = Part.LineSegment(obj_sketch006_vector_13, obj_sketch006_vector_10)
obj_sketch006_all_geoms = [obj_sketch006_line_1, obj_sketch006_line_2, obj_sketch006_point_1, obj_sketch006_circle_1, obj_sketch006_line_3, obj_sketch006_line_4, obj_sketch006_line_5, obj_sketch006_line_6, obj_sketch006_line_7, obj_sketch006_line_8, obj_sketch006_line_9, obj_sketch006_line_10]
obj_sketch006.addGeometry(obj_sketch006_all_geoms, False)
obj_sketch006_all_ext_geoms = [[obj_pocket002, 'Edge97'], [obj_pocket002, 'Edge57']]
for a, b in obj_sketch006_all_ext_geoms:
    obj_sketch006.addExternal(a.Name, b)
obj_sketch006_constraints = [
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge57'])-3, 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge97'])-3, 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge57'])-3, 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge97'])-3, 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1),
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2),
    ),
    # 6
    Sketcher.Constraint('Radius',
        obj_sketch006_all_geoms.index(obj_sketch006_circle_1), 1.6,
    ),
    # 7
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_circle_1), 3,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
    ),
    # 8
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_6), 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_6), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 1,
    ),
    # 12
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_3),
    ),
    # 13
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_5),
    ),
    # 14
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_4),
    ),
    # 15
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_6),
    ),
    # 16
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_8), 1,
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_8), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_9), 1,
    ),
    # 18
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_9), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_10), 1,
    ),
    # 19
    Sketcher.Constraint('Coincident',
        obj_sketch006_all_geoms.index(obj_sketch006_line_10), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 1,
    ),
    # 20
    Sketcher.Constraint('Horizontal',
        obj_sketch006_all_geoms.index(obj_sketch006_line_9),
    ),
    # 21
    Sketcher.Constraint('Vertical',
        obj_sketch006_all_geoms.index(obj_sketch006_line_8),
    ),
    # 22
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 2,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge97'])-3,
    ),
    # 23
    Sketcher.Constraint('PointOnObject',
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 1,
        -obj_sketch006_all_ext_geoms.index([obj_pocket002, 'Edge57'])-3,
    ),
    # 24
    Sketcher.Constraint('Symmetric',
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_4), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
    ),
    # 25
    Sketcher.Constraint('Symmetric',
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_7), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
    ),
    # 26
    Sketcher.Constraint('Symmetric',
        obj_sketch006_all_geoms.index(obj_sketch006_line_9), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
    ),
    # 27
    Sketcher.Constraint('DistanceY',
        obj_sketch006_all_geoms.index(obj_sketch006_point_1), 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 2,
        5.0,
    ),
    # 28
    Sketcher.Constraint('DistanceY',
        obj_sketch006_all_geoms.index(obj_sketch006_line_5), 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 1,
        5.0,
    ),
    # 29
]
obj_sketch006.addConstraint(obj_sketch006_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch006
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-024-Sketch006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch006')

obj_pocket003 = body_left_y_carriage_plate.newObject('PartDesign::Pocket', 'Pocket003')
obj_pocket003.Label = 'Pocket003'
obj_pocket003.Profile = (obj_sketch006, [])
obj_pocket003.Length = '15 mm'
obj_pocket003.Length2 = '100 mm'
obj_pocket003.Type = 'Length'
obj_pocket003.UpToFace = None
obj_pocket003.Reversed = False
obj_pocket003.Midplane = False
obj_pocket003.Offset = '0 mm'
obj_pocket003.BaseFeature = obj_pocket002
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pocket003
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pocket003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-025-Pocket003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket003')

obj_sketch007 = body_left_y_carriage_plate.newObject('Sketcher::SketchObject', 'Sketch007')
obj_sketch007.Support = (obj_pocket003, ['Face27'])
obj_sketch007.MapMode = 'FlatFace'
obj_sketch007_vector_1 = App.Vector(66.150, -12.000, 0.000)
obj_sketch007_vector_2 = App.Vector(90.599, -12.000, 0.000)
obj_sketch007_vector_3 = App.Vector(66.150, -32.000, 0.000)
obj_sketch007_vector_4 = App.Vector(90.599, -32.000, 0.000)
obj_sketch007_vector_5 = App.Vector(90.599, -2.000, 0.000)
obj_sketch007_vector_6 = App.Vector(85.599, -12.000, 0.000)
obj_sketch007_vector_7 = App.Vector(70.599, -12.000, 0.000)
obj_sketch007_vector_8 = App.Vector(70.599, -32.000, 0.000)
obj_sketch007_vector_9 = App.Vector(85.599, -32.000, 0.000)
obj_sketch007_line_1 = Part.LineSegment(obj_sketch007_vector_1, obj_sketch007_vector_2)
obj_sketch007_line_1.Construction = True
obj_sketch007_line_2 = Part.LineSegment(obj_sketch007_vector_3, obj_sketch007_vector_4)
obj_sketch007_line_2.Construction = True
obj_sketch007_point_1 = Part.Point(obj_sketch007_vector_5)
obj_sketch007_circle_1 = Part.Circle(obj_sketch007_vector_6, App.Vector (0.0, 0.0, 1.0), 2.0)
obj_sketch007_circle_2 = Part.Circle(obj_sketch007_vector_7, App.Vector (0.0, 0.0, 1.0), 2.0)
obj_sketch007_circle_3 = Part.Circle(obj_sketch007_vector_8, App.Vector (0.0, 0.0, 1.0), 2.0)
obj_sketch007_circle_4 = Part.Circle(obj_sketch007_vector_9, App.Vector (0.0, 0.0, 1.0), 2.0)
obj_sketch007_all_geoms = [obj_sketch007_line_1, obj_sketch007_line_2, obj_sketch007_point_1, obj_sketch007_circle_1, obj_sketch007_circle_2, obj_sketch007_circle_3, obj_sketch007_circle_4]
obj_sketch007.addGeometry(obj_sketch007_all_geoms, False)
obj_sketch007_all_ext_geoms = [[obj_xvslot_bind, 'Face36'], [obj_pocket003, 'Face6'], [obj_pocket003, 'Edge106']]
for a, b in obj_sketch007_all_ext_geoms:
    obj_sketch007.addExternal(a.Name, b)
obj_sketch007_constraints = [
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_line_2), 1,
        -obj_sketch007_all_ext_geoms.index([obj_pocket003, 'Edge106'])-3,
    ),
    # 1
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_line_2), 2,
        -obj_sketch007_all_ext_geoms.index([obj_pocket003, 'Face6'])-3,
    ),
    # 2
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 1,
        -obj_sketch007_all_ext_geoms.index([obj_pocket003, 'Edge106'])-3,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
        -obj_sketch007_all_ext_geoms.index([obj_pocket003, 'Face6'])-3,
    ),
    # 4
    Sketcher.Constraint('Horizontal',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1),
    ),
    # 5
    Sketcher.Constraint('Horizontal',
        obj_sketch007_all_geoms.index(obj_sketch007_line_2),
    ),
    # 6
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_point_1), 1,
        -obj_sketch007_all_ext_geoms.index([obj_xvslot_bind, 'Face36'])-3,
    ),
    # 7
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_point_1), 1,
        -obj_sketch007_all_ext_geoms.index([obj_pocket003, 'Face6'])-3,
    ),
    # 8
    Sketcher.Constraint('DistanceY',
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
        obj_sketch007_all_geoms.index(obj_sketch007_point_1), 1,
        10.0,
    ),
    # 9
    Sketcher.Constraint('DistanceY',
        obj_sketch007_all_geoms.index(obj_sketch007_line_2), 2,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
        20.0,
    ),
    # 10
    Sketcher.Constraint('Radius',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3), 2.0,
    ),
    # 11
    Sketcher.Constraint('Equal',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3),
        obj_sketch007_all_geoms.index(obj_sketch007_circle_2),
    ),
    # 12
    Sketcher.Constraint('Equal',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3),
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1),
    ),
    # 13
    Sketcher.Constraint('Equal',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3),
        obj_sketch007_all_geoms.index(obj_sketch007_circle_4),
    ),
    # 14
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_2), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1),
    ),
    # 15
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1),
    ),
    # 16
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_2),
    ),
    # 17
    Sketcher.Constraint('PointOnObject',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_4), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_2),
    ),
    # 18
    Sketcher.Constraint('Vertical',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_circle_4), 3,
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_2), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_circle_3), 3,
    ),
    # 20
    Sketcher.Constraint('DistanceX',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_2), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 3,
        15.0,
    ),
    # 21
    Sketcher.Constraint('DistanceX',
        obj_sketch007_all_geoms.index(obj_sketch007_circle_1), 3,
        obj_sketch007_all_geoms.index(obj_sketch007_line_1), 2,
        5.0,
    ),
    # 22
]
obj_sketch007.addConstraint(obj_sketch007_constraints)
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_sketch007
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pocket003, obj_sketch007]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-026-Sketch007.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch007')

obj_pocket004 = body_left_y_carriage_plate.newObject('PartDesign::Pocket', 'Pocket004')
obj_pocket004.Label = 'Pocket004'
obj_pocket004.Profile = (obj_sketch007, [])
obj_pocket004.Length = '6 mm'
obj_pocket004.Length2 = '100 mm'
obj_pocket004.Type = 'Length'
obj_pocket004.UpToFace = None
obj_pocket004.Reversed = False
obj_pocket004.Midplane = False
obj_pocket004.Offset = '0 mm'
obj_pocket004.BaseFeature = obj_pocket003
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_pocket004
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pocket003, obj_sketch007, obj_pocket004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-027-Pocket004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket004')

body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xleftidler_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pad002, obj_sketch005, obj_pocket002, obj_sketch006, obj_pocket003, obj_sketch007, obj_pocket004]
body_left_y_carriage_plate.Tip = obj_pocket004
FreeCAD.ActiveDocument.recompute()

App.ActiveDocument.saveAs("plate.FCStd")
