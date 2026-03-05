import cadquery as cq

# Parameters
head_diameter = 10
head_height = 2
shaft_diameter = 6
shaft_length = 20
phillips_diameter = 4

# Create the head
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Create the shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
    .faces(">Z")
    .workplane()
    .polygon(4, phillips_diameter)
    .cutBlind(-head_height)
)

# Combine head and shaft
result = head.union(shaft)