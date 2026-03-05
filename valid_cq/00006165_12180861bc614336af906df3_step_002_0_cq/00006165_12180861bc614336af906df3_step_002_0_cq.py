import cadquery as cq

# Parametric dimensions
outer_diameter = 30.0  # The outer diameter of the washer
inner_diameter = 14.0  # The inner diameter (hole) of the washer
thickness = 4.0        # The thickness of the washer

# Create the washer geometry
# Method 1: Create a cylinder and cut a hole
# result = cq.Workplane("XY").cylinder(thickness, outer_diameter/2).faces(">Z").hole(inner_diameter)

# Method 2: Create a 2D sketch of two circles and extrude
# This is generally cleaner for simple annular shapes
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)