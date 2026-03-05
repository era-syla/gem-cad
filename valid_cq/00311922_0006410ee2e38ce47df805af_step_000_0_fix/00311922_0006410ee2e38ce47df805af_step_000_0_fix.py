import cadquery as cq

# Parameters
thickness = 4
beam_width = 6
end_radius = 8
length = 120
hole_dia = 4
hex_dia = 6
hex_height = 2
spacing = 12

# Build the base geometry by extruding end circles and connecting rectangle
wp = cq.Workplane("XY")
circle_left = wp.circle(end_radius).extrude(thickness)
circle_right = wp.center(length, 0).circle(end_radius).extrude(thickness)
rect_mid = wp.center(length/2, 0).rect(length - 2*end_radius, beam_width).extrude(thickness)

result = circle_left.union(circle_right).union(rect_mid)

# Cut holes: one at left end, three at right end
hole_x_positions = [0] + [length - end_radius - i * spacing for i in range(3)]
for x in hole_x_positions:
    result = result.faces(">Z").workplane().center(x, 0).circle(hole_dia/2).cutThruAll()

# Add a hexagonal boss at the center
result = result.faces(">Z").workplane().center(length/2, 0).polygon(6, hex_dia).extrude(hex_height)