import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the tube
outer_diameter = 20.0 # Outer diameter of the tube
wall_thickness = 1.0  # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow tube
# Method 1: Create a solid cylinder and cut a smaller one from it
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Alternative Method 2 (using shell, often cleaner for uniform thickness):
# result = (
#     cq.Workplane("XY")
#     .circle(outer_radius)
#     .extrude(height)
#     .faces(">Z")
#     .shell(-wall_thickness)
# )

# Export or display is handled by the caller, 'result' is the final object