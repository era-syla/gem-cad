import cadquery as cq

# Parameters
tube_diameter = 30
tube_length = 200
headtube_length = 120

# Main Frame
main_frame = (cq.Workplane("front")
              .circle(tube_diameter / 2)
              .extrude(tube_length))

# Head Tube
head_tube = (cq.Workplane("top")
             .circle(tube_diameter / 2)
             .extrude(headtube_length)
             .translate((0, tube_length / 2, tube_diameter / 2)))

# Assembling the frame
result = main_frame.union(head_tube)