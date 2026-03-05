import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the tube
outer_diameter = 30.0 # Outer diameter of the tube
wall_thickness = 1.0  # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow tube
# Method 1: Create a solid cylinder and cut a hole
# result = cq.Workplane("XY").circle(outer_radius).extrude(height).faces(">Z").hole(inner_radius * 2)

# Method 2: Create a sketch with two circles and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer boundary
    .circle(inner_radius)  # Inner boundary (creates the hole automatically in 2D)
    .extrude(height)
)

# Export or visualization step is implicit by creating the 'result' variable