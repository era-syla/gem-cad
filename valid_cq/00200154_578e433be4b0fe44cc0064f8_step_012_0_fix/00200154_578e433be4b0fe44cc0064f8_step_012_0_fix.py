import cadquery as cq

# Parameters
length = 200.0
width = 10.0
thickness = 10.0
slot_width = 4.0
slot_depth = 4.0
hole_dia = 3.0
hole_count = 8

# Calculate hole positions along the length
spacing = length / (hole_count + 1)
y_positions = [(-length/2 + spacing * (i + 1)) for i in range(hole_count)]

# Build the main rail
result = (
    cq.Workplane("XY")
      .rect(width, thickness)
      .extrude(length)
)

# Cut the T-slot on the +X face
result = (
    result.faces(">X")
          .workplane()
          .rect(slot_width, length)
          .cutBlind(slot_depth)
)

# Drill mounting holes on the -X face
result = (
    result.faces("<X")
          .workplane()
          .pushPoints([(0, y) for y in y_positions])
          .hole(hole_dia)
)
