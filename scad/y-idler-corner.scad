module y_idler_corner(is_left) {
    k = is_left?1:0;
    mirror([k,0,0])
    difference() {
        union() {
            translate([10,  8,-16])  cube([5,32,42]);
            translate([10,-10,-16]) cube([5,48,25]);
            translate([10,-10,25])  cube([5,50,10]);
            translate([-5,-10,25])  cube([20,50,5]);
            translate([-5,-10,4])  cube([20,50,5]);

        };
        translate([9, 34, 17]) rotate([0,90,0]) cylinder(r=3, h=12);
        translate([9, 14, 17]) rotate([0,90,0]) cylinder(r=3, h=12);
        translate([9, 34, -5]) rotate([0,90,0]) cylinder(r=3, h=12);
        translate([9, 14, -5]) rotate([0,90,0]) cylinder(r=3, h=12);
        translate([-5]) cylinder(d=4, h=40);
    }
}
