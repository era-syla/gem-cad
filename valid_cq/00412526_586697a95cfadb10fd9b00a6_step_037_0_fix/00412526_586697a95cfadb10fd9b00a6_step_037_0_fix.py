import cadquery as cq

# Parameters
shaft_length = 25.0
shaft_diameter = 6.0
head_diameter = 12.0
head_height = 4.0
head_fillet = 1.0
recess_width = 1.5
recess_length = 8.0
recess_depth = 2.5

# Create shaft
shaft = cq.Workplane("XY").cylinder(shaft_length, shaft_diameter / 2)

# Create head
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)
# Fillet head edges
head = head.edges(">Z").fillet(head_fillet)
head = head.edges("<Z").fillet(head_fillet)

# Combine shaft and head
result = shaft.union(head)

# Create Phillips recess: horizontal slot
result = result.faces(">Z").workplane().rect(recess_length, recess_width).cutBlind(-recess_depth)
# Create Phillips recess: vertical slot
result = result.faces(">Z").workplane().rect(recess_width, recess_length).cutBlind(-recess_depth)