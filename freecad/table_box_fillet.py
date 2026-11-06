import FreeCAD as App
import FreeCADGui as Gui


DOC_BASENAME = "TableBoxFillet"
SAVE_PATH = "/Users/seva/src/sevasoft/valurap/freecad/table_box_fillet.FCStd"


def set_param(sheet, row, label, alias, value):
    sheet.set(f"A{row}", label)
    sheet.set(f"B{row}", value)
    sheet.setAlias(f"B{row}", alias)


doc_name = DOC_BASENAME
counter = 1
while doc_name in App.listDocuments():
    doc_name = f"{DOC_BASENAME}_{counter}"
    counter += 1

doc = App.newDocument(doc_name)
Gui.ActiveDocument = Gui.getDocument(doc.Name)

params = doc.addObject("Spreadsheet::Sheet", "Params")
params.Label = "Dimensions"
params.set("A1", "Parameter")
params.set("B1", "Value")
set_param(params, 2, "Length", "box_length", "60 mm")
set_param(params, 3, "Width", "box_width", "40 mm")
set_param(params, 4, "Height", "box_height", "25 mm")
set_param(params, 5, "Fillet Radius", "fillet_radius", "4 mm")

body = doc.addObject("PartDesign::Body", "Body")
box = doc.addObject("PartDesign::AdditiveBox", "Box")
body.addObject(box)
box.setExpression("Length", "Params.box_length")
box.setExpression("Width", "Params.box_width")
box.setExpression("Height", "Params.box_height")

doc.recompute()

fillet = doc.addObject("PartDesign::Fillet", "Fillet")
body.addObject(fillet)
fillet.Base = (box, [""])
fillet.UseAllEdges = True
fillet.setExpression("Radius", "Params.fillet_radius")

doc.recompute()
doc.saveAs(SAVE_PATH)

view = Gui.activeDocument().activeView()
view.viewAxometric()
view.fitAll()
