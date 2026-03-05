import cadquery as cq

# Parameters
top_tube_length = 500
top_tube_diameter = 30
steerer_angle_degrees = 75
seat_tube_length = 600
seat_tube_diameter = 35
down_tube_length = 550
down_tube_diameter = 40
bb_diameter = 45
bb_length = 68

# Top Tube
top_tube = (cq.Workplane("XY")
            .circle(top_tube_diameter / 2)
            .extrude(top_tube_length)
            .rotate((0, 0, 0), (0, 1, 0), 90))

# Seat Tube
seat_tube = (cq.Workplane("XY")
             .circle(seat_tube_diameter / 2)
             .extrude(seat_tube_length))

# Down Tube
down_tube = (cq.Workplane("XY")
             .circle(down_tube_diameter / 2)
             .extrude(down_tube_length)
             .rotate((0, 0, 0), (0, 1, 0), 90)
             .rotate((0, 0, 0), (1, 0, 0), steerer_angle_degrees))

# Bottom Bracket
bottom_bracket = (cq.Workplane("XY")
                  .circle(bb_diameter / 2)
                  .extrude(bb_length))

# Assemble Frame
result = (top_tube
          .union(seat_tube.translate((0, -top_tube_length / 2 - seat_tube_length / 2, 0)))
          .union(down_tube.translate((0, -top_tube_length / 2, 0)))
          .union(bottom_bracket.translate((0, -seat_tube_length / 2, 0))))