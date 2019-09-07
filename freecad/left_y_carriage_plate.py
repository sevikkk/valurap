
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

obj_xvslot_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XVSlot_bind')
obj_xvslot_bind_orig = App.getDocument('frame').getObject('XVSlot')
obj_xvslot_bind.TraceSupport = False
obj_xvslot_bind.Support = [(obj_xvslot_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xvslot_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xvslot_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-007-XVSlot_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XVSlot_bind')

obj_xfrontrail_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XFrontRail_bind')
obj_xfrontrail_bind_orig = App.getDocument('frame').getObject('XFrontRail')
obj_xfrontrail_bind.TraceSupport = False
obj_xfrontrail_bind.Support = [(obj_xfrontrail_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xfrontrail_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xvslot_bind, obj_xfrontrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-008-XFrontRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XFrontRail_bind')

obj_xbackrail_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XBackRail_bind')
obj_xbackrail_bind_orig = App.getDocument('frame').getObject('XBackRail')
obj_xbackrail_bind.TraceSupport = False
obj_xbackrail_bind.Support = [(obj_xbackrail_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xbackrail_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-009-XBackRail_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XBackRail_bind')

obj_xleftpulley_bind = body_left_y_carriage_plate.newObject('PartDesign::ShapeBinder', 'XLeftPulley_bind')
obj_xleftpulley_bind_orig = App.getDocument('frame').getObject('XLeftPulley')
obj_xleftpulley_bind.TraceSupport = False
obj_xleftpulley_bind.Support = [(obj_xleftpulley_bind_orig, '')]
if body_left_y_carriage_plate_debug:
    body_left_y_carriage_plate.Tip = obj_xleftpulley_bind
    body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind]
    FreeCAD.ActiveDocument.recompute()
    App.ActiveDocument.saveAs('debug/plate-left_y_carriage_plate-010-XLeftPulley_bind.FCStd')
FreeCAD.ActiveDocument.recompute()
print('XLeftPulley_bind')

body_left_y_carriage_plate.Group = [obj_leftvslot_bind, obj_leftrail_bind, obj_leftmgn_bind, obj_lefttopbelt_bind, obj_leftbottombelt_bind, obj_xleftmotor_bind, obj_xvslot_bind, obj_xfrontrail_bind, obj_xbackrail_bind, obj_xleftpulley_bind]
FreeCAD.ActiveDocument.recompute()

App.ActiveDocument.saveAs("plate.FCStd")
