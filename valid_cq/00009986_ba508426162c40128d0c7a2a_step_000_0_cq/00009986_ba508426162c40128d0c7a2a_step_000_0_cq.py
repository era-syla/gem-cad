import cadquery as cq

# Parametric dimensions
length = 200.0  # Total length of the tube
outer_diameter = 8.0  # Outer diameter of the tube
wall_thickness = 1.0  # Wall thickness

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the tube geometry
# We create a workplane, draw two concentric circles, and extrude them
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)

# Alternatively, using the dedicated tube method if preferred (commented out):
# result = cq.Workplane("XY").tube(length, outer_radius, inner_radius)