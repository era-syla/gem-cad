import cadquery as cq

pipe_diameter = 2
pipe_length = 10
bend_radius = 1

vertical_pipe = cq.Workplane("XY").circle(pipe_diameter / 2).extrude(pipe_length)
horizontal_pipe = cq.Workplane("XY").transformed(offset=(0, 0, pipe_length)).circle(pipe_diameter / 2).extrude(pipe_length)

bend_profile = cq.Workplane("XY").moveTo(bend_radius, 0).lineTo(pipe_length - bend_radius, 0).threePointArc((pipe_length, bend_radius), (pipe_length, pipe_length - bend_radius)).lineTo(pipe_length - bend_radius, pipe_length).threePointArc((bend_radius, pipe_length), (0, pipe_length - bend_radius)).close()

bend_solid = bend_profile.revolve()

result = vertical_pipe.union(horizontal_pipe).union(bend_solid)