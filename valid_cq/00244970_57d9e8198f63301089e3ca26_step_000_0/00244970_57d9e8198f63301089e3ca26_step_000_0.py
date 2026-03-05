import cadquery as cq

# --- Parameters ---
length = 320.0        # Total length of the channel
width = 40.0          # External width
height = 40.0         # External height
thickness = 2.5       # Material thickness
hole_pitch = 16.0     # Spacing between hole centers
large_hole_diam = 8.0 # Diameter of the center row holes
small_hole_diam = 4.0 # Diameter of the top/bottom row holes
row_offset = 12.0     # Distance from center row to outer rows

# --- Geometry Generation ---

# 1. Create the U-Channel Profile
# We sketch on the YZ plane (Width x Height) and extrude along X (Length)
# Coordinates defined clockwise from bottom-left
pts = [
    (0, 0),                       # Bottom-left outer
    (width, 0),                   # Bottom-right outer
    (width, height),              # Top-right outer
    (width - thickness, height),  # Top-right inner
    (width - thickness, thickness), # Inner corner right
    (thickness, thickness),       # Inner corner left
    (thickness, height),          # Top-left inner
    (0, height)                   # Top-left outer
]

channel = cq.Workplane("YZ").polyline(pts).close().extrude(length)

# 2. Calculate Hole Coordinates
# We generate lists of (x, y) coordinates for the 2D workplanes.
# The pattern is centered along the length.
num_holes = int(length / hole_pitch)
pattern_span = (num_holes - 1) * hole_pitch
start_x = (length - pattern_span) / 2.0

# Lists to store 2D coordinates for the faces
# For Side Faces: Y-local maps to Z-global (Height)
# For Bottom Face: Y-local maps to Y-global (Width)
center_pts = []
outer_pts_1 = [] # Top row (side) or Right row (bottom)
outer_pts_2 = [] # Bottom row (side) or Left row (bottom)

for i in range(num_holes):
    x_pos = start_x + i * hole_pitch
    
    # Coordinates assume workplane origin aligns with global origin projected
    # Center lines are at height/2 (for sides) or width/2 (for bottom)
    center_val = height / 2.0 # Assuming width == height for coordinate logic simplicity here
    
    center_pts.append((x_pos, center_val))
    outer_pts_1.append((x_pos, center_val + row_offset))
    outer_pts_2.append((x_pos, center_val - row_offset))

# 3. Apply Cuts to Faces

# Define the list of faces to apply the pattern to
# <Y: Left Side Wall
# >Y: Right Side Wall
# <Z: Bottom Face
faces_to_drill = ["<Y", ">Y", "<Z"]

result = channel

for face in faces_to_drill:
    # Select face and create workplane. 
    # Note: For <Z, center_val should logically be width/2, for side faces height/2.
    # Since width=height in parameters, we use the same lists. 
    # If width != height, specific lists would be needed for the bottom face.
    
    # Adjust center value if dimensions differ (making it robust)
    current_dim = width if face == "<Z" else height
    
    # Regenerate points for this specific face dimension
    f_center_pts = []
    f_outer_1_pts = []
    f_outer_2_pts = []
    for i in range(num_holes):
        x = start_x + i * hole_pitch
        mid = current_dim / 2.0
        f_center_pts.append((x, mid))
        f_outer_1_pts.append((x, mid + row_offset))
        f_outer_2_pts.append((x, mid - row_offset))
        
    result = (result
              .faces(face).workplane()
              # Cut Center Row (Large)
              .pushPoints(f_center_pts)
              .circle(large_hole_diam / 2.0)
              .cutBlind(-thickness * 3) # Cut through wall
              # Cut Outer Row 1 (Small)
              .pushPoints(f_outer_1_pts)
              .circle(small_hole_diam / 2.0)
              .cutBlind(-thickness * 3)
              # Cut Outer Row 2 (Small)
              .pushPoints(f_outer_2_pts)
              .circle(small_hole_diam / 2.0)
              .cutBlind(-thickness * 3)
              )