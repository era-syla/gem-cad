import cadquery as cq

# Define parametric dimensions
outer_diameter = 20.0
height = 8.0
hole_diameter = 5.0

# Create the cylindrical body
# We start with a workplane (XY is standard)
# Draw a circle for the outer diameter
# Extrude it to the specified height
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
)

# Cut the through-hole in the center
# Select the top face
# Draw a circle for the hole
# Cut through the entire solid
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# Alternative concise one-liner approach:
# result = cq.Workplane("XY").circle(outer_diameter/2).circle(hole_diameter/2).extrude(height)