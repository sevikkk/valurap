module x_carriage_plate(belt_offset, wheel_x_offset, wheel_z_offset) {
    echo("x_carriage_plate", belt_offset, wheel_x_offset, wheel_z_offset);
    difference() {
        union() {
            translate([-45,-25, 11.5]) cube([90, 70, 10]);
	};
        translate([-20, wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
        translate([20, wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
        translate([0, -wheel_x_offset+10, -6.5]) #cylinder(d=6, h=23.5);
	translate([-20, wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);
        translate([20, wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);
        translate([0, -wheel_x_offset+10, 11.5+3]) rotate([0,0,30]) #cylinder(d=9, h=14, $fn=6);

	translate([-73,-3.5 + 10,belt_offset+12.2/2]) #cube([40,7,5]);
	translate([33,-3.5 + 10,belt_offset+12.2/2]) #cube([40,7,5]);
	translate([33,-20 + 10, 10]) #cube([40,40,6]);
	translate([-73,-20 + 10, 10]) #cube([40,40,6]);

	translate([-37,-3.5 + 10, 0]) #cube([4,7,35]);
	translate([33,-3.5 + 10, 0]) #cube([4,7,35]);

        translate([39, 20, 12]) cylinder(d=5, h=10);
        translate([39, 0, 12]) cylinder(d=5, h=10);
        translate([-39, 20, 12]) cylinder(d=5, h=10);
        translate([-39, 0, 12]) cylinder(d=5, h=10);

        translate([39, 20, 20]) cylinder(d=9, h=10);
        translate([39, 0, 20]) cylinder(d=9, h=10);
        translate([-39, 20, 20]) cylinder(d=9, h=10);
        translate([-39, 0, 20]) cylinder(d=9, h=10);

	a = 15;
	b = 27;
        translate([-a, 10-b, 10]) #cylinder(d=4, h=100);
        translate([-a, b+10, 10]) #cylinder(d=4, h=100);
        translate([a, 10-b, 10]) #cylinder(d=4, h=100);
        translate([a, b+10, 10]) #cylinder(d=4, h=100);

        translate([-a, 10-b, 10]) rotate([0,0,30]) #cylinder(d=8, h=5, $fn=6);
        translate([-a, b+10, 10]) rotate([0,0,30]) #cylinder(d=8, h=5, $fn=6);
        translate([a, 10-b, 10]) rotate([0,0,30]) #cylinder(d=8, h=5, $fn=6);
        translate([a, b+10, 10]) rotate([0,0,30]) #cylinder(d=8, h=5, $fn=6);

        translate([34, -12, 11.5+10-4]) #cylinder(d=16, h=50);
        translate([24, -35, 10]) #cube([40,20,40]);

    };
}
