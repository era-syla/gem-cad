import cadquery as cq

# Geometric parameters for the hollow cylinder
height = 60.0          # Total height of the cylinder
outer_diameter = 25.0  # Diameter of the outer wall
inner_diameter = 12.0  # Diameter of the inner hole

# Create the 3D model
# 1. Initialize a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (which creates the void when extruded)
# 4. Extrude the profile to the specified height
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)