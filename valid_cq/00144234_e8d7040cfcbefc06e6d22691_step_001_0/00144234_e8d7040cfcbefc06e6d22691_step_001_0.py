import cadquery as cq

# Parametric dimensions based on the visual estimation of the provided image
length = 200.0        # Total length of the strap
width = 25.0          # Width of the strap
thickness = 2.0       # Thickness of the plate
hole_diameter = 5.0   # Diameter of the holes at the ends

# The slot2D function defines a stadium shape by the distance between 
# the centers of the two arcs (center_dist) and the diameter (width).
# Total length = center_dist + width (radius * 2)
center_dist = length - width

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .slot2D(center_dist, width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-center_dist / 2.0, 0), (center_dist / 2.0, 0)])
    .hole(hole_diameter)
)