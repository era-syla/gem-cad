import cadquery as cq

# Parameters
shaft_length = 30.0
shaft_diameter = 6.0
head_flat_to_flat = 10.0
head_height = 4.0

# Create shaft (smooth cylinder)
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(-shaft_length)

# Create hex head
head = cq.Workplane("XY").polygon(6, head_flat_to_flat).extrude(head_height)

# Combine shaft and head
result = shaft.union(head)