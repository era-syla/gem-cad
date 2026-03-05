import cadquery as cq

# -- Parameters --
length = 200.0
width = 50.0
height = 50.0
wall_thickness = 4.0

# Hole parameters
num_holes = 8
hole_dia = 6.0
csk_dia = 10.0
csk_angle = 90.0

# Calculate hole positions (evenly spaced along length)
# Spacing = Length / (N + 1)
spacing = length / (num_holes + 1)
# Generate X coordinates centered around 0
# The tube spans from -length/2 to +length/2
hole_x_positions = [-length/2 + (i + 1) * spacing for i in range(num_holes)]
hole_locations = [(x, 0) for x in hole_x_positions]

# -- 3D Modeling --

# 1. Create the base hollow square tube
# Sketch two concentric rectangles on YZ plane to define the wall
# Extrude along X axis, centered
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .rect(width - 2*wall_thickness, height - 2*wall_thickness)
    .extrude(length, both=True)
)

# 2. Cut countersunk holes on the Top Face (+Z)
# Select the top face, create a workplane, push points, and cut holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_dia, csk_dia, csk_angle)
)

# 3. Cut countersunk holes on the Side Face (+Y)
# Use the same longitudinal distribution
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_dia, csk_dia, csk_angle)
)