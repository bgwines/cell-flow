include <spec.scad>

$color_spectrum = [
    [0,0,204],
    [0,102,204],
    [0,204,204],
    [51,255,51],
    [153,255,51],
    [255,255,51],
    [255,153,51],
    [255,51,51],
    [255,51,153],
    [255,51,255],
];


module plate() {
  for (x = [0:$PLATE_LEN_X - 1]) {
    for (y = [0:$PLATE_LEN_Y - 1]) {
      for (z = [0:$PLATE_LEN_Z - 1]) {
        translate([x,y,z]) {
          current = $CURRENT[x][y][z];
          //current = x / ($PLATE_LEN_X - 1);
          i = floor((len($color_spectrum) - 1) * current);
          c = $color_spectrum[i];
          color([c[0] / 255, c[1] / 255, c[2] / 255]) {
            cube(0.6, center=true);
          }
        }
      }
    }
  }
}

// egg code from https://github.com/openscad/MCAD/blob/master/regular_shapes.scad
module ellipse(width, height) {
  scale([1, height/width, 1]) circle(r=width/2, $fn=$GRANULARITY);
}

module egg_outline(width, length){
  translate([0, width/2, 0])
    union() {
      rotate([0, 0, 180])
        difference() {
          ellipse(width, 2*length-width);
          translate([-length/2, 0, 0]) square(length);
        }
      circle(r=width/2, $fn=$GRANULARITY);
    }
}

module egg(width){
  length = width * 1.39;
    rotate_extrude()
        difference(){
            egg_outline(width, length);
            translate([-length, 0, 0]) square(2*length, center=true);
        }
}

module termini(pts, color_, z, is_egg = 0) {
  for (i = [0:len(pts) - 1])
    translate([pts[i][0], pts[i][1], z])
    color(color_)
      if (is_egg) {
        translate([0,0,-1]) egg(3);
      } else {
        cylinder(r=0.5, h=$CELL_H, center=true, $fn=$GRANULARITY);
      }
}


module main() {
  termini($SOURCES, "orange", $CELL_H/2 + $PLATE_LEN_Z);
  termini($SINKS, "cyan", -$CELL_H/2 - 1, is_egg=1);
  plate();
}

main();
