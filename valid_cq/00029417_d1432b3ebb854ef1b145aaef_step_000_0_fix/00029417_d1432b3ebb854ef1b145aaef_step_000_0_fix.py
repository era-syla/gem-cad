import cadquery as cq

# Parameters
thickness = 10.0       # thickness in Z
outer_dia = 30.0       # outer diameter of clamp ring
inner_dia = 20.0       # inner diameter of clamp ring
handle_length = 100.0  # length of the handle
handle_width = 12.0    # width of the handle (Y direction)
slit_width = 3.0       # width of the clamp slit
hole_dia = 5.0         # diameter of the bolt hole

# Base ring
ring = cq.Workplane("XY") \
    .circle(outer_dia/2) \
    .circle(inner_dia/2) \
    .extrude(thickness)

# Handle
handle = cq.Workplane("YZ", origin=(outer_dia/2, 0, thickness/2)) \
    .rect(handle_width, thickness) \
    .extrude(handle_length)

# Combine ring and handle
result = ring.union(handle)

# Clamp slit (cut a thin box through the ring)
slit = cq.Workplane("XY") \
    .box(outer_dia, slit_width, thickness) \
    .translate((0, 0, thickness/2))
result = result.cut(slit)

# Bolt hole (cut a small cylinder through one side of the ring)
hole = cq.Workplane("XZ", origin=(0, 0, thickness/2)) \
    .circle(hole_dia/2) \
    .extrude(outer_dia, both=True)
# Shift the hole slightly off center in Y so it only cuts one lug side (negative Y side)
hole = hole.translate((0, -((slit_width+inner_dia)/4), 0))
result = result.cut(hole)

# Final result
result