import cadquery as cq

# -- Parametric Dimensions --
length = 300.0
width = 80.0
thickness = 15.0

# End Holes (larger, near the edges)
end_hole_diameter = 10.0
end_hole_margin = 20.0       # Distance from the short edge
end_hole_spacing_y = 50.0    # Distance between holes across the width

# Center Holes (smaller, in the middle)
center_hole_diameter = 6.0
center_hole_pitch_x = 60.0   # Distance between holes along length
center_hole_pitch_y = 30.0   # Distance between holes along width

# -- Model Construction --

# 1. Create the main plate body
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Define coordinates for the end holes
# Located at both ends of the plate
end_x_pos = (length / 2.0) - end_hole_margin
end_y_pos = end_hole_spacing_y / 2.0

end_hole_points = [
    (-end_x_pos, -end_y_pos),
    (-end_x_pos,  end_y_pos),
    ( end_x_pos, -end_y_pos),
    ( end_x_pos,  end_y_pos),
]

# 3. Define coordinates for the center holes
# A rectangular pattern in the center
center_x_pos = center_hole_pitch_x / 2.0
center_y_pos = center_hole_pitch_y / 2.0

center_hole_points = [
    (-center_x_pos, -center_y_pos),
    (-center_x_pos,  center_y_pos),
    ( center_x_pos, -center_y_pos),
    ( center_x_pos,  center_y_pos),
]

# 4. Cut the holes
# We select the top face (>Z) to start the drilling operations
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(end_hole_points)
    .hole(end_hole_diameter)
    .pushPoints(center_hole_points)
    .hole(center_hole_diameter)
)