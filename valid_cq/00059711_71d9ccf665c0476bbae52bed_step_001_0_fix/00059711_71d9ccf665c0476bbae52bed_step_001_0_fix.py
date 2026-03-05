import cadquery as cq

# Parameters
cyl_r = 10
cyl_h = 5
beam_w = 6
beam_l = 80
beam_h = 5
gusset_h = 10
hole_d = 4
cyl_hole_d = 6

# Create the two end cylinders
left_cyl = cq.Workplane("XY").circle(cyl_r).extrude(cyl_h)
right_cyl = cq.Workplane("XY").transformed(offset=(beam_l, 0, 0)).circle(cyl_r).extrude(cyl_h)

# Create the beam connecting them
beam = cq.Workplane("XY").box(beam_l, beam_w, beam_h, centered=(False, True, False))

# Create a central triangular gusset on top of the beam
pts = [
    (beam_l/2 - 5, -beam_w/2),
    (beam_l/2 - 5,  beam_w/2),
    (beam_l/2 + 5,   0)
]
gusset = (
    cq.Workplane("XY")
      .transformed(offset=(0, 0, beam_h))
      .polyline(pts).close()
      .extrude(gusset_h)
)

# Combine solids
part = left_cyl.union(right_cyl).union(beam).union(gusset)

# Create cylinder through-holes
cyl_hole_cut = (
    cq.Workplane("XY")
      .pushPoints([(0, 0), (beam_l, 0)])
      .circle(cyl_hole_d/2)
      .extrude(cyl_h + 1)
)

# Create beam holes along the span
beam_hole_positions = [(20, 0), (40, 0), (60, 0)]
beam_hole_cut = (
    cq.Workplane("XY")
      .pushPoints(beam_hole_positions)
      .circle(hole_d/2)
      .extrude(beam_h + gusset_h + 1)
)

# Cut out the holes
result = part.cut(cyl_hole_cut).cut(beam_hole_cut)