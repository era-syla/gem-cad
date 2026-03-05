import cadquery as cq

# Parametric dimensions
base_len = 100.0
base_h = 10.0
block_len = 60.0
total_h = 35.0
radius = 20.0
width = 40.0
hole_dist = 80.0
hole_dia = 6.0

# Create the 2D profile and extrude
profile = (
    cq.Workplane("XZ")
    .moveTo(-base_len / 2.0, 0)
    .lineTo(base_len / 2.0, 0)
    .lineTo(base_len / 2.0, base_h)
    .lineTo(block_len / 2.0, base_h)
    .lineTo(block_len / 2.0, total_h)
    .lineTo(radius, total_h)
    .threePointArc((0, total_h - radius), (-radius, total_h))
    .lineTo(-block_len / 2.0, total_h)
    .lineTo(-block_len / 2.0, base_h)
    .lineTo(-base_len / 2.0, base_h)
    .close()
)

result = profile.extrude(width / 2.0, both=True)

# Add mounting holes
result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints([(hole_dist / 2.0, 0), (-hole_dist / 2.0, 0)])
    .hole(hole_dia)
)