import cadquery as cq

# Parameters
length = 100.0
width = 60.0
thickness = 20.0
chamfer_size = 10.0

# Right rectangular slot dimensions
slot_right_width = 15.0
slot_right_depth = 30.0

# Left trapezoidal cutout dimensions
slot_left_opening_width = 30.0
slot_left_base_width = 14.0
slot_left_depth = 25.0

# Define points for the profile counter-clockwise, starting from top edge
points = [
    # Top Edge
    (length/2 - chamfer_size, width/2),
    (-length/2 + chamfer_size, width/2),
    
    # Top-Left Corner Chamfer
    (-length/2, width/2 - chamfer_size),
    
    # Left Edge (Upper)
    (-length/2, slot_left_opening_width/2),
    
    # Left Slot (Trapezoidal)
    (-length/2 + slot_left_depth, slot_left_base_width/2),   # Inner top
    (-length/2 + slot_left_depth, -slot_left_base_width/2),  # Inner bottom
    
    # Left Edge (Lower)
    (-length/2, -slot_left_opening_width/2),
    (-length/2, -width/2 + chamfer_size),
    
    # Bottom-Left Corner Chamfer
    (-length/2 + chamfer_size, -width/2),
    
    # Bottom Edge
    (length/2 - chamfer_size, -width/2),
    
    # Bottom-Right Corner Chamfer
    (length/2, -width/2 + chamfer_size),
    
    # Right Edge (Lower)
    (length/2, -slot_right_width/2),
    
    # Right Slot (Rectangular)
    (length/2 - slot_right_depth, -slot_right_width/2), # Inner bottom
    (length/2 - slot_right_depth, slot_right_width/2),  # Inner top
    
    # Right Edge (Upper)
    (length/2, slot_right_width/2),
    
    # Top-Right Corner Chamfer End Point
    (length/2, width/2 - chamfer_size)
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)