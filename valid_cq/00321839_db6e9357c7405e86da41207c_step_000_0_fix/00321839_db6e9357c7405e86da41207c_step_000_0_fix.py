import cadquery as cq

# Parameters for the wedge
base_length = 40
triangle_height = 20
extrude_depth = 60

# Create a right‐triangle in the XZ plane and extrude along Y
result = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (base_length, 0),
          (0, triangle_height)
      ])
      .close()
      .extrude(extrude_depth)
)