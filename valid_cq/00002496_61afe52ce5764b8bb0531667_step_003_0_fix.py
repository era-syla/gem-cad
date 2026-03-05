import cadquery as cq

# Create a rivet/pin with a round head
# Parameters
shaft_diameter = 4.0
shaft_length = 12.0
head_diameter = 8.0
head_height = 2.0

# Build the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# Build the head (flat cylinder with rounded top edge)
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Combine shaft and head
result = shaft.union(head)

# Add fillet to the top edge of the head
result = result.edges(">Z").fillet(head_height * 0.45)