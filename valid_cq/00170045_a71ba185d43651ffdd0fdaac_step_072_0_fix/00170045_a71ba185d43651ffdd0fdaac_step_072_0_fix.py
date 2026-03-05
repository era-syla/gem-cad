import cadquery as cq

# Parameters
frame_outer_x = 100.0
frame_outer_y = 80.0
frame_thickness = 4.0

boss_diameter = 8.0
boss_height = 3.0
boss_hole_diameter = 3.0

bracket_width = frame_outer_x + 2 * frame_thickness
bracket_height = 12.0
bracket_thickness = frame_thickness
bracket_hole_diameter = 5.0
bracket_hole_offset = 15.0

# Build the rectangular frame as a hollow ring
result = (
    cq.Workplane("XY")
    .rect(frame_outer_x, frame_outer_y)
    .rect(frame_outer_x - 2 * frame_thickness, frame_outer_y - 2 * frame_thickness)
    .extrude(frame_thickness)
)

# Add corner bosses
corner_x = frame_outer_x / 2 - frame_thickness / 2
corner_y = frame_outer_y / 2 - frame_thickness / 2
corner_points = [
    (-corner_x, -corner_y),
    (-corner_x,  corner_y),
    ( corner_x,  corner_y),
    ( corner_x, -corner_y),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(corner_points)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Drill holes through the bosses
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(corner_points)
    .hole(boss_hole_diameter)
)

# Add the vertical back bracket on the rear edge of the frame
result = (
    result
    .faces("<Y")
    .workplane()
    .rect(bracket_width, bracket_height)
    .extrude(bracket_thickness)
)

# Drill mounting holes in the back bracket
hole_x = bracket_width / 2 - bracket_hole_offset
bracket_hole_positions = [(-hole_x, 0), (hole_x, 0)]
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(bracket_hole_positions)
    .hole(bracket_hole_diameter)
)