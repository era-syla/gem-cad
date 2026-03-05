import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
height = 100.0          # Total length of the tube
outer_diameter = 30.0   # Outer diameter
wall_thickness = 4.0    # Wall thickness

# Calculate radii
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder model
# We draw two concentric circles on the XY plane and extrude them.
# CadQuery automatically interprets the area between concentric shapes as a solid profile.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)