import cadquery as cq

# Parametric dimensions
outer_diameter = 10.0  # Outer diameter of the tube
wall_thickness = 1.0   # Thickness of the tube wall
length = 100.0         # Length of the tube

# Derived dimensions
inner_diameter = outer_diameter - (2 * wall_thickness)
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Create the hollow tube
# Method: Sketch two concentric circles and extrude them
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)