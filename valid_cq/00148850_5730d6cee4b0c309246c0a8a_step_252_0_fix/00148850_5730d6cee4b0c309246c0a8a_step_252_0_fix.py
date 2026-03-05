import cadquery as cq

# Parameters
thickness = 5.0
R_outer = 40.0
R_central_outer = 12.0
R_center_hole = 5.0
w_spoke = 5.0

# Outer ring
result = cq.Workplane("XY").circle(R_outer).circle(R_central_outer).extrude(thickness)

# Spokes
beam_length = R_outer - R_central_outer
beam_offset = R_central_outer + beam_length/2
for angle in [0, 90, 180, 270]:
    beam = (
        cq.Workplane("XY")
        .center(beam_offset, 0)
        .rect(beam_length, w_spoke)
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(beam)

# Central ring
center_ring = cq.Workplane("XY").circle(R_central_outer).circle(R_center_hole).extrude(thickness)
result = result.union(center_ring)