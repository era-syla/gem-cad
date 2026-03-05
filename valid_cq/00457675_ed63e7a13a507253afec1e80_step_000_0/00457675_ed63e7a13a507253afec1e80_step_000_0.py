import cadquery as cq

# Parametric dimensions
seat_width = 45.0
seat_depth = 45.0
seat_thickness = 4.0
leg_width = 4.0
leg_height = 45.0
back_height = 55.0
back_thickness = 4.0
back_angle = 8.0  # Tilt angle in degrees

# 1. Create the four legs
# We sketch a construction rectangle to locate the centers of the legs at the corners
legs = (
    cq.Workplane("XY")
    .rect(seat_width - leg_width, seat_depth - leg_width, forConstruction=True)
    .vertices()
    .rect(leg_width, leg_width)
    .extrude(leg_height)
)

# 2. Create the seat base
# Positioned on top of the legs
seat = (
    cq.Workplane("XY")
    .workplane(offset=leg_height)
    .box(seat_width, seat_depth, seat_thickness, centered=(True, True, False))
)

# 3. Create the backrest
# Positioned at the rear edge of the seat, tilted backwards
# We calculate the position so the back face of the backrest aligns with the back of the seat
pivot_y = (seat_depth / 2.0) - (back_thickness / 2.0)
pivot_z = leg_height + seat_thickness

backrest = (
    cq.Workplane("XY")
    .transformed(
        offset=cq.Vector(0, pivot_y, pivot_z),
        rotate=cq.Vector(-back_angle, 0, 0)
    )
    .box(seat_width, back_thickness, back_height, centered=(True, True, False))
)

# Union all parts to create the final model
result = legs.union(seat).union(backrest)