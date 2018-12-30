module y_motor_corner(is_left) {
    k = is_left?1:0;
    mirror([k,0,0])
    difference() {
        union() {
            difference() {
                union() {
                    translate([-25,-25,0]) cube([50,50,5]);
                    translate([22,-25,-45]) cube([3,50,50]);
                    translate([-25,-25,-45]) cube([50,3,50]);
                    translate([-25,22,-45]) cube([50,3,50]);
                    translate([-25,-25,-65]) cube([3,65,70]);
                };
                translate([-50,-30,-130]) rotate([0,0,0]) cube([100,100,100]);
                translate([0,0, -50]) rotate([0,0,0]) cylinder(d=25, h=100);
            };
            translate([-25,8,-66]) cube([3,32,89]);

        };
        translate([-30,14,-55]) rotate([0,90,0]) cylinder(r=3, h=10);
        translate([-30,34,-55]) rotate([0,90,0]) cylinder(r=3, h=10);
        translate([-30,34,-20]) rotate([0,90,0]) cylinder(r=3, h=10);
        translate([-30,34, 15]) rotate([0,90,0]) cylinder(r=3, h=10);
        translate([-30, 14, 15]) rotate([0,90,0]) cylinder(r=3, h=10);
        translate([15.5, 15.5, -5]) rotate([0,0,0]) cylinder(d=3, h=12);
        translate([15.5, -15.5, -5]) rotate([0,0,0]) cylinder(d=3, h=12);
        translate([-15.5, 15.5, -5]) rotate([0,0,0]) cylinder(d=3, h=12);
        translate([-15.5, -15.5, -5]) rotate([0,0,0]) cylinder(d=3, h=12);

    }
}
