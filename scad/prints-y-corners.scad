include <y-idler-corner.scad>
include <y-motor-corner.scad>

translate([0,0,25]) rotate([0,90,0]) y_motor_corner(true);
translate([50,0,25]) rotate([0,-90,0]) y_motor_corner(false);
translate([0,60,15]) rotate([0,-90,0]) y_idler_corner(true);
translate([50,60,15]) rotate([0,90,0]) y_idler_corner(false);

