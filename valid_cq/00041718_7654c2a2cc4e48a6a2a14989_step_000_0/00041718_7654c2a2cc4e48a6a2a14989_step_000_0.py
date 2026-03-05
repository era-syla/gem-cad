import cadquery as cq

# Parametric dimensions for the tube
length = 200.0        # Total length of the tube
outer_diameter = 15.0 # Outer diameter
wall_thickness = 1.5  # Thickness of the tube wall

# Calculate radii
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow tube by drawing two concentric circles and extruding
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer profile
    .circle(inner_radius)  # Inner hole profile
    .extrude(length)       # Extrude to create the solid tube
)