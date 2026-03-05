import cadquery as cq

# Geometric parameters
length = 500.0          # Total length of the tube
outer_diameter = 15.0   # Outer diameter
wall_thickness = 1.5    # Wall thickness

# Calculate inner radius based on outer diameter and wall thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow tube geometry
# 1. Initialize a Workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (which creates the hole when extruded)
# 4. Extrude the 2D profile to create the 3D solid
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)