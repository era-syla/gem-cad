import cadquery as cq

# Parameters for the geometry
length = 120.0
width = 40.0
thickness = 10.0
square_hole_side = 10.0
end_hole_diameter = 4.0
end_hole_spacing = 20.0  # Center-to-center distance
end_hole_depth = 20.0

# 1. Create the main rectangular body
# The box is centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the central square through-hole
# Select the top face (+Z), create a workplane, draw the square, and cut through
result = result.faces(">Z").workplane() \
    .rect(square_hole_side, square_hole_side) \
    .cutThruAll()

# 3. Create the two circular holes on the end face
# Select the face at the positive X end
# On this face, the local X-axis typically aligns with the global Y-axis (width)
# We position points symmetrically along the width
result = result.faces(">X").workplane() \
    .pushPoints([(end_hole_spacing / 2, 0), (-end_hole_spacing / 2, 0)]) \
    .circle(end_hole_diameter / 2) \
    .cutBlind(-end_hole_depth)