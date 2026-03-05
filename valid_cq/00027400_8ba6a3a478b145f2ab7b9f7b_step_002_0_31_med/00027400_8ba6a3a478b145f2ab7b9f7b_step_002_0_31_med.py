import cadquery as cq

# Parameters
hex_radius = 50.0
thickness = 5.0

# Create the hexagonal tile
result = (
    cq.Workplane("XY")
    .polygon(6, hex_radius * 2)
    .extrude(thickness)
)