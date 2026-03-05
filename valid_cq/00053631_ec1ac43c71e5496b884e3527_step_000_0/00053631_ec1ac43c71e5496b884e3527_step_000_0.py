import cadquery as cq

# Parametric dimensions
thickness = 1.0         # Thickness of the washer
outer_diameter = 30.0   # Outer diameter of the disk
hex_diameter = 10.0     # Diameter of the circumscribed circle for the hex hole

# Generate the CAD model
# 1. Start on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner hexagon (creates a hole when extruded with the outer circle)
# 4. Extrude to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .polygon(nSides=6, diameter=hex_diameter)
    .extrude(thickness)
)