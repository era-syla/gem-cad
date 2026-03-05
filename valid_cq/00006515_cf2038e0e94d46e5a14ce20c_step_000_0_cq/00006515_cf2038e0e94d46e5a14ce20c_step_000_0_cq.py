import cadquery as cq

# -- Dimensions --
plate_length = 100.0  # X-axis dimension
plate_width = 60.0    # Y-axis dimension
plate_thickness = 10.0 # Z-axis dimension

# Hole definitions
hole_diameter = 4.0
# Coordinates relative to the center of the plate (X, Y)
# Based on visual inspection, there are two holes on the left and two on the right.
# They seem somewhat symmetric but perhaps offset.
# Let's assume a standard pattern.
# Left pair
left_x = -plate_length / 2 + 15.0  # 15mm from left edge
# Right pair
right_x = plate_length / 2 - 15.0 # 15mm from right edge

# Y spacing
y_spacing = 25.0
top_y = y_spacing / 2
bottom_y = -y_spacing / 2

# List of hole center points (x, y)
# Looking closely at the image:
# - There are two holes on the left side, aligned vertically.
# - There are two holes on the right side.
# - The right holes look slightly higher/offset compared to the left ones, 
#   or it might be perspective. Let's assume a standard rectangular pattern 
#   first as it's the most common engineering case, but looking closer, 
#   the right holes seem shifted "up" in Y relative to the left ones.
#   Actually, let's look at the "front" face.
#   Left holes: one "lower", one "middle/upper".
#   Right holes: one "lower", one "middle/upper".
#   Let's assume a symmetric 4-hole pattern for robustness unless clear asymmetry is visible.
#   Re-evaluating image: The two holes on the right look like they are at the same X coordinate.
#   The two holes on the left look like they are at the same X coordinate.
#   Let's assume symmetric placement for a standard mounting plate.

hole_locations = [
    (-30, -15),
    (-30, 15),
    (30, -15),
    (30, 15)
]

# -- Modeling --

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Cut the holes
result = result.faces(">Z").workplane().pushPoints(hole_locations).hole(hole_diameter)

# If you want to export or visualize:
# show_object(result)