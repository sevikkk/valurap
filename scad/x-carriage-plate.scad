module x_carriage_plate(belt_offset, wheel_x_offset, wheel_z_offset) {
    difference() {
        union() {
            translate([-45,-20, 11.5]) cube([90, 60, 10]);
	};
        translate([-20, wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
        translate([20, wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
        translate([0, -wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
	translate([-20, wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);
        translate([20, wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);
        translate([0, -wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);
	translate([-70,-3.5 + 10,belt_offset+12.2/2]) #cube([40,7,5]);
	translate([30,-3.5 + 10,belt_offset+12.2/2]) #cube([40,7,5]);
	translate([30,-20 + 10, 10]) #cube([40,40,6]);
	translate([-70,-20 + 10, 10]) #cube([40,40,6]);
        translate([37, 20, 12]) cylinder(d=5, h=10);
        translate([37, 0, 12]) cylinder(d=5, h=10);
        translate([-37, 20, 12]) cylinder(d=5, h=10);
        translate([-37, 0, 12]) cylinder(d=5, h=10);
        translate([37, 20, 20]) cylinder(d=9, h=10);
        translate([37, 0, 20]) cylinder(d=9, h=10);
        translate([-37, 20, 20]) cylinder(d=9, h=10);
        translate([-37, 0, 20]) cylinder(d=9, h=10);

    };
}
