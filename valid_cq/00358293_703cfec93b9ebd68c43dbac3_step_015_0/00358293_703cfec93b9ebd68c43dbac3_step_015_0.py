import cadquery as cq

# Parametric dimensions
height = 100.0         # Total height of the tube
outer_diameter = 30.0  # External diameter
wall_thickness = 3.0   # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the hollow cylinder (tube)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)  # Draw outer boundary
    .circle(inner_radius)  # Draw inner boundary to create the hole
    .extrude(height)       # Extrude to create the solid
)