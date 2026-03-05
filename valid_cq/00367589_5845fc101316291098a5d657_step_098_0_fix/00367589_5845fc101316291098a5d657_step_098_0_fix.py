import cadquery as cq

# Define bolt dimensions
hex_diameter = 10
hex_height = 4
shaft_diameter = 6
shaft_length = 40
thread_length = 20
thread_pitch = 2

# Create hex head
hex_head = cq.Workplane("XY").polygon(6, hex_diameter).extrude(hex_height)

# Create shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length - thread_length)
)

# Create thread
thread = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .workplane(offset=thread_length)
    .circle(shaft_diameter / 2 - 1)
    .loft(combine=True)
    .faces(">Z")
    .workplane()
    .circle(thread_pitch / 2)
    .extrude(thread_pitch / 2, taper=45)
)

# Combine head, shaft, and thread
result = hex_head.union(shaft).union(thread)