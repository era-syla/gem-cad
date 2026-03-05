import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
width = 120.0
height = 90.0
thickness = 15.0

# Profile specifics
left_wall_height = 35.0
top_flat_width = 50.0  # Length of the horizontal segment on top

# Hole dimensions
hole_dia_large = 10.0
hole_dia_small = 4.0

# Hole positions (X, Y) relative to the bottom-left corner
pos_hole_bottom = (60.0, 20.0)
pos_hole_mid = (100.0, 35.0)
pos_hole_top = (75.0, 65.0)
pos_small_holes = [(110.0, 80.0), (110.0, 72.0)]

# --- Geometry Construction ---

# Define the points for the outer profile
# Starting from bottom-left (0,0) and going counter-clockwise
profile_pts = [
    (0, 0),                                      # Bottom-left corner
    (width, 0),                                  # Bottom-right corner
    (width, height),                             # Top-right corner
    (width - top_flat_width, height),            # Start of chamfer/slope
    (0, left_wall_height)                        # End of chamfer/slope on left wall
]

# Create the base plate
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(thickness)
)

# Cut the large mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([pos_hole_bottom, pos_hole_mid, pos_hole_top])
    .hole(hole_dia_large)
)

# Cut the small alignment holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pos_small_holes)
    .hole(hole_dia_small)
)