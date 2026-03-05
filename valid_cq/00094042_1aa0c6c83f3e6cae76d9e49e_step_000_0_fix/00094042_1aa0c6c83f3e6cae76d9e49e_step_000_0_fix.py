import cadquery as cq

# Parameters
thickness = 5
gap = 15
height = thickness * 2 + gap
L1 = 40
radius = height / 2
width = 20
hole_dia = 6
hole_x = 10
hole1_z = thickness / 2
hole2_z = thickness + gap + thickness / 2

# Main body: side profile extruded in the Y direction
body = (
    cq.Workplane("XZ")
      .polyline([(0, thickness + gap), (L1, thickness + gap)])
      .threePointArc((L1 + radius, height / 2), (L1, 0))
      .lineTo(0, 0)
      .close()
      .extrude(width)
)

# Subtract holes through the top and bottom plates
result = (
    body
      .cut(
          cq.Workplane("ZX", origin=(hole_x, 0, hole1_z))
            .circle(hole_dia / 2)
            .extrude(width)
      )
      .cut(
          cq.Workplane("ZX", origin=(hole_x, 0, hole2_z))
            .circle(hole_dia / 2)
            .extrude(width)
      )
)