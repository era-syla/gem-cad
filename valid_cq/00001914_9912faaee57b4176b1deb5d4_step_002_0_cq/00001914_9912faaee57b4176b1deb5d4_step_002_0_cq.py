import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the tube
outer_diameter = 10.0  # Outer diameter of the tube
wall_thickness = 1.5   # Wall thickness
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the tube
# We start by drawing two concentric circles and extruding them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(length)
)