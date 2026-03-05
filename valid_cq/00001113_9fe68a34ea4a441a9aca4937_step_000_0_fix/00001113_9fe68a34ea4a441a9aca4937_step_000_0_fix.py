import cadquery as cq

# Parameters
body_length = 150.0
body_width = 75.0
body_thickness = 8.0
corner_radius = 5.0

screen_margin = 4.0
screen_depth = 1.0

home_button_radius = 8.0
home_button_depth = 0.5
home_button_offset = 15.0

speaker_width = 18.0
speaker_height = 3.0
speaker_depth = 1.0
speaker_offset = 8.0

camera_radius = 1.5
camera_depth = 1.0
camera_offset = 8.0
camera_x_offset = 10.0

# Main body with filleted vertical edges
result = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Screen recess
result = (
    result.faces(">Z")
    .workplane()
    .rect(body_length - 2 * screen_margin, body_width - 2 * screen_margin)
    .cutBlind(-screen_depth)
)

# Home button cutout (bottom side)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, -body_length / 2 + home_button_offset)
    .circle(home_button_radius)
    .cutBlind(-home_button_depth)
)

# Speaker slot (bottom side)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, -body_length / 2 + speaker_offset)
    .rect(speaker_width, speaker_height)
    .cutBlind(-speaker_depth)
)

# Camera hole (bottom side, off-center)
result = (
    result.faces(">Z")
    .workplane()
    .center(-camera_x_offset, -body_length / 2 + camera_offset)
    .circle(camera_radius)
    .cutBlind(-camera_depth)
)
