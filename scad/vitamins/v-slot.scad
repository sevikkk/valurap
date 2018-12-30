//EXEMPLES use V_slot(shape,lenght);
//V_slot("20x20",10);
//V_slot("20x40",20);
//V_slot("20x60",30);
//V_slot("20x80",40);
//V_slot("40x40",20);
//V_slot("C-beam",10);
//////////////
$fn=60;
module vslot_center() {
    difference() {
        
        intersection() {
            translate([0,0,0.5]) cube([7.79,7.79,1],center=true);
            cylinder(d=13.5,h=3,center=true,$fn=4);
        }
            
        
        cylinder(d=4.2,h=3,center=true);
        for(i=[0:90:270]) rotate([0,0,i]) translate([7.2425,0,0]) rotate([0,0,45]) cube(5,center=true);
    }
}




module vslot_corner() {
    difference() {
        translate([5.5,5.5,0]) cube([3,3,1]);
        translate([5.5+1.07,5.5+1.07,-0.5]) cube([3,3,2]);
    }
    translate([3,3,0])rotate([0,0,45]) translate([0,-0.75,0]) cube([5.8,1.5,1]);
    difference() {
        hull() {for(i=[0,1],j=[0,1]) translate([i*8.5,j*8.5,0]) cylinder(d=3,h=1);}
        for(i=[0,90]) rotate([0,0,i]) translate([12.45,0,0]) rotate([0,0,45]) cube(10,center=true);
        cube(16.4,center=true);
    }
}

module vslot_raccord() {
    translate([-10,0,0]) {
        difference() {
            translate([0,8.2,0]) cube([20,1.8,1]);
            for(i=[0,20]) translate([i,12.45,0]) rotate([0,0,45]) cube(10,center=true);
        }
        translate([10,0,0]) for(i=[-1,1]) scale([i,1,1]) translate([5.39868/2,10-1.8-1.96,0]) cube([1.8,2,1]);
         for(i=[0,1]) translate([i*20,0,0]) rotate([0,0,i*90]) translate([3,3,0])rotate([0,0,45]) translate([0,-0.75,0]) cube([5.33205,1.5,1]);
    }
}

module vslot_inner_corner() {
    difference() {
        union() {
            translate([10,0,0]) vslot_raccord();
            translate([0,10,0]) rotate([0,0,-90]) vslot_raccord();
        }
        translate([0,0,-0.5]) cube([11,8.2,3]);
        translate([0,0,-0.5]) cube([8.2,11,3]);
    }
    translate([3,3,0])rotate([0,0,45]) translate([0,-0.75,0]) cube([9,1.5,1]);  
}


module v_slot(shape,lenght) {
scale([1,1,lenght]) {
    if (shape=="20x20") {
            vslot_center();
            for(i=[0:90:270]) rotate([0,0,i]) vslot_corner();
        }
        
    else if (shape=="20x40") {
            for(i=[-1,1]) translate([i*10,0,0]) vslot_center();
            for(i=[-1,1]) scale([1,i,1]) vslot_raccord();
            for(j=[-1,1]) scale([j,1,1]) translate([10,0,0]) for(i=[0,-90]) rotate([0,0,i]) vslot_corner();
        }
        
    else if (shape=="20x60") {
            for(i=[-1,0,1]) translate([i*20,0,0]) vslot_center();
            for(i=[-1,1]) scale([1,i,1]) for(i=[-1,1]) translate([i*10,0,0]) vslot_raccord();
            for(j=[-1,1]) scale([j,1,1]) translate([20,0,0]) for(i=[0,-90]) rotate([0,0,i]) vslot_corner();
        }
        
    else if (shape=="20x80") {
            for(i=[-3,-1,1,3]) translate([i*10,0,0]) vslot_center();
            for(i=[-1,1]) scale([1,i,1]) for(i=[-1,0,1]) translate([i*20,0,0]) vslot_raccord();
            for(j=[-1,1]) scale([j,1,1]) translate([30,0,0]) for(i=[0,-90]) rotate([0,0,i]) vslot_corner();
        }
        
    else if (shape=="40x40") {
            for(i=[0:90:270]) rotate([0,0,i]) {
                translate([10,10,0]) vslot_center();
                translate([0,10,0]) vslot_raccord();
                translate([10,10,0]) vslot_corner();
            }
        }
        
    else {

        for(i=[-3,-1,1,3]) translate([i*10,-10,0]) vslot_center();
        for(i=[-3,,3]) translate([i*10,10,0]) vslot_center();
            
        scale([1,-1,1]) for(i=[-1,0,1]) translate([i*20,10,0]) vslot_raccord();
        for(i=[-90,90]) rotate([0,0,i]) translate([0,30,0]) vslot_raccord();
        translate([0,-10,0]) vslot_raccord();
            
        for(j=[-1,1]) scale([j,1,1]) translate([30,-10,0]) rotate([0,0,-90]) vslot_corner();
        for(j=[-1,1]) scale([j,1,1]) translate([30,10,0]) for(i=[0,90]) rotate([0,0,i]) vslot_corner();
        
        for(j=[-1,1]) scale([j,1,1]) translate([-30,-10,0]) vslot_inner_corner();
    
    }
}

}


