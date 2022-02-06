import FreeCAD
import time

import sys

def pp(msg):
  sys.stderr.write(str(msg)+"\n")

if 0:
    import FreeCADGui
    from PySide2.QtWidgets import QApplication
    qt_app = QApplication(["bubu"])
    FreeCADGui.showMainWindow()

new_part = "left_x_opto_mount"

FreeCAD.open("frame.FCStd")
FreeCAD.newDocument(new_part)
FreeCAD.setActiveDocument(new_part)

FreeCAD.ActiveDocument.saveAs(f"{new_part}.FCStd")

body = FreeCAD.activeDocument().addObject('PartDesign::Body', new_part)
for o in [
    "XVSlot",
    "XFrontRail",
    "XFrontCarriage",
    "XFrontTitanMount",
    "XFrontMGN"
]:
    print(o)
    sb = body.newObject('PartDesign::SubShapeBinder', o + '_bind')
    ob = App.getDocument('frame').getObject(o)
    sb.Support = [(ob, ('',))]

FreeCAD.ActiveDocument.recompute()
#FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCAD.ActiveDocument.save()
