
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
body_left_z_rod_plate_debug = False
body_left_z_rod_plate = App.activeDocument().addObject('PartDesign::Body', 'left_z_rod_plate')
body_left_z_rod_plate.Label = 'left_z_rod_plate'
obj_panelfrontvslot_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'PanelFrontVSlot_bind')
obj_panelfrontvslot_bind_orig = App.getDocument('frame').getObject('PanelFrontVSlot')
obj_panelfrontvslot_bind.TraceSupport = False
obj_panelfrontvslot_bind.Support = [(obj_panelfrontvslot_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_panelfrontvslot_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-001-PanelFrontVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('PanelFrontVSlot_bind')

obj_panelleftvslot_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'PanelLeftVSlot_bind')
obj_panelleftvslot_bind_orig = App.getDocument('frame').getObject('PanelLeftVSlot')
obj_panelleftvslot_bind.TraceSupport = False
obj_panelleftvslot_bind.Support = [(obj_panelleftvslot_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_panelleftvslot_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-002-PanelLeftVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('PanelLeftVSlot_bind')

obj_frameflrod_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'FrameFLRod_bind')
obj_frameflrod_bind_orig = App.getDocument('frame').getObject('FrameFLRod')
obj_frameflrod_bind.TraceSupport = False
obj_frameflrod_bind.Support = [(obj_frameflrod_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_frameflrod_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-003-FrameFLRod_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLRod_bind')

obj_frameflnut_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'FrameFLNut_bind')
obj_frameflnut_bind_orig = App.getDocument('frame').getObject('FrameFLNut')
obj_frameflnut_bind.TraceSupport = False
obj_frameflnut_bind.Support = [(obj_frameflnut_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_frameflnut_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-004-FrameFLNut_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLNut_bind')

obj_frameflmgn_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'FrameFLMGN_bind')
obj_frameflmgn_bind_orig = App.getDocument('frame').getObject('FrameFLMGN')
obj_frameflmgn_bind.TraceSupport = False
obj_frameflmgn_bind.Support = [(obj_frameflmgn_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_frameflmgn_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-005-FrameFLMGN_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLMGN_bind')

obj_frameflvslot_bind = body_left_z_rod_plate.newObject('PartDesign::ShapeBinder', 'FrameFLVSlot_bind')
obj_frameflvslot_bind_orig = App.getDocument('frame').getObject('FrameFLVSlot')
obj_frameflvslot_bind.TraceSupport = False
obj_frameflvslot_bind.Support = [(obj_frameflvslot_bind_orig, '')]
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_frameflvslot_bind
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-006-FrameFLVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('FrameFLVSlot_bind')

obj_sketch = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch')
obj_sketch.Support = (obj_panelleftvslot_bind, ['Face7'])
obj_sketch.MapMode = 'FlatFace'
obj_sketch_vector_1 = App.Vector(42.000, 48.500, 0.000)
obj_sketch_vector_2 = App.Vector(-10.000, 48.500, 0.000)
obj_sketch_vector_3 = App.Vector(-10.000, 0.000, 0.000)
obj_sketch_vector_4 = App.Vector(-30.000, -12.000, 0.000)
obj_sketch_vector_5 = App.Vector(-30.000, -42.000, 0.000)
obj_sketch_vector_6 = App.Vector(0.000, -42.000, 0.000)
obj_sketch_vector_7 = App.Vector(42.000, 11.500, 0.000)
obj_sketch_vector_8 = App.Vector(42.000, 16.500, 0.000)
obj_sketch_vector_9 = App.Vector(42.000, 43.500, 0.000)
obj_sketch_vector_10 = App.Vector(10.000, 48.500, 0.000)
obj_sketch_vector_11 = App.Vector(-0.000, 48.500, 0.000)
obj_sketch_vector_12 = App.Vector(-0.000, 0.000, 0.000)
obj_sketch_vector_13 = App.Vector(-15.000, -27.000, 0.000)
obj_sketch_vector_14 = App.Vector(-9.343, -21.343, 0.000)
obj_sketch_vector_15 = App.Vector(-9.343, -32.657, 0.000)
obj_sketch_vector_16 = App.Vector(-20.657, -32.657, 0.000)
obj_sketch_vector_17 = App.Vector(-20.657, -21.343, 0.000)
obj_sketch_vector_18 = App.Vector(-0.000, 38.500, 0.000)
obj_sketch_vector_19 = App.Vector(-0.000, 24.250, 0.000)
obj_sketch_vector_20 = App.Vector(-0.000, 10.000, 0.000)
obj_sketch_line_1 = Part.LineSegment(obj_sketch_vector_1, obj_sketch_vector_2)
obj_sketch_line_2 = Part.LineSegment(obj_sketch_vector_2, obj_sketch_vector_3)
obj_sketch_line_3 = Part.LineSegment(obj_sketch_vector_3, obj_sketch_vector_4)
obj_sketch_line_4 = Part.LineSegment(obj_sketch_vector_4, obj_sketch_vector_5)
obj_sketch_line_5 = Part.LineSegment(obj_sketch_vector_5, obj_sketch_vector_6)
obj_sketch_line_6 = Part.LineSegment(obj_sketch_vector_6, obj_sketch_vector_7)
obj_sketch_line_7 = Part.LineSegment(obj_sketch_vector_7, obj_sketch_vector_1)
obj_sketch_point_1 = Part.Point(obj_sketch_vector_8)
obj_sketch_point_1.Construction = True
obj_sketch_point_2 = Part.Point(obj_sketch_vector_9)
obj_sketch_point_2.Construction = True
obj_sketch_point_3 = Part.Point(obj_sketch_vector_10)
obj_sketch_point_3.Construction = True
obj_sketch_line_8 = Part.LineSegment(obj_sketch_vector_11, obj_sketch_vector_12)
obj_sketch_line_8.Construction = True
obj_sketch_circle_1 = Part.Circle(obj_sketch_vector_13, App.Vector (0.0, 0.0, 1.0), 5.0)
obj_sketch_circle_2 = Part.Circle(obj_sketch_vector_14, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_3 = Part.Circle(obj_sketch_vector_15, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_4 = Part.Circle(obj_sketch_vector_16, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_5 = Part.Circle(obj_sketch_vector_17, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch_circle_6 = Part.Circle(obj_sketch_vector_18, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_7 = Part.Circle(obj_sketch_vector_19, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_circle_8 = Part.Circle(obj_sketch_vector_20, App.Vector (0.0, 0.0, 1.0), 2.6)
obj_sketch_all_geoms = [obj_sketch_line_1, obj_sketch_line_2, obj_sketch_line_3, obj_sketch_line_4, obj_sketch_line_5, obj_sketch_line_6, obj_sketch_line_7, obj_sketch_point_1, obj_sketch_point_2, obj_sketch_point_3, obj_sketch_line_8, obj_sketch_circle_1, obj_sketch_circle_2, obj_sketch_circle_3, obj_sketch_circle_4, obj_sketch_circle_5, obj_sketch_circle_6, obj_sketch_circle_7, obj_sketch_circle_8]
obj_sketch.addGeometry(obj_sketch_all_geoms, False)
obj_sketch_all_ext_geoms = [[obj_frameflmgn_bind, 'Face489'], [obj_frameflmgn_bind, 'Face493'], [obj_frameflmgn_bind, 'Face453'], [obj_panelleftvslot_bind, 'Face5'], [obj_panelleftvslot_bind, 'Face12'], [obj_frameflnut_bind, 'Edge21'], [obj_frameflnut_bind, 'Edge17'], [obj_frameflnut_bind, 'Edge23'], [obj_frameflnut_bind, 'Edge19'], [obj_frameflnut_bind, 'Edge15'], [obj_panelleftvslot_bind, 'Face19']]
for a, b in obj_sketch_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
    obj_sketch.addExternal(a.Name, b)
obj_sketch_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_4), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_5), 1,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_6), 1,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_7), 1,
    ),
    # 6
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_line_7), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
    ),
    # 7
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflmgn_bind, 'Face453'])-3,
    ),
    # 8
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_7),
    ),
    # 9
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmgn_bind, 'Face493'])-3,
    ),
    # 10
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmgn_bind, 'Face453'])-3,
    ),
    # 11
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_line_6), 2,
        obj_sketch_all_geoms.index(obj_sketch_point_1), 1,
        5.0,
    ),
    # 12
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmgn_bind, 'Face489'])-3,
    ),
    # 13
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        -obj_sketch_all_ext_geoms.index([obj_frameflmgn_bind, 'Face453'])-3,
    ),
    # 14
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_point_2), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_1), 1,
        5.0,
    ),
    # 15
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 16
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        -obj_sketch_all_ext_geoms.index([obj_panelleftvslot_bind, 'Face5'])-3,
    ),
    # 17
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_2),
    ),
    # 18
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_2), 2,
        -obj_sketch_all_ext_geoms.index([obj_panelleftvslot_bind, 'Face12'])-3,
    ),
    # 19
    Sketcher.Constraint('Symmetric',
        obj_sketch_all_geoms.index(obj_sketch_line_3), 2,
        obj_sketch_all_geoms.index(obj_sketch_line_5), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge15'])-3, 3,
    ),
    # 20
    Sketcher.Constraint('Vertical',
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 21
    Sketcher.Constraint('Horizontal',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
    ),
    # 22
    Sketcher.Constraint('DistanceX',
        obj_sketch_all_geoms.index(obj_sketch_line_4), 2,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge15'])-3, 3,
        15.0,
    ),
    # 23
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_line_5),
        obj_sketch_all_geoms.index(obj_sketch_line_4),
    ),
    # 24
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 25
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        -obj_sketch_all_ext_geoms.index([obj_panelleftvslot_bind, 'Face19'])-3,
    ),
    # 26
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_8), 2,
        -obj_sketch_all_ext_geoms.index([obj_panelleftvslot_bind, 'Face12'])-3,
    ),
    # 27
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_line_8), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_1),
    ),
    # 28
    Sketcher.Constraint('Symmetric',
        obj_sketch_all_geoms.index(obj_sketch_line_1), 2,
        obj_sketch_all_geoms.index(obj_sketch_point_3), 1,
        obj_sketch_all_geoms.index(obj_sketch_line_8), 0,
    ),
    # 29
    Sketcher.Constraint('Radius',
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 1.6,
    ),
    # 30
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_5),
        obj_sketch_all_geoms.index(obj_sketch_circle_4),
    ),
    # 31
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_5),
        obj_sketch_all_geoms.index(obj_sketch_circle_3),
    ),
    # 32
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_5),
        obj_sketch_all_geoms.index(obj_sketch_circle_2),
    ),
    # 33
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_5), 3,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge17'])-3, 3,
    ),
    # 34
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_2), 3,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge19'])-3, 3,
    ),
    # 35
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_3), 3,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge21'])-3, 3,
    ),
    # 36
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_4), 3,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge23'])-3, 3,
    ),
    # 37
    Sketcher.Constraint('Coincident',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 3,
        -obj_sketch_all_ext_geoms.index([obj_frameflnut_bind, 'Edge15'])-3, 3,
    ),
    # 38
    Sketcher.Constraint('Radius',
        obj_sketch_all_geoms.index(obj_sketch_circle_1), 5.0,
    ),
    # 39
    Sketcher.Constraint('Radius',
        obj_sketch_all_geoms.index(obj_sketch_circle_8), 2.6,
    ),
    # 40
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_8),
        obj_sketch_all_geoms.index(obj_sketch_circle_7),
    ),
    # 41
    Sketcher.Constraint('Equal',
        obj_sketch_all_geoms.index(obj_sketch_circle_8),
        obj_sketch_all_geoms.index(obj_sketch_circle_6),
    ),
    # 42
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_circle_6), 3,
        obj_sketch_all_geoms.index(obj_sketch_line_8),
    ),
    # 43
    Sketcher.Constraint('PointOnObject',
        obj_sketch_all_geoms.index(obj_sketch_circle_7), 3,
        obj_sketch_all_geoms.index(obj_sketch_line_8),
    ),
    # 44
    Sketcher.Constraint('DistanceY',
        -1, 1,
        obj_sketch_all_geoms.index(obj_sketch_circle_8), 3,
        10.0,
    ),
    # 45
    Sketcher.Constraint('DistanceY',
        obj_sketch_all_geoms.index(obj_sketch_circle_6), 3,
        obj_sketch_all_geoms.index(obj_sketch_line_8), 1,
        10.0,
    ),
    # 46
    Sketcher.Constraint('Symmetric',
        obj_sketch_all_geoms.index(obj_sketch_circle_6), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_8), 3,
        obj_sketch_all_geoms.index(obj_sketch_circle_7), 3,
    ),
    # 47
]
obj_sketch.addConstraint(obj_sketch_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-007-Sketch.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch')

obj_pad = body_left_z_rod_plate.newObject('PartDesign::Pad', 'Pad')
obj_pad.Label = 'Pad'
obj_pad.Profile = (obj_sketch, [])
obj_pad.Length = '6.0 mm'
obj_pad.Length2 = '100.0 mm'
obj_pad.Type = 'Length'
obj_pad.Reversed = False
obj_pad.Midplane = False
obj_pad.Offset = '0.0 mm'
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pad
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-008-Pad.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad')

obj_sketch001 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch001')
obj_sketch001.Support = (obj_pad, ['Face17'])
obj_sketch001.MapMode = 'FlatFace'
obj_sketch001_vector_1 = App.Vector(-10.000, 48.500, 0.000)
obj_sketch001_vector_2 = App.Vector(42.000, 48.500, 0.000)
obj_sketch001_vector_3 = App.Vector(42.000, 11.500, 0.000)
obj_sketch001_vector_4 = App.Vector(0.000, -42.000, 0.000)
obj_sketch001_vector_5 = App.Vector(-4.000, -42.000, 0.000)
obj_sketch001_vector_6 = App.Vector(-4.000, -16.000, 0.000)
obj_sketch001_vector_7 = App.Vector(-30.000, -16.000, 0.000)
obj_sketch001_vector_8 = App.Vector(-30.000, -12.000, 0.000)
obj_sketch001_vector_9 = App.Vector(-10.000, -0.000, 0.000)
obj_sketch001_vector_10 = App.Vector(-10.000, 0.000, 0.000)
obj_sketch001_vector_11 = App.Vector(-10.000, 4.000, 0.000)
obj_sketch001_vector_12 = App.Vector(-10.000, 44.500, 0.000)
obj_sketch001_vector_13 = App.Vector(36.000, 44.500, 0.000)
obj_sketch001_vector_14 = App.Vector(36.000, 13.574, 0.000)
obj_sketch001_vector_15 = App.Vector(28.484, 4.000, 0.000)
obj_sketch001_vector_16 = App.Vector(-7.628, -42.000, 0.000)
obj_sketch001_vector_17 = App.Vector(42.000, 21.217, 0.000)
obj_sketch001_line_1 = Part.LineSegment(obj_sketch001_vector_1, obj_sketch001_vector_2)
obj_sketch001_line_2 = Part.LineSegment(obj_sketch001_vector_2, obj_sketch001_vector_3)
obj_sketch001_line_3 = Part.LineSegment(obj_sketch001_vector_3, obj_sketch001_vector_4)
obj_sketch001_line_4 = Part.LineSegment(obj_sketch001_vector_4, obj_sketch001_vector_5)
obj_sketch001_line_5 = Part.LineSegment(obj_sketch001_vector_5, obj_sketch001_vector_6)
obj_sketch001_line_6 = Part.LineSegment(obj_sketch001_vector_6, obj_sketch001_vector_7)
obj_sketch001_line_7 = Part.LineSegment(obj_sketch001_vector_7, obj_sketch001_vector_8)
obj_sketch001_line_8 = Part.LineSegment(obj_sketch001_vector_8, obj_sketch001_vector_9)
obj_sketch001_line_9 = Part.LineSegment(obj_sketch001_vector_10, obj_sketch001_vector_11)
obj_sketch001_line_10 = Part.LineSegment(obj_sketch001_vector_12, obj_sketch001_vector_1)
obj_sketch001_line_11 = Part.LineSegment(obj_sketch001_vector_12, obj_sketch001_vector_13)
obj_sketch001_line_12 = Part.LineSegment(obj_sketch001_vector_13, obj_sketch001_vector_14)
obj_sketch001_line_13 = Part.LineSegment(obj_sketch001_vector_14, obj_sketch001_vector_15)
obj_sketch001_line_14 = Part.LineSegment(obj_sketch001_vector_15, obj_sketch001_vector_11)
obj_sketch001_circle_1 = Part.Circle(obj_sketch001_vector_3, App.Vector (0.0, 0.0, 1.0), 6.0)
obj_sketch001_circle_1.Construction = True
obj_sketch001_circle_2 = Part.Circle(obj_sketch001_vector_4, App.Vector (0.0, 0.0, 1.0), 6.0)
obj_sketch001_circle_2.Construction = True
obj_sketch001_line_15 = Part.LineSegment(obj_sketch001_vector_16, obj_sketch001_vector_17)
obj_sketch001_line_15.Construction = True
obj_sketch001_all_geoms = [obj_sketch001_line_1, obj_sketch001_line_2, obj_sketch001_line_3, obj_sketch001_line_4, obj_sketch001_line_5, obj_sketch001_line_6, obj_sketch001_line_7, obj_sketch001_line_8, obj_sketch001_line_9, obj_sketch001_line_10, obj_sketch001_line_11, obj_sketch001_line_12, obj_sketch001_line_13, obj_sketch001_line_14, obj_sketch001_circle_1, obj_sketch001_circle_2, obj_sketch001_line_15]
obj_sketch001.addGeometry(obj_sketch001_all_geoms, False)
obj_sketch001_all_ext_geoms = [[obj_pad, 'Edge21'], [obj_pad, 'Edge7'], [obj_pad, 'Edge16'], [obj_pad, 'Edge13']]
for a, b in obj_sketch001_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
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
        obj_sketch001_all_geoms.index(obj_sketch001_line_11), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_12), 1,
    ),
    # 9
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_12), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_13), 1,
    ),
    # 10
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_13), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_14), 1,
    ),
    # 11
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
    ),
    # 12
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_11), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 1,
    ),
    # 13
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_14), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
    ),
    # 14
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge13'])-3, 1,
    ),
    # 15
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge7'])-3, 2,
    ),
    # 16
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge13'])-3,
    ),
    # 17
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge16'])-3, 2,
    ),
    # 18
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge16'])-3,
    ),
    # 19
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_5),
    ),
    # 20
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_6),
    ),
    # 21
    Sketcher.Constraint('DistanceX',
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_4), 1,
        4.0,
    ),
    # 22
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_7), 2,
        4.0,
    ),
    # 23
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge21'])-3, 1,
    ),
    # 24
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_circle_1), 3,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
    ),
    # 25
    Sketcher.Constraint('Radius',
        obj_sketch001_all_geoms.index(obj_sketch001_circle_1), 6.0,
    ),
    # 26
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_circle_2), 3,
        obj_sketch001_all_geoms.index(obj_sketch001_line_3), 2,
    ),
    # 27
    Sketcher.Constraint('Radius',
        obj_sketch001_all_geoms.index(obj_sketch001_circle_2), 6.0,
    ),
    # 28
    Sketcher.Constraint('Tangent',
        obj_sketch001_all_geoms.index(obj_sketch001_line_15), 0,
        obj_sketch001_all_geoms.index(obj_sketch001_circle_2), 0,
    ),
    # 29
    Sketcher.Constraint('Tangent',
        obj_sketch001_all_geoms.index(obj_sketch001_circle_1), 0,
        obj_sketch001_all_geoms.index(obj_sketch001_line_15), 0,
    ),
    # 30
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_12), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_15),
    ),
    # 31
    Sketcher.Constraint('Vertical',
        obj_sketch001_all_geoms.index(obj_sketch001_line_12),
    ),
    # 32
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge21'])-3, 2,
    ),
    # 33
    Sketcher.Constraint('DistanceX',
        obj_sketch001_all_geoms.index(obj_sketch001_line_12), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2), 2,
        6.0,
    ),
    # 34
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_11),
    ),
    # 35
    Sketcher.Constraint('Coincident',
        obj_sketch001_all_geoms.index(obj_sketch001_line_1), 1,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge7'])-3, 1,
    ),
    # 36
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 1,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge7'])-3,
    ),
    # 37
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 1,
        obj_sketch001_all_geoms.index(obj_sketch001_line_10), 2,
        4.0,
    ),
    # 38
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge7'])-3,
    ),
    # 39
    Sketcher.Constraint('DistanceY',
        obj_sketch001_all_geoms.index(obj_sketch001_line_8), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_9), 2,
        4.0,
    ),
    # 40
    Sketcher.Constraint('Horizontal',
        obj_sketch001_all_geoms.index(obj_sketch001_line_14),
    ),
    # 41
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_13), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_15),
    ),
    # 42
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_15), 1,
        -obj_sketch001_all_ext_geoms.index([obj_pad, 'Edge16'])-3,
    ),
    # 43
    Sketcher.Constraint('PointOnObject',
        obj_sketch001_all_geoms.index(obj_sketch001_line_15), 2,
        obj_sketch001_all_geoms.index(obj_sketch001_line_2),
    ),
    # 44
]
obj_sketch001.addConstraint(obj_sketch001_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch001
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-009-Sketch001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch001')

obj_pad001 = body_left_z_rod_plate.newObject('PartDesign::Pad', 'Pad001')
obj_pad001.Label = 'Pad001'
obj_pad001.Profile = (obj_sketch001, [])
obj_pad001.Length = '10.0 mm'
obj_pad001.Length2 = '100.0 mm'
obj_pad001.Type = 'UpToFace'
obj_pad001.Reversed = False
obj_pad001.Midplane = False
obj_pad001.Offset = '0.0 mm'
obj_pad001.BaseFeature = obj_pad
obj_pad001.UpToFace = (obj_frameflmgn_bind, ['Face177'])
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pad001
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-010-Pad001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad001')

obj_sketch002 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch002')
obj_sketch002.Support = (obj_pad001, ['Face5'])
obj_sketch002.MapMode = 'FlatFace'
obj_sketch002_vector_1 = App.Vector(-36.000, 54.401, 0.000)
obj_sketch002_vector_2 = App.Vector(10.000, 16.000, 0.000)
obj_sketch002_vector_3 = App.Vector(10.000, 54.401, 0.000)
obj_sketch002_line_1 = Part.LineSegment(obj_sketch002_vector_1, obj_sketch002_vector_2)
obj_sketch002_line_2 = Part.LineSegment(obj_sketch002_vector_2, obj_sketch002_vector_3)
obj_sketch002_line_3 = Part.LineSegment(obj_sketch002_vector_3, obj_sketch002_vector_1)
obj_sketch002_all_geoms = [obj_sketch002_line_1, obj_sketch002_line_2, obj_sketch002_line_3]
obj_sketch002.addGeometry(obj_sketch002_all_geoms, False)
obj_sketch002_all_ext_geoms = [[obj_pad001, 'Edge26'], [obj_pad001, 'Edge27']]
for a, b in obj_sketch002_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
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
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        obj_sketch002_all_geoms.index(obj_sketch002_line_3), 2,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_2), 2,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge27'])-3, 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 2,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge27'])-3, 1,
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge26'])-3,
    ),
    # 6
    Sketcher.Constraint('DistanceX',
        -obj_sketch002_all_ext_geoms.index([obj_pad001, 'Edge26'])-3, 2,
        obj_sketch002_all_geoms.index(obj_sketch002_line_1), 1,
        6.0,
    ),
    # 7
]
obj_sketch002.addConstraint(obj_sketch002_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch002
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-011-Sketch002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch002')

obj_pocket = body_left_z_rod_plate.newObject('PartDesign::Pocket', 'Pocket')
obj_pocket.Label = 'Pocket'
obj_pocket.Profile = (obj_sketch002, [])
obj_pocket.Length = '0.0 mm'
obj_pocket.Length2 = '100.0 mm'
obj_pocket.Type = 'UpToFace'
obj_pocket.Reversed = False
obj_pocket.Midplane = False
obj_pocket.Offset = '0.0 mm'
obj_pocket.BaseFeature = obj_pad001
obj_pocket.UpToFace = (obj_pad001, ['Face25'])
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pocket
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-012-Pocket.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket')

obj_sketch003 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch003')
obj_sketch003.Support = (obj_pocket, ['Face30'])
obj_sketch003.MapMode = 'FlatFace'
obj_sketch003_vector_1 = App.Vector(-28.484, 54.401, 0.000)
obj_sketch003_vector_2 = App.Vector(30.000, 16.000, 0.000)
obj_sketch003_vector_3 = App.Vector(30.000, 54.401, 0.000)
obj_sketch003_line_1 = Part.LineSegment(obj_sketch003_vector_1, obj_sketch003_vector_2)
obj_sketch003_line_2 = Part.LineSegment(obj_sketch003_vector_2, obj_sketch003_vector_3)
obj_sketch003_line_3 = Part.LineSegment(obj_sketch003_vector_3, obj_sketch003_vector_1)
obj_sketch003_all_geoms = [obj_sketch003_line_1, obj_sketch003_line_2, obj_sketch003_line_3]
obj_sketch003.addGeometry(obj_sketch003_all_geoms, False)
obj_sketch003_all_ext_geoms = [[obj_pocket, 'Edge74'], [obj_pocket, 'Edge62']]
for a, b in obj_sketch003_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
    obj_sketch003.addExternal(a.Name, b)
obj_sketch003_constraints = [
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 1,
    ),
    # 1
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 1,
    ),
    # 2
    Sketcher.Constraint('Coincident',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge62'])-3, 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge62'])-3, 1,
        obj_sketch003_all_geoms.index(obj_sketch003_line_3), 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_2), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge74'])-3, 2,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        obj_sketch003_all_geoms.index(obj_sketch003_line_1), 2,
        -obj_sketch003_all_ext_geoms.index([obj_pocket, 'Edge74'])-3, 1,
    ),
    # 6
]
obj_sketch003.addConstraint(obj_sketch003_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch003
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-013-Sketch003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch003')

obj_pocket001 = body_left_z_rod_plate.newObject('PartDesign::Pocket', 'Pocket001')
obj_pocket001.Label = 'Pocket001'
obj_pocket001.Profile = (obj_sketch003, [])
obj_pocket001.Length = '0.0 mm'
obj_pocket001.Length2 = '100.0 mm'
obj_pocket001.Type = 'UpToFace'
obj_pocket001.Reversed = False
obj_pocket001.Midplane = False
obj_pocket001.Offset = '0.0 mm'
obj_pocket001.BaseFeature = obj_pocket
obj_pocket001.UpToFace = (obj_pocket, ['Face10'])
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pocket001
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-014-Pocket001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket001')

obj_sketch004 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch004')
obj_sketch004.Support = (obj_pocket001, ['Face7'])
obj_sketch004.MapMode = 'FlatFace'
obj_sketch004_vector_1 = App.Vector(-16.000, -42.000, 0.000)
obj_sketch004_vector_2 = App.Vector(-54.401, 4.000, 0.000)
obj_sketch004_vector_3 = App.Vector(-54.401, -42.000, 0.000)
obj_sketch004_line_1 = Part.LineSegment(obj_sketch004_vector_1, obj_sketch004_vector_2)
obj_sketch004_line_2 = Part.LineSegment(obj_sketch004_vector_2, obj_sketch004_vector_3)
obj_sketch004_line_3 = Part.LineSegment(obj_sketch004_vector_3, obj_sketch004_vector_1)
obj_sketch004_all_geoms = [obj_sketch004_line_1, obj_sketch004_line_2, obj_sketch004_line_3]
obj_sketch004.addGeometry(obj_sketch004_all_geoms, False)
obj_sketch004_all_ext_geoms = [[obj_pocket001, 'Face31'], [obj_pocket001, 'Face26'], [obj_pocket001, 'Face27'], [obj_pocket001, 'Face19']]
for a, b in obj_sketch004_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
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
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
    ),
    # 3
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Face26'])-3,
    ),
    # 4
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Face31'])-3,
    ),
    # 5
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 2,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Face19'])-3,
    ),
    # 6
    Sketcher.Constraint('PointOnObject',
        obj_sketch004_all_geoms.index(obj_sketch004_line_1), 1,
        -obj_sketch004_all_ext_geoms.index([obj_pocket001, 'Face27'])-3,
    ),
    # 7
    Sketcher.Constraint('Horizontal',
        obj_sketch004_all_geoms.index(obj_sketch004_line_3),
    ),
    # 8
    Sketcher.Constraint('Vertical',
        obj_sketch004_all_geoms.index(obj_sketch004_line_2),
    ),
    # 9
]
obj_sketch004.addConstraint(obj_sketch004_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch004
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-015-Sketch004.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch004')

obj_pocket002 = body_left_z_rod_plate.newObject('PartDesign::Pocket', 'Pocket002')
obj_pocket002.Label = 'Pocket002'
obj_pocket002.Profile = (obj_sketch004, [])
obj_pocket002.Length = '0.0 mm'
obj_pocket002.Length2 = '100.0 mm'
obj_pocket002.Type = 'UpToFace'
obj_pocket002.Reversed = False
obj_pocket002.Midplane = False
obj_pocket002.Offset = '0.0 mm'
obj_pocket002.BaseFeature = obj_pocket001
obj_pocket002.UpToFace = (obj_pocket001, ['Face9'])
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pocket002
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-016-Pocket002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket002')

obj_sketch005 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch005')
obj_sketch005.Support = (obj_pocket002, ['Face29'])
obj_sketch005.MapMode = 'FlatFace'
obj_sketch005_vector_1 = App.Vector(22.201, 40.000, 0.000)
obj_sketch005_vector_2 = App.Vector(42.201, 40.000, 0.000)
obj_sketch005_vector_3 = App.Vector(42.201, 20.000, 0.000)
obj_sketch005_vector_4 = App.Vector(22.201, 20.000, 0.000)
obj_sketch005_circle_1 = Part.Circle(obj_sketch005_vector_1, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_2 = Part.Circle(obj_sketch005_vector_2, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_3 = Part.Circle(obj_sketch005_vector_3, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_circle_4 = Part.Circle(obj_sketch005_vector_4, App.Vector (0.0, 0.0, 1.0), 1.6)
obj_sketch005_all_geoms = [obj_sketch005_circle_1, obj_sketch005_circle_2, obj_sketch005_circle_3, obj_sketch005_circle_4]
obj_sketch005.addGeometry(obj_sketch005_all_geoms, False)
obj_sketch005_all_ext_geoms = [[obj_frameflmgn_bind, 'Edge2'], [obj_frameflmgn_bind, 'Edge18'], [obj_frameflmgn_bind, 'Edge25'], [obj_frameflmgn_bind, 'Edge9'], [obj_frameflmgn_bind, 'Edge11'], [obj_frameflmgn_bind, 'Edge4'], [obj_frameflmgn_bind, 'Edge23'], [obj_frameflmgn_bind, 'Edge16']]
for a, b in obj_sketch005_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
    obj_sketch005.addExternal(a.Name, b)
obj_sketch005_constraints = [
    Sketcher.Constraint('Radius',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4), 1.6,
    ),
    # 1
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1),
    ),
    # 2
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2),
    ),
    # 3
    Sketcher.Constraint('Equal',
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4),
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3),
    ),
    # 4
    Sketcher.Constraint('Symmetric',
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge2'])-3, 1,
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge4'])-3, 1,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_1), 3,
    ),
    # 5
    Sketcher.Constraint('Symmetric',
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge11'])-3, 1,
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge9'])-3, 1,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_2), 3,
    ),
    # 6
    Sketcher.Constraint('Symmetric',
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge23'])-3, 1,
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge25'])-3, 1,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_3), 3,
    ),
    # 7
    Sketcher.Constraint('Symmetric',
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge16'])-3, 1,
        -obj_sketch005_all_ext_geoms.index([obj_frameflmgn_bind, 'Edge18'])-3, 1,
        obj_sketch005_all_geoms.index(obj_sketch005_circle_4), 3,
    ),
    # 8
]
obj_sketch005.addConstraint(obj_sketch005_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch005
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-017-Sketch005.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch005')

obj_pocket003 = body_left_z_rod_plate.newObject('PartDesign::Pocket', 'Pocket003')
obj_pocket003.Label = 'Pocket003'
obj_pocket003.Profile = (obj_sketch005, [])
obj_pocket003.Length = '6.0 mm'
obj_pocket003.Length2 = '100.0 mm'
obj_pocket003.Type = 'Length'
obj_pocket003.Reversed = False
obj_pocket003.Midplane = False
obj_pocket003.Offset = '0.0 mm'
obj_pocket003.BaseFeature = obj_pocket002
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pocket003
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-018-Pocket003.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pocket003')

body_left_z_rod_plate = App.ActiveDocument.getObject('left_z_rod_plate')
obj_pocket003 = App.ActiveDocument.getObject('Pocket003')
obj_fillet = body_left_z_rod_plate.newObject('PartDesign::Fillet', 'Fillet')
obj_fillet.Label = 'Fillet'
obj_fillet.Base = (obj_pocket003, ['Edge28', 'Edge38', 'Edge36'])
obj_fillet.Radius = '5.0 mm'
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_fillet
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003, obj_fillet]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-019-Fillet.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Fillet')

