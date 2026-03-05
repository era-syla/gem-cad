import cadquery as cq

# Parameters
length = 200.0
bottom_width = 20.0
top_width = 18.0
bottom_thickness = 2.0
side_height = 4.0
top_thickness = 2.0

# Sketch the cross‐section in the XZ plane and extrude along Y
result = (
    cq.Workplane("XZ")
      .polyline([
          (-bottom_width/2, 0),
          ( bottom_width/2, 0),
          ( bottom_width/2, bottom_thickness),
          ( top_width/2, bottom_thickness),
          ( top_width/2, bottom_thickness + side_height),
          (-top_width/2, bottom_thickness + side_height),
          (-bottom_width/2, bottom_thickness)
      ])
      .close()
      .extrude(length)
)