import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
plate_width = 100.0
plate_height = 200.0
plate_thickness = 10.0

# Top rectangular window parameters
# Distance from top edge and side edges
top_margin = 10.0
side_margin = 10.0
window_height = 40.0
window_width = plate_width - (2 * side_margin)

# Middle circular holes parameters
hole_diameter = 25.0
hole_spacing = 50.0  # Horizontal distance between centers
hole_y_pos = 0.0     # Vertical position relative to center

# Bottom square cutout parameters
square_size = 20.0
square_bottom_margin = 20.0
# Align square horizontally with the left circular hole
square_x_pos = -hole_spacing / 2

# --- Geometric Modeling ---

# 1. Create the base plate centered on the XY plane
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the top rectangular cutout
# Calculate the Y center position for the window
# (Top Edge Y) - (Margin) - (Half Window Height)
window_center_y = (plate_height / 2) - top_margin - (window_height / 2)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, window_center_y)
    .rect(window_width, window_height)
    .cutThruAll()
)

# 3. Create the two circular holes
# Using pushPoints to create multiple features at once
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, hole_y_pos), (hole_spacing / 2, hole_y_pos)])
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 4. Create the bottom square cutout
# Calculate the Y center position for the square
# (Bottom Edge Y) + (Margin) + (Half Square Size)
square_center_y = (-plate_height / 2) + square_bottom_margin + (square_size / 2)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(square_x_pos, square_center_y)
    .rect(square_size, square_size)
    .cutThruAll()
)