import cadquery as cq

# Parameter definitions
outer_diameter = 50.0  # Outer diameter of the tube
wall_thickness = 5.0   # Thickness of the tube wall
height = 80.0          # Height (length) of the tube

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# Method 1: Create a solid cylinder and cut a hole
# result = cq.Workplane("XY").circle(outer_radius).extrude(height).faces(">Z").hole(inner_radius * 2)

# Method 2: Create a 2D annular ring and extrude it (often cleaner for simple tubes)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer circle
    .circle(inner_radius)  # Inner circle (creates the void)
    .extrude(height)       # Extrude to create the tube
)

# Export the result (optional, but good practice for verification)
# cq.exporters.export(result, "tube.step")