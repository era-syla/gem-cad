import cadquery as cq

base_width = 10
side_height = 4
peak_height = 8
length = 150

profile = (
    cq.Workplane("XZ")
      .polyline([
          (-base_width/2, 0),
          ( base_width/2, 0),
          ( base_width/2, side_height),
          (             0, peak_height),
          (-base_width/2, side_height)
      ])
      .close()
)

result = profile.extrude(length)