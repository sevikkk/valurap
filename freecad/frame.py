import sys
import FreeCAD

App = FreeCAD

FreeCAD.open("vitamins/vitamins.FCStd")
App.setActiveDocument("vitamins")

Y = 400
if 0:
    X1 = 450 - 44
    X2 = 450 - 44
elif 0:
    X1 = 0
    X2 = 50
elif 0:
    X1 = 450 - 50 - 44
    X2 = 450 - 44
else:
    X1 = 180
    X2 = 280
Z = 100

X_plate_thickness = 5
titan_motor_plate_thickness = 5
front_titan_placement = App.Vector(30, -60, -30)
back_titan_placement = App.Vector(-30 + 44, 60, -30)

y_belt_offset_x = 17
y_belt_offset_y = 42 / 2 + 5
y_belt_offset_z = -12
y_belt_end_offset_y = 25
y_belt_length = 1000 + y_belt_offset_y + y_belt_end_offset_y
x_belt_length = 450 - 50

pulley_r = 6

vslot_20x40_500 = App.ActiveDocument.VSLOT20x40_500
vslot_20x40_1000 = App.ActiveDocument.VSLOT20x40_1000
mgn_12 = App.ActiveDocument.MGN12H
mgr_1000 = App.ActiveDocument.MGNR12R1000
mgr_450 = App.ActiveDocument.MGNR12R450
titan = App.ActiveDocument.TitanAero
nema17_47 = App.ActiveDocument.NEMA17_47
gt2_pulley = App.ActiveDocument.GT2Pulley_20
gt2_idler = App.ActiveDocument.GT2IdlerToothed_20
heated_plate = App.ActiveDocument.HeatedPlate
vslot_20x20_1000 = App.ActiveDocument.VSLOT20x20_1000
vslot_20x40_400 = App.ActiveDocument.VSLOT20x40_400
vslot_20x20_500 = App.ActiveDocument.VSLOT20x20_500
rod8_500 = App.ActiveDocument.Rod8
nut8 = App.ActiveDocument.Nut8
coupler5x8 = App.ActiveDocument.Coupler5x8
bb608zz = App.ActiveDocument.BB608ZZ


def remove(name):
    old = App.ActiveDocument.getObject(name)
    if old:
        if getattr(old, "removeObjectsFromDocument", None):
            old.removeObjectsFromDocument()
        App.ActiveDocument.removeObject(name)


def add(name, base, placement, *moves):
    print("adding", name)
    sys.stdout.flush()
    remove(name)

    new = App.ActiveDocument.addObject("PartDesign::Body", name)
    new_f = App.ActiveDocument.addObject("PartDesign::FeatureBase", name + "_body")
    new_f.BaseFeature = base
    p = placement
    for move in moves:
        p = move.multiply(p)
    new.Placement = p
    new.Group = [new_f]
    new.Tip = new_f
    print(new.supportedProperties())
    return new


remove("LeftTopBelt")
remove("RightTopBelt")
remove("LeftBottomBelt")
remove("RightBottomBelt")
remove("YBelt")

remove("FrontTopBelt")
remove("BackTopBelt")
remove("FrontBottomBelt")
remove("BackBottomBelt")
remove("XBelt")

y_belt = App.ActiveDocument.addObject("Part::Box", "YBelt")
y_belt.Length = "{} mm".format(y_belt_length)
y_belt.Width = "6 mm"
y_belt.Height = "2 mm"
if y_belt.ViewObject:
    y_belt.ViewObject.Visibility = False

x_belt = App.ActiveDocument.addObject("Part::Box", "XBelt")
x_belt.Length = "{} mm".format(x_belt_length)
x_belt.Width = "6 mm"
x_belt.Height = "2 mm"
if x_belt.ViewObject:
    x_belt.ViewObject.Visibility = False

if 0:
    heated_plate = App.ActiveDocument.addObject("Part::Box", "HeatedPlate_base")
    heated_plate.Length = "300 mm"
    heated_plate.Width = "300 mm"
    heated_plate.Height = "3 mm"
    if heated_plate.ViewObject:
        heated_plate.ViewObject.Visibility = False

    for x in [7, 300 - 7]:
        for y in [7, 300 - 7]:
            cyl = App.ActiveDocument.addObject("Part::Cylinder", "HeatedPlate_mount")
            cyl.Height = "5 mm"
            cyl.Radius = "2 mm"
            cyl.Placement = App.Placement(
                App.Vector(x, y, -1), App.Rotation(App.Vector(0, 0, 1), 0)
            )
            if cyl.ViewObject:
                cyl.ViewObject.Visibility = False
            cut = App.ActiveDocument.addObject("Part::Cut", "HeatedPlate_cut")
            cut.Base = heated_plate
            cut.Tool = cyl
            if cut.ViewObject:
                cut.ViewObject.Visibility = False
            heated_plate = cut

