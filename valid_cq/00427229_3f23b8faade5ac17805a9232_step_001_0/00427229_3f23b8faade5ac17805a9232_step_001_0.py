import cadquery as cq

# Parametric dimensions based on the image analysis
# The object appears to be a long, slender tube or hollow rod
length = 150.0          # Total vertical length
outer_diameter = 6.0    # Outer diameter of the rod
inner_diameter = 2.0    # Diameter of the hole visible on the top face

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Draw outer profile
    .circle(inner_diameter / 2.0)  # Draw inner profile (hole)
    .extrude(length)               # Extrude to create the solid tube
)