import cadquery as cq

# Parametric dimensions for the hexagonal standoff
height = 20.0        # Total length of the standoff
flat_to_flat = 10.0  # Distance across flats of the hexagon
hole_diameter = 4.0  # Diameter of the through hole (M4 ish)
chamfer_size = 0.5   # Size of the chamfer on the hole entrance

# Radius calculation for the hexagon from flat-to-flat distance
# For a hexagon, flat_to_flat = sqrt(3) * radius (where radius is center to vertex)
# So, radius (or circumradius) = flat_to_flat / sqrt(3)
# CadQuery's polygon method uses the circumradius if I recall correctly, but `regularPolygon`
# often takes a radius. Let's look at the standard practice.
# cq.Workplane('XY').polygon(nSides=6, diameter=...) takes a diameter across corners (circumdiameter).
# Relation: flat_to_flat = circumdiameter * cos(30 deg) = circumdiameter * (sqrt(3)/2)
# Therefore: circumdiameter = flat_to_flat / (sqrt(3)/2) = 2 * flat_to_flat / sqrt(3)
import math
circum_diameter = 2 * flat_to_flat / math.sqrt(3)

# Create the base hexagonal prism
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=circum_diameter)
    .extrude(height)
)

# Create the through hole
result = result.faces(">Z").workplane().hole(hole_diameter)

# Add chamfer to the top edge of the hole
# We select the top face, then get the inner wire (the hole's edge)
# Since .hole() cuts through, the top face now has an outer wire (hex) and inner wire (circle).
# We want to chamfer the circular edge on the top face.
result = (
    result.faces(">Z")
    .edges("%Circle") # Select circular edges on the top face
    .chamfer(chamfer_size)
)

# Optional: Add chamfer to the bottom hole edge as well, typical for spacers
# result = result.faces("<Z").edges("%Circle").chamfer(chamfer_size)

# Export or visualization step is handled by the calling environment, 
# but 'result' variable is required.