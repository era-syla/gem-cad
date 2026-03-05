import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
cylinder_height = 60.0      # Total length of the cylinder
outer_diameter = 20.0       # Outer diameter of the tube
inner_diameter = 8.0        # Inner diameter (the through-hole)

# Create the hollow cylinder geometry
# Method: Draw two concentric circles on the XY plane and extrude them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Outer profile
    .circle(inner_diameter / 2.0)  # Inner profile (void)
    .extrude(cylinder_height)      # Extrude to create the solid tube
)