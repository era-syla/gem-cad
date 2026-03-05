import cadquery as cq

# --- Parametric Dimensions ---
# Overall bounding box (approximate main body)
width = 100.0
depth = 60.0
thickness = 5.0

# Corner and Edge Details
front_chamfer = 10.0
right_straight_len = 15.0  # Length of the straight section on the right side
back_cut_width = 30.0      # Horizontal inset for the back-right angled cut

# Arm Details (Top-Left extension)
arm_x_offset = 15.0        # Position from the left edge
arm_width = 5.0
arm_length = 35.0          # Extension length beyond the back edge

# Side Notch Details (Left edge)
notch_dist_from_front = 35.0
notch_height = 8.0
notch_depth = 3.0

# --- Geometry Definition ---

# Define points in Counter-Clockwise order starting from the front-left chamfer
# Coordinate system: (0,0) is the theoretical bottom-left corner of the bounding box
points = [
    # Front Edge
    (front_chamfer, 0),
    (width - front_chamfer, 0),
    
    # Front-Right Corner (Chamfer)
    (width, front_chamfer),
    
    # Right Edge
    (width, front_chamfer + right_straight_len),
    
    # Back-Right Angled Cut
    (width - back_cut_width, depth),
    
    # Back Edge (Right section)
    (arm_x_offset + arm_width, depth),
    
    # Arm Extension
    (arm_x_offset + arm_width, depth + arm_length),
    (arm_x_offset, depth + arm_length),
    (arm_x_offset, depth),
    
    # Back Edge (Left section)
    (0, depth),
    
    # Left Edge with Notch
    (0, notch_dist_from_front + notch_height),
    (notch_depth, notch_dist_from_front + notch_height), # Notch In
    (notch_depth, notch_dist_from_front),                # Notch Vertical
    (0, notch_dist_from_front),                          # Notch Out
    
    # Left Edge to Start
    (0, front_chamfer)
]

# Create the Workplane, draw the polyline profile, and extrude
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)