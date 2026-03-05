import cadquery as cq

# Parameters based on visual estimation of the object
outer_diameter = 60.0  # Overall diameter of the cylinder
height = 15.0          # Height of the cylinder
wall_thickness = 8.0   # Thickness of the outer wall
floor_thickness = 4.0  # Thickness of the bottom base

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
cut_depth = height - floor_thickness

# Generate the geometry
# 1. Create the base solid cylinder
# 2. Select the top face
# 3. Cut a blind hole to create the cup-like shape
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-cut_depth)
)