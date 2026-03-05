import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
inner_diameter = 42.0
thickness = 5.0

# Calculate radii
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Create the ring geometry
# We start with a workplane, sketch two circles, and extrude the difference
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

# Alternative method using tube/hollow cylinder primitive if preferred:
# result = cq.Workplane("XY").tube(outer_radius, inner_radius, thickness)