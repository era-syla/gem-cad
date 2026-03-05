import cadquery as cq

# Parameters
base_length = 120.0
base_width = 50.0
base_height = 15.0

raised_length = 65.0
raised_height = 30.0

cutout_radius = 22.5
hole_pitch = 92.5
hole_dia = 8.0

# 1. Base and raised block
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .faces(">Z")
    .workplane()
    .box(raised_length, base_width, raised_height)
)

# 2. U-Shape Cutout
# The base box is centered at Z=0, so its top is at base_height / 2.
# The raised block sits on top of the base.
cutout_center_z = (base_height / 2.0) + raised_height

cylinder_cut = (
    cq.Workplane("XZ")
    .center(0, cutout_center_z)
    .circle(cutout_radius)
    .extrude(base_width + 10, both=True)
)

result = result.cut(cylinder_cut)

# 3. Mounting Holes
result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints([(hole_pitch/2, 0), (-hole_pitch/2, 0)])
    .hole(hole_dia)
)