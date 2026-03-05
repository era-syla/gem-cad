import cadquery as cq

# Parameters
base_width = 20.0
top_width = 15.0
side_height = 32.5
thickness = 10.0
top_radius = top_width / 2.0
hole_diameter = 5.0
hole_radius = hole_diameter / 2.0
hole_z = side_height

# Create the bracket profile and extrude
result = (
    cq.Workplane("XZ")
      .polyline([
          (-base_width/2, 0),
          ( base_width/2, 0),
          ( top_width/2, side_height)
      ])
      .threePointArc((0, side_height + top_radius), (-top_width/2, side_height))
      .close()
      .extrude(thickness)
)

# Create the hole as a cylinder and cut through
hole_cyl = (
    cq.Workplane("XZ", origin=(0, 0, hole_z))
      .circle(hole_radius)
      .extrude(thickness)
)

result = result.cut(hole_cyl)