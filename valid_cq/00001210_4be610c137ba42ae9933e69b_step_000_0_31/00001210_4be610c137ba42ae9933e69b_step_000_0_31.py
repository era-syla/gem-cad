import cadquery as cq

# Parameters defining the profile shape
length_total = 100.0
length_straight_part = 35.0

# Y-coordinates for the top edge (straight slope)
y_top_left = 35.0
y_top_right = 18.0

# Y-coordinates for the bottom edge
y_bot_left = 15.0
y_bot_seam = 5.0   # Point where the straight bottom meets the curved bottom
y_bot_right = 10.0

# Intermediate point to define the curvature of the bottom arc
arc_mid_x = 70.0
arc_mid_y = 2.0

# Extrusion depth (thickness of the part)
depth = 20.0

# Create the 2D profile and extrude it into a 3D solid
result = (
    cq.Workplane("XZ")
    # Start at top-left corner
    .moveTo(0, y_top_left)
    
    # Top straight edge sloping down
    .lineTo(length_total, y_top_right)
    
    # Right vertical edge
    .lineTo(length_total, y_bot_right)
    
    # Bottom curved edge (right part, bulging downwards)
    .threePointArc((arc_mid_x, arc_mid_y), (length_straight_part, y_bot_seam))
    
    # Bottom straight edge (left part)
    .lineTo(0, y_bot_left)
    
    # Close the profile (creates the left vertical edge)
    .close()
    
    # Extrude the profile into 3D
    .extrude(depth)
)