front_vslot = add(
    "FrontVSlot",
    vslot_20x40_500,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
)

left_vslot = add(
    "LeftVSlot",
    vslot_20x40_1000,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(App.Vector(-10, -10, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)


right_vslot = add(
    "RightVSlot",
    vslot_20x40_1000,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(App.Vector(510, -10, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

back_vslot = add(
    "BackVSlot",
    vslot_20x40_500,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(App.Vector(0, 980, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

left_rail = add(
    "LeftRail",
    mgr_1000,
    App.Placement(left_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 0, 30), App.Rotation(App.Vector(0, 0, 1), 0)),
)

right_rail = add(
    "RightRail",
    mgr_1000,
    App.Placement(right_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 0, 30), App.Rotation(App.Vector(0, 0, 1), 0)),
)

left_mgn = add(
    "LeftMGN",
    mgn_12,
    App.Placement(left_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, Y, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

right_mgn = add(
    "RightMGN",
    mgn_12,
    App.Placement(right_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, Y, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_vslot = add(
    "XVSlot",
    vslot_20x40_500,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90)),
    App.Placement(left_mgn.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(10, 10 + 22, 13 + 10 + X_plate_thickness),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)

x_front_rail = add(
    "XFrontRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90)),
    App.Placement(x_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(25, -30, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_back_rail = add(
    "XBackRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(x_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(25, 10, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_front_mgn = add(
    "XFrontMGN",
    mgn_12,
    x_front_rail.Placement,
    App.Placement(App.Vector(X1, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_back_mgn = add(
    "XBackMGN",
    mgn_12,
    x_back_rail.Placement,
    App.Placement(App.Vector(X2, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_front_titan = add(
    "XFrontTitan",
    titan,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(x_front_mgn.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(front_titan_placement, App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_front_motor = add(
    "XFrontMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(x_front_titan.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(-47 - titan_motor_plate_thickness, 6.66, 23),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)


x_back_titan = add(
    "XBackTitan",
    titan,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(x_back_mgn.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(back_titan_placement, App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_back_motor = add(
    "XBackMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 180)),
    App.Placement(x_back_titan.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(47 + titan_motor_plate_thickness, -6.66, 23),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)


left_top_belt = add(
    "LeftTopBelt",
    y_belt,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(left_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(
            -y_belt_offset_x, -y_belt_offset_y, 13 + X_plate_thickness + y_belt_offset_z
        ),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)

left_bottom_belt = add(
    "LeftBottomBelt",
    y_belt,
    left_top_belt.Placement,
    App.Placement(
        App.Vector(0, 0, -pulley_r * 2 - 2), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

right_top_belt = add(
    "RightTopBelt",
    y_belt,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(right_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(
            y_belt_offset_x + 6,
            -y_belt_offset_y,
            13 + X_plate_thickness + y_belt_offset_z,
        ),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)

right_bottom_belt = add(
    "RightBottomBelt",
    y_belt,
    right_top_belt.Placement,
    App.Placement(
        App.Vector(0, 0, -pulley_r * 2 - 2), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

left_pulley = add(
    "LeftPulley",
    gt2_pulley,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
    App.Placement(left_top_belt.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(3.75 + 3, 0, -pulley_r), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)


right_pulley = add(
    "RightPulley",
    gt2_pulley,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(right_top_belt.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(-(3.75 + 3 + 6), 0, -pulley_r), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)


left_motor = add(
    "LeftMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
    App.Placement(left_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(47 + 7, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)


right_motor = add(
    "RightMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(right_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(-47 - 7, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)


left_idler = add(
    "LeftIdler",
    gt2_idler,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
    App.Placement(left_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(-5.5, y_belt_length, 0), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)


right_idler = add(
    "RightIdler",
    gt2_idler,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(right_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(5.5, y_belt_length, 0), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

x_left_motor = add(
    "XLeftMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90)),
    App.Placement(x_front_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(-25 - 10 + 14 + 21 + 5, 47 + 5, -10 - 5 - 21),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)


x_right_motor = add(
    "XRightMotor",
    nema17_47,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(x_back_rail.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(450 - (-25 - 10 + 14 + 21 + 5), -(47 + 5), -10 - 5 - 21),
        App.Rotation(App.Vector(0, 0, 1), 0),
    ),
)

x_left_pulley = add(
    "XLeftPulley",
    gt2_pulley,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90)),
    App.Placement(x_left_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, -(47 + 7), 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)


x_right_pulley = add(
    "XRightPulley",
    gt2_pulley,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(x_right_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 47 + 7, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

x_left_idler = add(
    "XLeftIdler",
    gt2_idler,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(x_right_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(-x_belt_length, 5.5, 0), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)


x_right_idler = add(
    "XRightIdler",
    gt2_idler,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 90)),
    App.Placement(x_left_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(x_belt_length, -5.5, 0), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

front_top_belt = add(
    "FrontTopBelt",
    x_belt,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(x_left_pulley.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(
        App.Vector(0, -6.75 - 6, pulley_r), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)


back_top_belt = add(
    "BackTopBelt",
    x_belt,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(x_left_idler.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 1.5, pulley_r), App.Rotation(App.Vector(0, 0, 1), 0)),
)

front_bottom_belt = add(
    "FrontBottomBelt",
    x_belt,
    front_top_belt.Placement,
    App.Placement(
        App.Vector(0, 0, -pulley_r * 2 - 2), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

back_bottom_belt = add(
    "BackBottomBelt",
    x_belt,
    back_top_belt.Placement,
    App.Placement(
        App.Vector(0, 0, -pulley_r * 2 - 2), App.Rotation(App.Vector(0, 0, 1), 0)
    ),
)

panel_left_vslot = add(
    "PanelLeftVSlot",
    vslot_20x20_1000,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(left_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(50, 0, -Z - 20), App.Rotation(App.Vector(0, 0, 1), 0)),
)

panel_right_vslot = add(
    "PanelRightVSlot",
    vslot_20x20_1000,
    panel_left_vslot.Placement,
    App.Placement(App.Vector(400 + 20, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

panel_front_vslot = add(
    "PanelFrontVSlot",
    vslot_20x40_400,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(
        panel_left_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
    ),
    App.Placement(App.Vector(10, 10 + 40, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

panel_vslots = []
panels = []

for i in range(3):
    local_y = (300 + 6) * i
    if i == 2:
        last_adj = -20
    else:
        last_adj = 0
    panel_other_vslot = add(
        f"PanelVSlot{i}",
        vslot_20x40_400,
        panel_front_vslot.Placement,
        App.Placement(
            App.Vector(0, 300 - 14 + local_y + last_adj, 0),
            App.Rotation(App.Vector(0, 0, 1), 0),
        ),
    )
    panel_vslots.append(panel_other_vslot)
    panel = add(
        f"Panel{i}",
        heated_plate,
        App.Placement(
            panel_front_vslot.Placement.Base, App.Rotation(App.Vector(1, 0, 0), 0)
        ),
        App.Placement(
            App.Vector(50, local_y - 7, 10 + 10), App.Rotation(App.Vector(1, 0, 0), 0)
        ),
    )
    panels.append(panel)

frame_fl_vslot = add(
    "FrameFLVSlot",
    vslot_20x40_500,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(1, 0, 0), 180)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(left_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 30, -10), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_fr_vslot = add(
    "FrameFRVSlot",
    vslot_20x40_500,
    frame_fl_vslot.Placement,
    App.Placement(App.Vector(500 + 20, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_bl_vslot = add(
    "FrameBLVSlot",
    vslot_20x40_500,
    frame_fl_vslot.Placement,
    App.Placement(App.Vector(0, 1000 - 40, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_br_vslot = add(
    "FrameBRVSlot",
    vslot_20x40_500,
    frame_bl_vslot.Placement,
    App.Placement(App.Vector(500 + 20, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_front_vslot = add(
    "FrameFrontVSlot",
    vslot_20x20_500,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(front_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(0, 0, -490), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_back_vslot = add(
    "FrameBackVSlot",
    vslot_20x20_500,
    frame_front_vslot.Placement,
    App.Placement(App.Vector(0, 1000 - 20, 0), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_fl_rail = add(
    "FrameFLRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(frame_fl_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(10, 0, -20), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_bl_rail = add(
    "FrameBLRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), -90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 90)),
    App.Placement(frame_bl_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(10, 0, -20), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_fr_rail = add(
    "FrameFRRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
    App.Placement(frame_fr_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(-10, 0, -20), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_br_rail = add(
    "FrameBRRail",
    mgr_450,
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90)),
    App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
    App.Placement(frame_br_vslot.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)),
    App.Placement(App.Vector(-10, 0, -20), App.Rotation(App.Vector(0, 0, 1), 0)),
)

frame_fl_mgn = add(
    "FrameFLMGN",
    mgn_12,
    frame_fl_rail.Placement,
    App.Placement(App.Vector(0, 0, -Z), App.Rotation(App.Vector(0, 0, 1), 0)),
)
frame_fr_mgn = add(
    "FrameFRMGN",
    mgn_12,
    frame_fr_rail.Placement,
    App.Placement(App.Vector(0, 0, -Z), App.Rotation(App.Vector(0, 0, 1), 0)),
)
frame_bl_mgn = add(
    "FrameBLMGN",
    mgn_12,
    frame_bl_rail.Placement,
    App.Placement(App.Vector(0, 0, -Z), App.Rotation(App.Vector(0, 0, 1), 0)),
)
frame_br_mgn = add(
    "FrameBRMGN",
    mgn_12,
    frame_br_rail.Placement,
    App.Placement(App.Vector(0, 0, -Z), App.Rotation(App.Vector(0, 0, 1), 0)),
)

for i in range(4):
    if i == 0:
        p = "FL"
        base = front_vslot.Placement.Base
        k1 = 1
        k2 = 1
        k3 = 0
    elif i == 1:
        p = "FR"
        base = front_vslot.Placement.Base
        k1 = -1
        k2 = 1
        k3 = 500
    if i == 2:
        p = "BL"
        base = back_vslot.Placement.Base
        k1 = 1
        k2 = -1
        k3 = 0
    if i == 3:
        p = "BR"
        base = back_vslot.Placement.Base
        k1 = -1
        k2 = -1
        k3 = 500

    frame_fl_motor = add(
        f"Frame{p}Motor",
        nema17_47,
        App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 180)),
        App.Placement(base, App.Rotation(App.Vector(0, 0, 1), 0)),
        App.Placement(
            App.Vector(65 * k1 + k3, -(21 + 5 + 10) * k2, 47 + 35),
            App.Rotation(App.Vector(0, 0, 1), 0),
        ),
    )

    frame_fl_rod = add(
        f"Frame{p}Rod",
        rod8_500,
        App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), 180)),
        App.Placement(
            frame_fl_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
        ),
        App.Placement(
            App.Vector(0, 0, -(47 + 25)), App.Rotation(App.Vector(0, 0, 1), 0)
        ),
    )

    frame_fl_coupler = add(
        f"Frame{p}Coupler",
        coupler5x8,
        App.Placement(
            frame_fl_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
        ),
        App.Placement(
            App.Vector(0, 0, -(47 + 25 + 12)), App.Rotation(App.Vector(0, 0, 1), 0)
        ),
    )

    frame_fl_nut = add(
        f"Frame{p}Nut",
        nut8,
        App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 1, 0), -90)),
        App.Placement(
            frame_fl_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
        ),
        App.Placement(
            App.Vector(0, 0, -(47 + 80 + Z)), App.Rotation(App.Vector(0, 0, 1), 0)
        ),
    )

    frame_fl_topbb = add(
        f"Frame{p}TopBB",
        bb608zz,
        App.Placement(
            frame_fl_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
        ),
        App.Placement(
            App.Vector(0, 0, -(47 + 25 + 15)), App.Rotation(App.Vector(0, 0, 1), 0)
        ),
    )

    frame_fl_bottombb = add(
        f"Frame{p}BottomBB",
        bb608zz,
        App.Placement(
            frame_fl_motor.Placement.Base, App.Rotation(App.Vector(0, 0, 1), 0)
        ),
        App.Placement(App.Vector(0, 0, -565), App.Rotation(App.Vector(0, 0, 1), 0)),
    )

App.ActiveDocument.recompute()
# Gui.SendMsgToActiveView("ViewFit")
App.ActiveDocument.saveAs("frame.FCStd")
print()
print()
print()
