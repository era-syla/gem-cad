import cadquery as cq

# Parameters
head_diameter = 10.0
head_height = 4.0
shaft_diameter = 6.0
shaft_length = 20.0

# Build head + smooth shaft
result = (
    cq.Workplane("XY")
      .circle(head_diameter/2).extrude(head_height)
      .faces(">Z")
      .circle(shaft_diameter/2).extrude(shaft_length)
)