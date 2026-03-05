import cadquery as cq

# Parametric dimensions
shaft_length = 80.0
shaft_diameter = 5.0
head_diameter = 10.0
head_length = 12.0
slot_width = 3.0
slot_depth = 8.0

# Create the main shaft geometry (aligned along X axis)
# Start with a circle on the YZ plane and extrude
result = cq.Workplane("YZ").circle(shaft_diameter / 2.0).extrude(shaft_length)

# Add the cylindrical head to the end of the shaft
# Select the face at the end of the shaft (+X direction)
result = (
    result.faces(">X")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_length)
)

# Cut the slot into the head
# Select the end face of the head, draw a rectangle wider than the head
# to ensure a complete cut through the diameter, and cut inwards
result = (
    result.faces(">X")
    .workplane()
    .rect(head_diameter * 2.0, slot_width)
    .cutBlind(-slot_depth)
)