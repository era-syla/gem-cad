import cadquery as cq

# Define parametric dimensions for the hollow cylinder
height = 60.0          # Total height of the tube
outer_diameter = 25.0  # Outer diameter
wall_thickness = 3.0   # Wall thickness

# Calculate derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the geometry
# 1. Initialize a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle to create a ring profile
# 4. Extrude the profile vertically to the defined height
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)