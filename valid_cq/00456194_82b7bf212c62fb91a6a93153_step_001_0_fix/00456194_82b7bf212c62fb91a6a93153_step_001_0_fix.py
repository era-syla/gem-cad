import cadquery as cq

# Create the main pipe
pipe1 = cq.Workplane("XY").circle(5).extrude(20)
# Create the bend
bend = cq.Workplane("YZ").center(0, 20).circle(5).workplane(offset=10).circle(5).loft()
# Combine the straight pipe and the bend
main_pipe = pipe1.union(bend)

# Create the second pipe
pipe2 = cq.Workplane("XY").circle(5).extrude(20).translate((10, 0, 0))

# Combine both parts into a final result
result = main_pipe.union(pipe2)