import cadquery as cq

# Parametric dimensions
plate_width = 50.0
plate_height = 50.0
plate_thickness = 4.0

small_hole_dia = 6.0
small_hole_x = -12.0
small_hole_y = 12.0

large_hole_dia = 12.0
large_hole_x = 12.0
large_hole_y = 12.0

notch_width = 10.0
notch_height = 10.0
notch_x = plate_width / 2.0
notch_y = -10.0

rod_dia = 8.0
rod_length = 90.0

disc_dia1 = 40.0
disc_thickness1 = 2.0
disc_dia2 = 38.0
disc_thickness2 = 1.0

center_indent_dia = 8.0
center_indent_depth = 1.0

# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Add holes and notch to plate
result = (
    result.faces(">Z").workplane()
    # Small hole
    .pushPoints([(small_hole_x, small_hole_y)])
    .hole(small_hole_dia)
    # Large hole
    .pushPoints([(large_hole_x, large_hole_y)])
    .hole(large_hole_dia)
    # Side notch (rectangle centered on the right edge)
    .pushPoints([(notch_x, notch_y)])
    .rect(notch_width * 2, notch_height) # Width is doubled to ensure complete boundary cut
    .cutBlind(-plate_thickness)
)

# 3. Add connecting rod
result = (
    result.faces(">Z").workplane()
    .circle(rod_dia / 2.0)
    .extrude(rod_length)
)

# 4. Add end disc (first wider layer)
result = (
    result.faces(">Z").workplane()
    .circle(disc_dia1 / 2.0)
    .extrude(disc_thickness1)
)

# 5. Add end disc (second stepped layer for the edge detail)
result = (
    result.faces(">Z").workplane()
    .circle(disc_dia2 / 2.0)
    .extrude(disc_thickness2)
)

# 6. Add center circular indentation on the outer face
result = (
    result.faces(">Z").workplane()
    .circle(center_indent_dia / 2.0)
    .cutBlind(-center_indent_depth)
)