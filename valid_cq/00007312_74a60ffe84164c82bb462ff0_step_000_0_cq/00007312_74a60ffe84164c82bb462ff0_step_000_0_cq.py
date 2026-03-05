import cadquery as cq

# Parametric dimensions
height = 100.0       # Total length of the tube
outer_diameter = 30.0 # Outer diameter of the cylinder
wall_thickness = 5.0  # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the geometry
# Method 1: Create a cylinder and cut a smaller cylinder from it
# result = cq.Workplane("XY").cylinder(height, outer_radius).faces(">Z").hole(inner_radius * 2)

# Method 2: Sketch a circle, extrude, sketch inner circle, cut
# result = (
#     cq.Workplane("XY")
#     .circle(outer_radius)
#     .extrude(height)
#     .faces(">Z")
#     .circle(inner_radius)
#     .cutThruAll()
# )

# Method 3 (Cleanest for a simple tube): Extrude a ring profile
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)