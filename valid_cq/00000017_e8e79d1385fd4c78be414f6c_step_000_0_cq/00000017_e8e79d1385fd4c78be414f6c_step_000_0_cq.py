import cadquery as cq

# Parametric dimensions
plate_width = 80.0   # Total width of the plate
plate_length = 80.0  # Total length of the plate
plate_thickness = 2.0 # Thickness of the plate
grid_count_x = 8     # Number of grid divisions along X
grid_count_y = 8     # Number of grid divisions along Y
groove_depth = 0.2   # Depth of the grid lines
groove_width = 0.2   # Width of the grid lines (approximate for visual representation)

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add grid lines to the top surface
# Calculate step sizes
step_x = plate_length / grid_count_x
step_y = plate_width / grid_count_y

# Create vertical cuts (along Y axis)
for i in range(1, grid_count_x):
    x_pos = -plate_length/2 + i * step_x
    result = result.faces(">Z").workplane().moveTo(x_pos, 0).rect(groove_width, plate_width).cutBlind(-groove_depth)

# Create horizontal cuts (along X axis)
for i in range(1, grid_count_y):
    y_pos = -plate_width/2 + i * step_y
    result = result.faces(">Z").workplane().moveTo(0, y_pos).rect(plate_length, groove_width).cutBlind(-groove_depth)

# Note: The image shows a simple plate with grid lines. 
# Depending on the rendering or manufacturing intent, these could be shallow grooves 
# or just separate bodies/faces. The code above simulates the visual appearance with shallow cuts.
# Alternatively, if this is meant to be a tiled floor, one might create an array of boxes.
# Given the "single object" look, a scored plate is the most likely geometric interpretation.