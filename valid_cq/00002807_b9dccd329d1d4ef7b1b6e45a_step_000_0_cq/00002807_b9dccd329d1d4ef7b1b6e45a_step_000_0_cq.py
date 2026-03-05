import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the cylinder
outer_radius = 40.0  # Outer radius of the cylinder
wall_thickness = 10.0 # Thickness of the wall

# Calculated dimension
inner_radius = outer_radius - wall_thickness

# Generate the 3D model
# Method: Create a solid cylinder and cut a smaller cylinder from the center
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)

# Alternative method (single operation profile):
# result = (
#     cq.Workplane("XY")
#     .circle(outer_radius)
#     .circle(inner_radius)
#     .extrude(height)
# )