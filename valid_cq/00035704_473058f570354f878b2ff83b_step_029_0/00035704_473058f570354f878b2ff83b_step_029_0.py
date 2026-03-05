import cadquery as cq

# Parametric dimensions
height = 150.0        # Total height of the tube
outer_diameter = 50.0 # Outer diameter of the tube
wall_thickness = 1.5  # Wall thickness

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (tube) geometry
# We sketch two concentric circles and extrude the region between them
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)