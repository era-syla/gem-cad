import cadquery as cq

# Parametric dimensions
height = 100.0       # Total length of the tube
outer_radius = 20.0  # Outer radius of the tube
wall_thickness = 5.0 # Thickness of the tube wall

# Derived dimensions
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# Method 1: Create a cylinder and subtract a smaller cylinder
result = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
    .faces(">Z")
    .hole(inner_radius * 2)
)

# Alternative Method 2 (Sketch based - simpler logic for cross-section):
# result = (
#     cq.Workplane("XY")
#     .circle(outer_radius)
#     .circle(inner_radius)
#     .extrude(height)
# )

# The result variable contains the final geometry