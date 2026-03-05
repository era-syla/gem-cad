import cadquery as cq

# Define parametric variables for the various components
# Dimensions are estimated based on visual proportions from the image

# 1. Square Plate
plate_sq_side = 20.0
plate_sq_thick = 2.0
plate_sq_fillet = 2.0

# 2. Rectangular Plates
plate_rect_width = 40.0
plate_rect_depth = 20.0
plate_rect_thick = 2.0
plate_rect_fillet = 2.0
hole_dia = 4.0

# 3. Tall Tube
tube_outer_dia = 8.0
tube_inner_dia = 6.0
tube_height = 30.0

# 4. Short Tube
short_tube_outer_dia = 8.0
short_tube_inner_dia = 6.0
short_tube_height = 15.0

# 5. Long Rod/Shaft
rod_dia = 3.0
rod_height = 50.0

# 6. Thin Pin
pin_dia = 2.0
pin_height = 25.0

# 7. Circular Discs
disc_dia = 8.0
disc_thick = 2.0
thick_disc_thick = 4.0

# 8. Nut/Hex piece
hex_width = 8.0 # Across flats
hex_height = 3.0
hex_hole = 4.0

# 9. Bolt head / Cap
cap_dia = 10.0
cap_height = 5.0
cap_chamfer = 1.0

# 10. Elongated/Oval piece
oval_length = 20.0
oval_width = 10.0
oval_height = 4.0

# --- Geometry Creation ---

# 1. Square Plate (Bottom Left)
square_plate = (
    cq.Workplane("XY")
    .box(plate_sq_side, plate_sq_side, plate_sq_thick)
    .edges("|Z")
    .fillet(plate_sq_fillet)
    .translate((-40, -20, 0))
)

# 2. Tall Tube (Top Left)
tall_tube = (
    cq.Workplane("XY")
    .circle(tube_outer_dia / 2)
    .circle(tube_inner_dia / 2)
    .extrude(tube_height)
    .translate((-20, 10, 0))
)

# 3. Small Disc (Bottom Left)
small_disc = (
    cq.Workplane("XY")
    .circle(disc_dia / 2)
    .extrude(disc_thick)
    .translate((-25, -35, 0))
)

# 4. Thicker Disc (Bottom Middle)
thick_disc = (
    cq.Workplane("XY")
    .circle(disc_dia / 2)
    .extrude(thick_disc_thick)
    .translate((-5, -45, 0))
)

# 5. Long Rod (Middle)
long_rod = (
    cq.Workplane("XY")
    .circle(rod_dia / 2)
    .extrude(rod_height)
    .translate((0, 0, 0))
)

# 6. Short Tube (Middle)
short_tube = (
    cq.Workplane("XY")
    .circle(short_tube_outer_dia / 2)
    .circle(short_tube_inner_dia / 2)
    .extrude(short_tube_height)
    .translate((10, -5, 0))
)

# 7. Rectangular Plate with 1 Hole (Middle)
rect_plate_1 = (
    cq.Workplane("XY")
    .box(plate_rect_width, plate_rect_depth, plate_rect_thick)
    .edges("|Z")
    .fillet(plate_rect_fillet)
    .faces(">Z").workplane()
    .pushPoints([(-12, 0)]) # Hole offset
    .hole(hole_dia)
    .translate((25, -10, 0))
)

# 8. Rectangular Plate with 2 Holes (Top Right)
rect_plate_2 = (
    cq.Workplane("XY")
    .box(plate_rect_width, plate_rect_depth, plate_rect_thick)
    .edges("|Z")
    .fillet(plate_rect_fillet)
    .faces(">Z").workplane()
    .pushPoints([(-12, 0), (12, 0)]) # Two holes
    .hole(hole_dia)
    .translate((45, 15, 0))
)

# 9. Hex Nut (Middle Small)
hex_nut = (
    cq.Workplane("XY")
    .polygon(6, hex_width)
    .extrude(hex_height)
    .faces(">Z").workplane()
    .hole(hex_hole)
    .translate((20, -25, 0))
)

# 10. Thin Pin (Right of Rect Plate)
thin_pin = (
    cq.Workplane("XY")
    .circle(pin_dia / 2)
    .extrude(pin_height)
    .translate((40, -20, 0))
)

# 11. Oval/Rounded Cap (Bottom Center)
oval_part = (
    cq.Workplane("XY")
    .rect(oval_length - oval_width, oval_width) # Inner rectangle
    .extrude(oval_height)
    .edges("|Z")
    .fillet(oval_width / 2 - 0.01) # Full round ends
    .edges(">Z")
    .chamfer(0.5)
    .translate((20, -60, 0))
)

# 12. Hex Cap/Bolt Head (Far Right)
hex_cap = (
    cq.Workplane("XY")
    .polygon(6, hex_width)
    .extrude(hex_height * 2)
    .edges(">Z")
    .chamfer(0.5)
    .translate((70, -10, 0))
)

# Combine all parts into a single assembly result
result = (
    square_plate
    .union(tall_tube)
    .union(small_disc)
    .union(thick_disc)
    .union(long_rod)
    .union(short_tube)
    .union(rect_plate_1)
    .union(rect_plate_2)
    .union(hex_nut)
    .union(thin_pin)
    .union(oval_part)
    .union(hex_cap)
)