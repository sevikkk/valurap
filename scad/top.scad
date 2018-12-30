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
Y_motors_offset = 4; // Adjust to put lower belt inside of extrusion cavity

X_belt = GT2x6;
X_pulley = GT2x20_metal_pulley;
X_idler = GT2x20_metal_idler;
X_wheel = wheel_23mm;
X_motors_offset = 4; // Adjust to put lower belt inside of extrusion cavity


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


module x_carriage(belt_offset) {
 wheel_z_offset = wheel_v_slot_offset(X_wheel);
 wheel_y_offset = wheel_bearing_heoght(X_wheel)/2;
    
 translate([-20, 0, wheel_z_offset-10]) rotate([90,0,0]) nylon_wheel(X_wheel);
 translate([20, 0, wheel_z_offset-10]) rotate([90,0,0]) nylon_wheel(X_wheel);
 translate([0, 0, -wheel_z_offset-10]) rotate([90,0,0]) nylon_wheel(X_wheel);

}

module x_motor(X_size, X) {
 translate([-12, 0, 17]) rotate([180, 0, 0]) {
     NEMA(NEMA17);
     translate([0, 0, 5]) metal_pulley(X_pulley);
     translate([-pulley_od(X_pulley)/2, 0, 17])
        belt_loop(loop_dia=pulley_od(X_pulley), loop_straight=X_size/2 + X, belt_end=40, belt=X_belt);
 };
}


module x_idler(X_size, X) {
 translate([ -12, 0, 17]) rotate([180, 0, 0]) {
        translate([0, 0, 5]) metal_pulley(X_idler);
        translate([-pulley_od(X_pulley)/2, 0, 17])  rotate([180,0,0]) belt_loop(
            loop_straight=X_size/2 - X, belt_end=40,
            loop_dia=pulley_od(X_pulley), belt=X_belt);
 };
}

module x_end(X_size, X, X_other, vslot_offset, is_left=true) {
 wheel_x_offset = wheel_v_slot_offset(Y_wheel);
 wheel_z_offset = wheel_bearing_heoght(Y_wheel)/2;
    
 translate([-wheel_x_offset-10, -20, 0]) nylon_wheel(Y_wheel);
 translate([-wheel_x_offset-10, 20, 0]) nylon_wheel(Y_wheel);
 translate([wheel_x_offset-10, 0, 0]) nylon_wheel(Y_wheel);
 
 translate([0, 20 + X_motors_offset, vslot_offset]) x_motor(X_size, X);
 translate([0, -20 - X_motors_offset, vslot_offset]) x_idler(X_size, X_other);

}

module x_assembly(X_size, X1, X2, belt_offset) {
 vslot_offset = 30;
 translate([X_size/2, 0, vslot_offset]) rotate([-90, 0, 90]) v_slot("20x40", X_size);
 translate([-X_size/2, 0, 0]) x_end(X_size, X1, -X2, vslot_offset, true);
 translate([X_size/2, 0, 0]) rotate([0, 0, 180]) x_end(X_size, -X2, X1, vslot_offset, false);
 translate([X1, 10, vslot_offset+10]) x_carriage(X_motors_offset+10);
 translate([X2, -10, vslot_offset+10]) rotate([0, 0, 180]) x_carriage(X_motors_offset+10);
    
}


module y_motor(Y_size, Y, is_left=true) {
 k = is_left? 1 : -1;
 a = is_left? 0 : 180;
 translate([5 * k, -25, 0]) rotate([-90, 0, 90 * k]) {
        NEMA(NEMA17);
        translate([0, 0, 5]) metal_pulley(Y_pulley);
        translate([-pulley_od(Y_pulley)/2 * k, 0, 17]) rotate([a,0,a]) belt_loop(loop_straight=Y_size/2 + Y, belt_end=40, loop_dia=pulley_od(Y_pulley), belt=Y_belt);
 };
}


module y_idler(Y_size, Y, is_left=true) {
 k = is_left? 1 : -1;
 a = is_left? 180 : 0;
 translate([ 5* k, 15, 0]) rotate([-90, 0, 90 * k]) {
        translate([0, 0, 5]) metal_pulley(Y_idler);
        translate([pulley_od(Y_pulley)/2 * k, 0, 17]) rotate([a,0,a]) belt_loop(loop_straight=Y_size/2 - Y - 10, belt_end=40, loop_dia=pulley_od(Y_pulley), belt=Y_belt);
 };
}


module top(X_size, Y_size, X1, X2, Y) {
 frame(X_size, Y_size);
 translate([-X_size/2, -Y_size/2, Y_motors_offset + 40]) y_motor(Y_size, Y, true);
 translate([X_size/2, -Y_size/2, Y_motors_offset + 40]) y_motor(Y_size, Y, false);
 translate([-X_size/2, Y_size/2, Y_motors_offset + 40]) y_idler(Y_size, Y, true);
 translate([X_size/2, Y_size/2, Y_motors_offset + 40]) y_idler(Y_size, Y, false);
 translate([0, Y, 30]) x_assembly(X_size, X1, X2, Y_motors_offset + 10);
}


top(X_size=250, Y_size=300, X1=20, X2=-20, Y=-20);
