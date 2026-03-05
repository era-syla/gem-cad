import cadquery as cq

inner_radius = 50
wall_thickness = 2
tube_height = 10
bend_angle = 180

result = (
    cq.Workplane("XZ")
      .moveTo(inner_radius, -tube_height/2)
      .hLine(wall_thickness)
      .vLine(tube_height)
      .hLine(-wall_thickness)
      .vLine(-tube_height)
      .close()
      .revolve(bend_angle)
)