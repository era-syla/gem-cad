import cadquery as cq

# Parameters
base_len = 100
base_wid = 20
base_h = 20

beam_thk = 10
beam_wid = 10
beam_len = 80
beam_angle = 60  # degrees

cyl_len = 30
cyl_r = 10

# Base block
base = cq.Workplane("XY").box(base_len, base_wid, base_h)

# Lever arm (beam) rotated about its bottom center
# Create beam centered at origin
beam = cq.Workplane("XY").box(beam_thk, beam_wid, beam_len)
# Move bottom face to XY plane so pivot is at origin
beam = beam.translate((0, 0, beam_len/2))
# Rotate around pivot at origin about Y axis
beam = beam.rotate((0, 0, 0), (0, 1, 0), beam_angle)
# Move pivot to the top-right edge of the base
pivot_x = base_len / 2
pivot_z = base_h
beam = beam.translate((pivot_x, 0, pivot_z))

# Cylinder hinge at top of beam, axis along Y
cylinder = (
    cq.Workplane("XZ")
    .circle(cyl_r)
    .extrude(cyl_len)
    # center cylinder along Y axis
    .translate((0, -cyl_len / 2, 0))
    # move to hinge pivot location
    .translate((pivot_x, 0, pivot_z))
)

# Combine all parts
result = base.union(beam).union(cylinder)