import cadquery as cq
import math

# Geometric Parameters
shaft_diameter = 8.0      # Diameter of the bolt shaft
shaft_length = 20.0       # Length of the bolt shaft
head_flats = 14.0         # Width across flats (wrench size)
head_height = 6.0         # Height (thickness) of the bolt head

# Calculate the diameter across corners (circumscribed circle)
# Formula: D_corner = D_flat / cos(30deg) = D_flat / (sqrt(3)/2)
head_outer_diameter = head_flats / (math.sqrt(3) / 2.0)

# Create the Hex Head
# We start on the XY plane and extrude upwards
# By default, polygon vertices are aligned with the X-axis
bolt_head = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=head_outer_diameter)
    .extrude(head_height)
)

# Create the Shaft
# We select the bottom face of the head (lowest Z value)
# Create a workplane on it (normal points away from the solid, i.e., -Z)
# Draw the circle and extrude
result = (
    bolt_head
    .faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)