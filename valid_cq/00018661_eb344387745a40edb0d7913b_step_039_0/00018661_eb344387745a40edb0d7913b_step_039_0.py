import cadquery as cq
import math

# Parameters
height = 60.0          # Total length of the hexagonal standoff
across_flats = 12.0    # Distance across flats (wrench size)
hole_diameter = 6.0    # Diameter of the central through-hole

# Calculate the circumscribed diameter (distance across corners)
# Relation: Across Flats = Across Corners * cos(30 degrees)
across_corners = across_flats / (math.sqrt(3) / 2.0)

# Generate the geometry
# 1. Create a Workplane on the XY plane
# 2. Draw a hexagon using the calculated across_corners diameter
# 3. Draw a circle for the inner hole (subtractive by nesting in extrusion)
# 4. Extrude the profile to the specified height
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=across_corners)
    .circle(hole_diameter / 2.0)
    .extrude(height)
)