body_left_z_rod_plate = App.ActiveDocument.getObject('left_z_rod_plate')
obj_fillet = App.ActiveDocument.getObject('Fillet')
obj_fillet001 = body_left_z_rod_plate.newObject('PartDesign::Fillet', 'Fillet001')
obj_fillet001.Label = 'Fillet001'
obj_fillet001.Base = (obj_fillet, ['Edge66', 'Edge86', 'Edge87'])
obj_fillet001.Radius = '3.0 mm'
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_fillet001
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003, obj_fillet, obj_fillet001]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-020-Fillet001.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Fillet001')

obj_sketch006 = body_left_z_rod_plate.newObject('Sketcher::SketchObject', 'Sketch006')
obj_sketch006.Support = (obj_fillet001, ['Face36'])
obj_sketch006.MapMode = 'FlatFace'
obj_sketch006_vector_1 = App.Vector(16.000, 44.500, 0.000)
obj_sketch006_vector_2 = App.Vector(16.000, 4.000, 0.000)
obj_sketch006_vector_3 = App.Vector(29.132, 4.000, 0.000)
obj_sketch006_line_1 = Part.LineSegment(obj_sketch006_vector_1, obj_sketch006_vector_2)
obj_sketch006_line_2 = Part.LineSegment(obj_sketch006_vector_2, obj_sketch006_vector_3)
obj_sketch006_line_3 = Part.LineSegment(obj_sketch006_vector_3, obj_sketch006_vector_1)
obj_sketch006_all_geoms = [obj_sketch006_line_1, obj_sketch006_line_2, obj_sketch006_line_3]
obj_sketch006.addGeometry(obj_sketch006_all_geoms, False)
obj_sketch006_all_ext_geoms = [[obj_fillet001, 'Edge62'], [obj_fillet001, 'Edge101']]
for a, b in obj_sketch006_all_ext_geoms:
    print(f' Ext: {a.Name}, {b}')
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
        -obj_sketch006_all_ext_geoms.index([obj_fillet001, 'Edge62'])-3, 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 1,
    ),
    # 3
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_fillet001, 'Edge62'])-3, 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_3), 2,
    ),
    # 4
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_fillet001, 'Edge101'])-3, 1,
        obj_sketch006_all_geoms.index(obj_sketch006_line_1), 2,
    ),
    # 5
    Sketcher.Constraint('Coincident',
        -obj_sketch006_all_ext_geoms.index([obj_fillet001, 'Edge101'])-3, 2,
        obj_sketch006_all_geoms.index(obj_sketch006_line_2), 2,
    ),
    # 6
]
obj_sketch006.addConstraint(obj_sketch006_constraints)
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_sketch006
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003, obj_fillet, obj_fillet001, obj_sketch006]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-021-Sketch006.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Sketch006')

