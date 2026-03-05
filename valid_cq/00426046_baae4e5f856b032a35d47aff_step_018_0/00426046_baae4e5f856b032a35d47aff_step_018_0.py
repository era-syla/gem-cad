import cadquery as cq

# Parametric dimensions for the tube
height = 100.0          # Total length of the tube
outer_diameter = 8.0    # Outer diameter
wall_thickness = 0.8    # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the tube geometry
# We sketch two concentric circles on the XY plane and extrude them to create a hollow cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)