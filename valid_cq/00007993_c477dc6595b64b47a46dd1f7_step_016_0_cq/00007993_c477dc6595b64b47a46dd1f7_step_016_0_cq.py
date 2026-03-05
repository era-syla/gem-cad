import cadquery as cq

# Parameters for the tube
length = 100.0       # Total height of the tube
outer_diameter = 40.0 # Outer diameter
wall_thickness = 3.0 # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the tube
# Method 1: Create a cylinder and cut a smaller cylinder out of it
# result = cq.Workplane("XY").cylinder(length, outer_radius).faces(">Z").hole(inner_radius * 2)

# Method 2: Sketch two circles and extrude (more explicit about the profile)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)