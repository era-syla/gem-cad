import cadquery as cq

# Parametric dimensions for the spring
coil_mean_diameter = 12.0
wire_diameter = 2.0
pitch = 4.0
number_of_turns = 20

# Derived calculations
coil_radius = coil_mean_diameter / 2.0
wire_radius = wire_diameter / 2.0
total_height = pitch * number_of_turns

# Create the helical path wire
# makeHelix generates a helix along the Z-axis starting at (radius, 0, 0)
helix_path = cq.Wire.makeHelix(
    pitch=pitch,
    height=total_height,
    radius=coil_radius
)

# Create the solid spring by sweeping a circular profile along the path
# We define the profile on the XZ plane and center it at the helix start radius
result = (
    cq.Workplane("XZ")
    .center(coil_radius, 0)
    .circle(wire_radius)
    .sweep(cq.Workplane(obj=helix_path), isFrenet=True)
)