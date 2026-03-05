import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 100.0
outer_radius = 25.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (tube) geometry
# 1. Establish a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (this creates the hollow ring profile)
# 4. Extrude the profile to the specified height
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)