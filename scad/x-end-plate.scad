module x_end_plate(vslot_offset, belt_offset, wheel_x_offset, wheel_z_offset) {
    difference() {
        union() {
            translate([-45,-50, 12.5]) cube([85, 100, 6]);
            translate([-6,-50,12.5]) cube([46, 15, 22.5]);
            translate([-45,-50,12.5]) cube([31, 15, 22.5]);
            translate([-20,-50, belt_offset + 12.2/2 + 1.5]) cube([15, 13, 5]);
            translate([-20,-50, 29]) cube([15, 15, 6]);

            translate([-6,  35,12.5]) cube([46, 15, 22.5]);
            translate([-45, 35,12.5]) cube([31, 15, 22.5]);
            translate([-20, 37, belt_offset + 12.2/2 + 1.5]) cube([15, 13, 5]);
            translate([-20, 35, 29]) cube([15, 15, 6]);

            translate([-45,-50,12.5]) cube([20, 100, 22.5]);
	};
        translate([wheel_x_offset-10, -40, -10]) #cylinder(d=6, h=51.5);
        translate([wheel_x_offset-10, 40, -10]) #cylinder(d=6, h=51.5);
        translate([-wheel_x_offset-10, 0, -10]) #cylinder(d=6, h=51.5);
	translate([-3,-20,15]) #cube([100,40,20]);
        translate([30, -10, 0]) cylinder(d=5, h=20);
        translate([10, -10, 0]) cylinder(d=5, h=20);
        translate([30, 10, 0]) cylinder(d=5, h=20);
        translate([10, 10, 0]) cylinder(d=5, h=20);
        translate([-10, -24, 0]) cylinder(d=3, h=100);
        translate([-10, -24, 0]) cylinder(d=6, h=15);
    };
}

module x_end_top(vslot_offset, belt_offset, wheel_x_offset, wheel_z_offset) {
    echo("x_end offsets",vslot_offset, belt_offset, wheel_x_offset, wheel_z_offset);
    difference() {
        union() {
            translate([-45,-50, 35]) cube([85, 100, 7]);
	}
        translate([wheel_x_offset-10, -40, -10]) #cylinder(d=6, h=51.5);
        translate([wheel_x_offset-10, 40, -10]) #cylinder(d=6, h=51.5);
        translate([-wheel_x_offset-10, 0, -10]) #cylinder(d=6, h=51.5);
        translate([wheel_x_offset-10, -40, 38]) rotate([0,0,30]) cylinder(d=12, h=10, $fn=6);
        translate([wheel_x_offset-10, 40,  38]) rotate([0,0,30]) cylinder(d=12, h=10, $fn=6);
        translate([-wheel_x_offset-10, 0,  38]) cylinder(d=12, h=10, $fn=6);
        translate([37, -10, 30]) cylinder(d=5, h=20);
        translate([17, -10, 30]) cylinder(d=5, h=20);
        translate([37, 10, 30]) cylinder(d=5, h=20);
        translate([17, 10, 30]) cylinder(d=5, h=20);
        translate([-10, -24, 0]) cylinder(d=3, h=100);
        translate([-10, 24, 0]) cylinder(d=25, h=100);
        translate([-10-15.5, 24-15.5, 0]) cylinder(d=3, h=100);
        translate([-10-15.5, 24+15.5, 0]) cylinder(d=3, h=100);
        translate([-10+15.5, 24-15.5, 0]) cylinder(d=3, h=100);
        translate([-10+15.5, 24+15.5, 0]) cylinder(d=3, h=100);
        translate([-10-15.5, 24-15.5, 0]) cylinder(d=6, h=39);
        translate([-10-15.5, 24+15.5, 0]) cylinder(d=6, h=39);
        translate([-10+15.5, 24-15.5, 0]) cylinder(d=6, h=39);
        translate([-10+15.5, 24+15.5, 0]) cylinder(d=6, h=39);
    };
}
