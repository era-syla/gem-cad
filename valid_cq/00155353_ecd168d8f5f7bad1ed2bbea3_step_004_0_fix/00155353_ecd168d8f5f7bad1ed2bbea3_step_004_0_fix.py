import cadquery as cq

# Parameters
thickness = 3
width = 150
height = 120

window_width = 120
window_height = 80

small_rect_w = 30
small_rect_h = 20

# Base plate
result = cq.Workplane("XY").rect(width, height).extrude(thickness)

# Main window cutout with curved bottom
half_w = window_width / 2
top_y = height / 2
bot_y = top_y - window_height
arc_height = 20  # how far up the bottom arc peaks

result = (
    result
    .faces(">Z")
    .workplane()
    .polyline([
        (-half_w, top_y),
        (half_w,  top_y),
        (half_w,  bot_y)
    ])
    .threePointArc((0, bot_y + arc_height), (-half_w, bot_y))
    .close()
    .cutBlind(thickness)
)

# Small rectangular pocket at bottom left
offset_x = -width/2 + small_rect_w/2 + 10
offset_y = -height/2 + small_rect_h/2
result = (
    result
    .faces(">Z")
    .workplane(origin=(offset_x, offset_y))
    .rect(small_rect_w, small_rect_h)
    .cutBlind(thickness)
)

# Mounting/drilled holes
hole_positions = [
    (-55, -55), (-45, -55), (-35, -55),  # under small pocket
    (50, -55),                           # bottom right
    (0, 55),                             # top center
    (70, 0)                              # right center
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(3)
)

# Final result
# variable 'result' contains the final solid
