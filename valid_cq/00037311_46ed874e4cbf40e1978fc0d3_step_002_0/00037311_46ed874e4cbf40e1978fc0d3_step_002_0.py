import cadquery as cq

# Parameters for the geometry
height = 90.0           # Total height of the vertical left edge
width = 80.0            # Total width from left edge to the tip
thickness = 4.0         # Thickness of the plate

# Top edge step parameters
top_step_x = 25.0       # Distance from left corner to the step
top_step_drop = 8.0     # Vertical drop of the step

# Jagged diagonal edge parameters
num_notches = 3         # Number of notches along the diagonal
notch_width = 5.0       # Horizontal depth of the cutouts
notch_height = 5.0      # Vertical height of the cutouts

# -- Geometry Calculation --

# Initialize points list starting from Origin (Bottom-Left)
points = [(0, 0)]

# 1. Vertical Up to Top-Left
points.append((0, height))

# 2. Top Edge with Step
points.append((top_step_x, height))
points.append((top_step_x, height - top_step_drop))
points.append((width, height - top_step_drop))  # The Tip

# 3. Jagged Diagonal (Calculating path from Tip back to Origin)
# The path consists of alternating slanted segments and stepped notches.
# We calculate the dimensions of the slant segments to ensure the path ends exactly at (0,0).

# Total dimensions to cover
total_dy = height - top_step_drop
total_dx = width

# Available dimensions for slants after subtracting notches
# Note: Traversing from Tip to Origin means moving Left (-X) and Down (-Y)
slant_total_dx = total_dx - (num_notches * notch_width)
slant_total_dy = total_dy - (num_notches * notch_height)

# Dimensions per slant segment
# There are (num_notches + 1) slant segments
dx_slant = slant_total_dx / (num_notches + 1)
dy_slant = slant_total_dy / (num_notches + 1)

# Current position tracker
curr_x = width
curr_y = height - top_step_drop

for _ in range(num_notches):
    # Slant Segment
    curr_x -= dx_slant
    curr_y -= dy_slant
    points.append((curr_x, curr_y))
    
    # Notch Horizontal Step (Inwards/Left)
    curr_x -= notch_width
    points.append((curr_x, curr_y))
    
    # Notch Vertical Step (Down)
    curr_y -= notch_height
    points.append((curr_x, curr_y))

# Final Slant Segment to Origin
points.append((0, 0))

# -- Model Creation --
result = cq.Workplane("XY").polyline(points).close().extrude(thickness)