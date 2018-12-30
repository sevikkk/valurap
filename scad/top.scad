// $fn=60;
module vitamin(name) {};

use_realistic_colors = true;
printed_plastic_color = "orange";
bulldog_real_color = "black";
belt_real_color = "green";
cable_strip_real_color = "grey";

include <vitamins/colors.scad>
include <vitamins/vitamins.scad>

Y_belt = GT2x6;
Y_pulley = GT2x20_metal_pulley;
Y_idler = GT2x20_metal_idler;
Y_wheel = wheel_23mm;

module belt_loop(loop_dia=12.2, loop_straight=200, belt_end=40, belt=Y_belt) {
    height = loop_dia + 2 * belt_thickness(belt);
    length = loop_straight + belt_end;

    color(belt_color)
    translate([loop_dia / 2, 0, 0])
        linear_extrude(height = belt_width(belt), convexity = 5, center = true)
            difference() {
                union() {
                    circle(r = height / 2, center = true);
                    translate([0, -height / 2])
                        square([length, height]);
                }
                union() {
                    circle(r = loop_dia / 2, center = true);
                    translate([0, -loop_dia / 2])
                        square([length, loop_dia]);
                }
                translate([loop_straight, -height])
                    square([100, height]);
            }
}


module frame(X_size, Y_size) {
 translate([-X_size/2,  Y_size/2 - 10, 20])
    rotate([0, 90, 0]) v_slot("20x40", X_size);
 translate([-X_size/2, -Y_size/2 + 10, 20])
    rotate([0, 90, 0]) v_slot("20x40", X_size);
 translate([ X_size/2 + 10, -Y_size/2, 20])
    rotate([-90, 90, 0]) v_slot("20x40", Y_size);
 translate([-X_size/2 - 10, -Y_size/2, 20])
    rotate([-90, 90, 0]) v_slot("20x40", Y_size);
}


module x_end(X, X_other, is_left=true) {
 wheel_offset = wheel_v_slot_offset(Y_wheel);
    
 translate([-wheel_offset-10, -20, 0]) nylon_wheel(Y_wheel);
 translate([-wheel_offset-10, 20, 0]) nylon_wheel(Y_wheel);
 translate([wheel_offset-10, 0, 0]) nylon_wheel(Y_wheel);

}


module x_assembly(X_size, X1, X2) {
 translate([X_size/2, 0, 30]) rotate([-90, 0, 90]) v_slot("20x40", X_size);
 translate([-X_size/2, 0, 0]) x_end(X1, X2, true);
 translate([X_size/2, 0, 0]) rotate([0, 0, 180]) x_end(X2, X1, false);
}


module y_motor(Y_size, Y, is_left=true) {
 k = is_left? 1 : -1;
 a = is_left? 0 : 180;
 translate([5 * k, -25, 0]) rotate([-90, 0, 90 * k]) {
        NEMA(NEMA17);
        translate([0, 0, 5]) metal_pulley(Y_pulley);
        translate([-12.2/2 * k, 0, 17]) rotate([a,0,a]) belt_loop(loop_straight=Y_size/2 + Y, belt_end=40);
 };
}


module y_idler(Y_size, Y, is_left=true) {
 k = is_left? 1 : -1;
 a = is_left? 180 : 0;
 translate([ 5* k, 15, 0]) rotate([-90, 0, 90 * k]) {
        translate([0, 0, 5]) metal_pulley(Y_idler);
        translate([12.2/2 * k, 0, 17]) rotate([a,0,a]) belt_loop(loop_straight=Y_size/2 - Y - 10, belt_end=40);
 };
}


module top(X_size, Y_size, X1, X2, Y) {
 frame(X_size, Y_size);
 translate([-X_size/2, -Y_size/2, 44]) y_motor(Y_size, Y, true);
 translate([X_size/2, -Y_size/2, 44]) y_motor(Y_size, Y, false);
 translate([-X_size/2, Y_size/2, 44]) y_idler(Y_size, Y, true);
 translate([X_size/2, Y_size/2, 44]) y_idler(Y_size, Y, false);
 translate([0, Y, 30]) x_assembly(X_size, X1, X2, 14);
}


top(X_size=250, Y_size=300, X1=0, X2=0, Y=-20);
