import cadquery as cq

# Parametric dimensions
height = 80.0       # Total height of the prism
diameter = 12.0     # Circumscribed diameter (corner-to-corner) of the hexagon

# Create the hexagonal prism
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=diameter)
    .extrude(height)
)