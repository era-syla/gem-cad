import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Outer diameter of the tube
wall_thickness = 3.0   # Thickness of the tube wall
height = 100.0         # Height of the tube

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# Method 1: Create a solid cylinder and cut a smaller one
# result = (
#     cq.Workplane("XY")
#     .circle(outer_radius)
#     .extrude(height)
#     .faces(">Z")
#     .workplane()
#     .circle(inner_radius)
#     .cutBlind(-height)
# )

# Method 2: Create a sketch with two circles and extrude (more robust)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer circle
    .circle(inner_radius)  # Inner circle (creates the hole automatically)
    .extrude(height)
)