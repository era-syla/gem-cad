import cadquery as cq
import math

# Parameters
beam_length = 70.0
offset_y = 10.0
cyl_rad = 5.0
cyl_height = 15.0
beam_width = 10.0
beam_thickness = 5.0
hole_rad = 2.0

# End cylinders
cyl1 = cq.Workplane("XY").circle(cyl_rad).extrude(cyl_height)
cyl2 = cq.Workplane("XY").transformed(offset=(beam_length, offset_y, 0)).circle(cyl_rad).extrude(cyl_height)

# Beam sweep path
path_wire = cq.Workplane("XY").polyline([(0, 0), (beam_length, offset_y)]).val()
beam = cq.Workplane("XY").workplane(offset=cyl_height).rect(beam_width, beam_thickness).sweep(path_wire)

# Holes through the beam
holes = None
for frac in [0.2, 0.4, 0.6]:
    x = beam_length * frac
    y = offset_y * frac
    hole = (
        cq.Workplane("XY")
          .transformed(offset=(x, y, cyl_height + beam_thickness / 2))
          .circle(hole_rad)
          .extrude(-beam_thickness - 2.0)
    )
    holes = hole if holes is None else holes.union(hole)

# Combine everything
result = cyl1.union(cyl2).union(beam).cut(holes)