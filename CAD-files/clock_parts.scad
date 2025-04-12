outer_dia = 296;

module glas_holder(){
    difference() {
        difference() {
            cylinder(17,r=outer_dia/2,$fn=360);
            translate([0,0,-1]){
                cylinder(19,r=280/2,$fn=720);
            }
        }
        union() {
            translate([-151,-151,-1]){
                cube([151,301,20]);
            }
            translate([-151,-151,-1]){
                cube([301,151,20]);
            }
        }
    }
}

module front_plate(){
    difference() {
        difference() {
            cylinder(1.5,r=outer_dia/2,$fn=360);
            translate([0,0,-1]){
                cylinder(19,r=8/2,$fn=720);
            }
        }
        union() {
            translate([-151,-151,-1]){
                cube([151,301,20]);
            }
            translate([-151,-151,-1]){
                cube([301,151,20]);
            }
        }
    }
}

module back_plate(){
    difference() {
        difference() {
            cylinder(1.5,r=outer_dia/2,$fn=360);
            translate([0,0,-1]){
                cylinder(19,r=160/2,$fn=720);
            }
        }
        union() {
            translate([-151,-151,-1]){
                cube([151,301,20]);
            }
            translate([-151,-151,-1]){
                cube([301,151,20]);
            }
        }
    }
}

module outer_ring(){
    difference() {
        difference() {
            cylinder(13,r=outer_dia/2,$fn=360);
            translate([0,0,-1]){
                cylinder(19,r=260/2,$fn=720);
                translate([(outer_dia/2)*0.66,(outer_dia/2)*0.66,0]) {
                    
                    cylinder(19,r=2,$fn=100);
                }
            }
            
        }
        
        union() {
            translate([-151,-151,-1]){
                cube([151,301,20]);
            }
            translate([-151,-151,-1]){
                cube([301,151,20]);
            }
        }
    }
}

//glas_holder();
//front_plate();
//back_plate();
outer_ring();