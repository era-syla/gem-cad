import cadquery as cq

# Parametric dimensions
w = 42.0
t = 2.5
r_corner = 3.0
d_center = 22.0
d_mount = 3.2
d_small = 2.0
hole_spacing = 31.0
offset = hole_spacing / 2.0
spacing_x = 60.0

# Plate 1 (L-shaped bracket)
# Creating a square base, cutting out the bottom-right quadrant cleanly, then filleting all Z-edges
plate1_base = (cq.Workplane("XY")
               .box(w, w, t)
               .faces(">Z").workplane()
               .center(w/4 + 1, -w/4 - 1)
               .rect(w/2 + 2, w/2 + 2)
               .cutThruAll()
               .edges("|Z").fillet(r_corner)
              )

plate1 = (plate1_base
          .faces(">Z").workplane()
          .pushPoints([(-offset, offset), (offset, offset), (-offset, -offset)])
          .hole(d_mount)
          .faces(">Z").workplane()
          .pushPoints([(-8, -offset), (8, offset)])
          .hole(d_small)
         )

# Plates 2 and 3 (Full square plates)
plate2_base = cq.Workplane("XY").box(w, w, t).edges("|Z").fillet(r_corner)

plate2 = (plate2_base
          .faces(">Z").workplane()
          .hole(d_center)
          .faces(">Z").workplane()
          .rect(hole_spacing, hole_spacing, forConstruction=True)
          .vertices().hole(d_mount)
          .faces(">Z").workplane()
          .pushPoints([(-8, -offset), (8, offset)])
          .hole(d_small)
         )

plate3 = plate2

# Assemble into final result
result = (cq.Workplane("XY")
          .add(plate1.translate((-spacing_x, 0, 0)).val())
          .add(plate2.val())
          .add(plate3.translate((spacing_x, 0, 0)).val())
         )