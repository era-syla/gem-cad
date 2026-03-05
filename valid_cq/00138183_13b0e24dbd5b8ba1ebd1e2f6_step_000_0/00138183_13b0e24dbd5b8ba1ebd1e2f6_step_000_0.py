import cadquery as cq

# Geometric parameters based on the visual estimation of the image
# The object appears to be a long, thin-walled cylindrical tube
length = 300.0          # Total length of the tube
outer_diameter = 10.0   # External diameter
wall_thickness = 1.0    # Thickness of the tube wall

# Calculate derived dimension
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the CAD model
# We establish a workplane, draw concentric circles for the tube profile, and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)