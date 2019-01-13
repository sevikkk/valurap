wheel_23mm   = ["Nylon Wheel 23 mm", 7.8, 7.4, 14, 5, 7, 5, 17.5];
wheel_34mm   = ["Nylon Wheel 34.5 mm", 12.25, 12, 19, 6, 11, 6, 25];

function wheel_type(type) = type[0];
function wheel_circle_offset(type) = type[1];
function wheel_circle_diameter(type) = type[2];
function wheel_bearing_od(type) = type[3];
function wheel_bearing_height(type) = type[4];
function wheel_width(type) = type[5];
function wheel_bearing_id(type) = type[6];
function wheel_v_slot_offset(type) = type[7];

module nylon_wheel(type)
{
    color("LightGrey",.9)
    difference()
    {
        union()
        {
            rotate_extrude(convexity = 10, $fn = 64)
            translate([wheel_circle_offset(type), 0, 0])
            circle(d = wheel_circle_diameter(type), $fn = 64);
            cylinder(d=wheel_bearing_od(type), h=wheel_bearing_height(type), center=true);
        }
        translate([0,0,wheel_width(type)/2])
        cylinder(d=50,h=10);
        translate([0,0,-10 - wheel_width(type)/2])
        cylinder(d=50,h=10);
        cylinder(d=wheel_bearing_id(type),h=10,center=true,$fn=24);
    }
}
