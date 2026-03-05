import cadquery as cq

# Parametric dimensions for the tube
height = 200.0          # Total length of the tube
outer_diameter = 50.0   # External diameter
wall_thickness = 2.5    # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# We draw two concentric circles on the workplane and extrude the resulting face
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Outer boundary
    .circle(inner_radius)  # Inner boundary (hole)
    .extrude(height)
)