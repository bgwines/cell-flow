include <spec.scad>

module plate() {
  for (x = [0:$PLATE_LEN_X - 1]) {
    for (y = [0:$PLATE_LEN_Y - 1]) {
      for (z = [0:$PLATE_LEN_Z - 1]) {
        translate([x,y,z]) {
          c = $COLORS[x][y][z];
          //color([0,c,c])
            cube(c, center=true);
        }
      }
    }
  }
}

module termini(pts, color_, z) {
  for (i = [0:len(pts) - 1])
    translate([pts[i][0], pts[i][1], z])
    color(color_)
    cylinder(r=0.5, h=$CELL_H, center=true, $fn=$GRANULARITY);
}

module main() {
  termini($SOURCES, "orange", $CELL_H/2 + $PLATE_LEN_Z);
  termini($SINKS, "cyan", -$CELL_H/2 - 1);
  plate();
}

main();
