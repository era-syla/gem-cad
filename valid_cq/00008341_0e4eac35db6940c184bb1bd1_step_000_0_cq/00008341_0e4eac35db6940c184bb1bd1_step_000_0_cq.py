import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
thickness = 3.0
polygon_sides = 8
polygon_radius = 6.0  # Radius from center to polygon vertex (circumradius)

# Create the washer with octagonal hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .polygon(polygon_sides, polygon_radius * 2) # polygon uses diameter
    .extrude(thickness)
)