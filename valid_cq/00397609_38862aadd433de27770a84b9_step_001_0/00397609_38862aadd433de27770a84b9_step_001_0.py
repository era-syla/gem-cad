import cadquery as cq

# Parametric dimensions
length = 100.0         # Total length of the tube
outer_diameter = 30.0  # Outside diameter
wall_thickness = 2.0   # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the 3D model
# We draw two concentric circles on the XY plane. 
# CadQuery automatically detects the region between them as the profile to extrude.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)