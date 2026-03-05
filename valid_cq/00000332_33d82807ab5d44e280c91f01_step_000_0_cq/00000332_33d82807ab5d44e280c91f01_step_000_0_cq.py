import cadquery as cq

# Parametric dimensions
length = 100.0       # Length of the tube
outer_diameter = 50.0 # Outer diameter of the tube
wall_thickness = 2.0  # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (tube)
# We create a solid cylinder and cut a smaller cylinder from inside,
# or simply extrude a ring.
# Using the Workplane method with circle and extrusion is very clear.

result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer circle
    .circle(inner_radius)  # Inner circle to create the hollow part
    .extrude(length)       # Extrude to create the tube length
)

# Alternatively, using solid operations:
# result = cq.Solid.makeCylinder(outer_radius, length).cut(
#     cq.Solid.makeCylinder(inner_radius, length)
# )

# Export or display is handled by the environment, 'result' is the required variable name.