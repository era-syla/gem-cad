import cadquery as cq

panel_length = 80
panel_width = 60
panel_thickness = 3

ramp_length = 40
ramp_height = panel_thickness

pin_radius = 1
pin_length = panel_width + 4

bracket_width = 5
bracket_depth = 10
bracket_height = 10

# ramp
ramp = cq.Workplane("XY") \
    .polyline([(0, 0), (ramp_length, 0), (ramp_length, ramp_height), (0, 0)]) \
    .close() \
    .extrude(panel_width)

# panels
panels = cq.Workplane("XY")
for i in range(3):
    panels = panels.union(
        cq.Workplane("XY")
          .transformed(offset=(ramp_length + i * panel_length, 0, ramp_height))
          .rect(panel_length, panel_width)
          .extrude(panel_thickness)
    )

# hinge pins
pins = cq.Workplane("XY")
for j in [1, 2]:
    xj = ramp_length + j * panel_length
    pins = pins.union(
        cq.Workplane("ZX")
          .transformed(offset=(xj, panel_width/2 - pin_length/2, ramp_height + panel_thickness/2))
          .circle(pin_radius)
          .extrude(pin_length)
    )

# support brackets
brackets = cq.Workplane("XY")
for i in range(3):
    x_center = ramp_length + i * panel_length + panel_length/2
    brackets = brackets.union(
        cq.Workplane("XY")
          .transformed(offset=(x_center, bracket_depth/2, 0))
          .rect(bracket_width, bracket_depth)
          .extrude(-bracket_height)
    )

result = ramp.union(panels).union(pins).union(brackets)