import cadquery as cq

# Define parametric variables for dimensions
outer_diameter = 20.0  # Diameter of the cylinder
wall_thickness = 2.0   # Thickness of the tube wall
height = 50.0          # Total length of the tube

# Derived dimension
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the hollow cylinder (pipe)
# Method 1: Create a solid cylinder and cut a hole
# result = (
#     cq.Workplane("XY")
#     .circle(outer_diameter / 2)
#     .extrude(height)
#     .faces(">Z")
#     .workplane()
#     .hole(inner_diameter)
# )

# Method 2: Create two concentric circles and extrude (more efficient for simple tubes)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Optional: Export to STL to verify
# cq.exporters.export(result, "pipe.stl")