obj_pad002 = body_left_z_rod_plate.newObject('PartDesign::Pad', 'Pad002')
obj_pad002.Label = 'Pad002'
obj_pad002.Profile = (obj_sketch006, [])
obj_pad002.Length = '4.0 mm'
obj_pad002.Length2 = '100.0 mm'
obj_pad002.Type = 'Length'
obj_pad002.Reversed = True
obj_pad002.Midplane = False
obj_pad002.Offset = '0.0 mm'
obj_pad002.BaseFeature = obj_fillet001
if body_left_z_rod_plate_debug:
    body_left_z_rod_plate.Tip = obj_pad002
    body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003, obj_fillet, obj_fillet001, obj_sketch006, obj_pad002]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_z_rod_plate-022-Pad002.FCStd')
FreeCAD.ActiveDocument.recompute()
print('Pad002')

body_left_z_rod_plate.Group = [obj_panelfrontvslot_bind, obj_panelleftvslot_bind, obj_frameflrod_bind, obj_frameflnut_bind, obj_frameflmgn_bind, obj_frameflvslot_bind, obj_sketch, obj_pad, obj_sketch001, obj_pad001, obj_sketch002, obj_pocket, obj_sketch003, obj_pocket001, obj_sketch004, obj_pocket002, obj_sketch005, obj_pocket003, obj_fillet, obj_fillet001, obj_sketch006, obj_pad002]
body_left_z_rod_plate.Tip = obj_pad002
FreeCAD.ActiveDocument.recompute()
Part.export([body_left_z_rod_plate], 'left_z_rod_plate.brep')

App.ActiveDocument.saveAs("left_z_rod_plate.FCStd")
