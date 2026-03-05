import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
length = 150.0          # Horizontal length from back wall to front tip
height_back = 100.0     # Height of the vertical back edge
height_front = 15.0     # Height of the vertical front tip
thickness = 3.0         # Sheet metal thickness
chamfer_bottom = 15.0   # Size of the chamfer at the bottom-rear corner

# Hook (connection tab) dimensions
num_hooks = 3
hook_pitch = 30.0       # Center-to-center vertical spacing
hook_top_margin = 5.0   # Distance from top edge to top of first hook

hook_depth = 10.0       # Distance the hooks protrude backwards (negative X)
hook_height = 12.0      # Total vertical length of the hook tab
notch_height = 6.0      # Height of the locking notch slot
tooth_width = 5.0       # Width of the solid material behind the notch

# --- Geometry Construction ---

# Calculate derived dimensions for the hook profile
# x_outer is the furthest point back
x_outer = -hook_depth
# x_inner is the depth of the notch cut
x_inner = -(hook_depth - tooth_width)

# Define the list of 2D coordinates for the profile
points = []

# 1. Start at Bottom-Front corner
points.append((length, 0))

# 2. Go to Top-Front corner
points.append((length, height_front))

# 3. Go to Top-Back corner (on the wall line)
points.append((0, height_back))

# 4. Create the hooks along the back edge
#    We iterate from top to bottom
for i in range(num_hooks):
    # Calculate Y positions for the current hook
    y_start = height_back - hook_top_margin - (i * hook_pitch)
    y_end = y_start - hook_height
    y_notch_top = y_end + notch_height
    
    # Add points to trace the hook shape
    
    # Point on the wall line at start of hook
    points.append((0, y_start))
    
    # Go Outward (Backwards)
    points.append((x_outer, y_start))
    
    # Go Down
    points.append((x_outer, y_end))
    
    # Go Inward (into the notch)
    points.append((x_inner, y_end))
    
    # Go Up (inside the notch)
    points.append((x_inner, y_notch_top))
    
    # Return to the wall line
    points.append((0, y_notch_top))

# 5. Create the bottom-rear chamfer
#    Go down along the wall to the chamfer start
points.append((0, chamfer_bottom))
#    Go to the bottom edge chamfer end
points.append((chamfer_bottom, 0))

# --- Solid Generation ---
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)