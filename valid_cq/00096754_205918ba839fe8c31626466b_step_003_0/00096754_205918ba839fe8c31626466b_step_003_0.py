import cadquery as cq

# Parametric dimensions
length = 100.0        # Total length of the part
height = 60.0         # Total height of the part
thickness = 15.0      # Extrusion thickness

chamfer_width = 30.0  # Horizontal width of the angled corner
chamfer_height = 35.0 # Vertical height of the angled corner
slot_width = 20.0     # Width of the U-shaped cutout
slot_depth = 20.0     # Depth of the U-shaped cutout
right_wall_len = 25.0 # Length of the top flat edge on the right side

# Calculate key coordinates for the profile
# Coordinates are defined counter-clockwise starting from origin (0,0)

# 1. Start at bottom-left origin
p1 = (0, 0)

# 2. Bottom right corner
p2 = (length, 0)

# 3. Top right corner
p3 = (length, height)

# 4. Start of slot (right side)
p4 = (length - right_wall_len, height)

# 5. Bottom right corner of slot
p5 = (length - right_wall_len, height - slot_depth)

# 6. Bottom left corner of slot
p6 = (length - right_wall_len - slot_width, height - slot_depth)

# 7. End of slot (left side, back to top edge)
p7 = (length - right_wall_len - slot_width, height)

# 8. Start of chamfer on top edge
p8 = (chamfer_width, height)

# 9. End of chamfer on left edge
p9 = (0, height - chamfer_height)

# Create the list of points for the polyline
pts = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

# Generate the model
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)