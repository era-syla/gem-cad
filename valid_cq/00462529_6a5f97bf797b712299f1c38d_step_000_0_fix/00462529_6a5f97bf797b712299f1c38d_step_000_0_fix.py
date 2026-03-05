import cadquery as cq

# Parameters
width = 10
height = 100
horiz = 80
thickness = 5
radius = width
hole_dia = 6
hole_offset = 15

# Build the L-shaped profile with outer fillet in 2D and extrude into 3D
result = (
    cq.Workplane("XY")
      .polyline([
          (0, 0),
          (width, 0),
          (width, height - width),
          (horiz, height - width),
      ])
      .radiusArc((horiz - width, height), width)
      .lineTo(0, height)
      .close()
      .extrude(thickness)
)

# Drill holes through the thickness on the top face
result = (
    result
      .faces(">Z")
      .workplane()
      .pushPoints([
          ( hole_offset,            height - hole_offset),
          ( horiz - hole_offset,    height - hole_offset),
          ( horiz - hole_offset,    hole_offset),
          ( hole_offset,            hole_offset),
      ])
      .hole(hole_dia)
)

# 'result' now contains the final solid
result