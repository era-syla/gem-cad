import cadquery as cq

# Main plate dimensions
plate_width = 100
plate_height = 80
plate_thickness = 4

# Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Slot dimensions
slot_length = 35
slot_width = 8
slot_corner_r = slot_width / 2

# Create slots - these are rounded-end slots (stadium shape)
# Top-left slot
result = (result
    .cut(
        cq.Workplane("XY")
        .center(-25, 22)
        .slot2D(slot_length, slot_width, 0)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Top-right slot
result = (result
    .cut(
        cq.Workplane("XY")
        .center(25, 22)
        .slot2D(slot_length, slot_width, 90)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Bottom-left slot
result = (result
    .cut(
        cq.Workplane("XY")
        .center(-25, -22)
        .slot2D(slot_length, slot_width, 90)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Bottom-right slot
result = (result
    .cut(
        cq.Workplane("XY")
        .center(25, -22)
        .slot2D(slot_length, slot_width, 0)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Center text area - create a raised text effect or recessed
# Add a recessed "misian" text in center (approximate with a central rectangular recess)
# Central slot/cutout for text area
text_recess_w = 45
text_recess_h = 12
text_recess_depth = 1.5

result = (result
    .cut(
        cq.Workplane("XY")
        .center(0, 0)
        .rect(text_recess_w, text_recess_h)
        .extrude(text_recess_depth)
        .translate((0, 0, plate_thickness/2 - text_recess_depth))
    )
)

# Add small circular holes near the text (as seen in image - small circles near center slots)
small_hole_r = 3.5

# Left center circle
result = (result
    .cut(
        cq.Workplane("XY")
        .center(-24, 0)
        .circle(small_hole_r)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Right center circle
result = (result
    .cut(
        cq.Workplane("XY")
        .center(24, 0)
        .circle(small_hole_r)
        .extrude(plate_thickness + 2)
        .translate((0, 0, -1))
    )
)

# Add the "misian" text as embossed/debossed on the plate
try:
    text_solid = (
        cq.Workplane("XY")
        .text("misian", 8, 1.0, font="Arial", halign="center", valign="center")
        .translate((0, 0, plate_thickness/2))
    )
    result = result.union(text_solid)
except:
    pass