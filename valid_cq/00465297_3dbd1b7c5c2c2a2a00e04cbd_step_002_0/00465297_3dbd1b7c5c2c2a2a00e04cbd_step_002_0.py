import cadquery as cq

# Dimensions
height = 70.0
top_width = 180.0
bottom_width = 20.0
thickness = 30.0
wall_thickness = 15.0
rib_thickness = 15.0

# Calculate profile coordinates
x_top = top_width / 2.0
x_bot = bottom_width / 2.0

# Outer Trapezoid Profile Points
# Defined Counter-Clockwise starting from top-right
pts_outer = [
    (x_top, height),    
    (-x_top, height),   
    (-x_bot, 0),        
    (x_bot, 0)          
]

# Inner Cutout Calculation
# Calculate the slope of the side wall to create parallel offsets
dy = height
dx = x_top - x_bot
slope = dy / dx

# Right Cutout (Right-angled triangle)
# Inner vertical edge X position
x_inner = rib_thickness / 2.0
# Top horizontal edge Y position
y_top_hole = height - wall_thickness

# Calculate outer top vertex to maintain wall thickness
# We calculate the X position on the outer wall at y_top_hole, then shift inward
x_outer_at_y = x_bot + (y_top_hole / slope)
# Horizontal offset to maintain approximate perpendicular wall thickness
# Heuristic offset: wall_thickness * 1.5 accounts for the angle
x_hole_outer = x_outer_at_y - (wall_thickness * 1.5)

# Calculate bottom vertex Y position
# Defined by the intersection of the inner vertical line and a line parallel to the outer edge
# passing through the hole's outer top vertex
y_hole_bot = y_top_hole - slope * (x_hole_outer - x_inner)

# Ensure the bottom of the hole doesn't go below the bottom wall thickness
if y_hole_bot < wall_thickness:
    y_hole_bot = wall_thickness

pts_hole_right = [
    (x_inner, y_top_hole),
    (x_hole_outer, y_top_hole),
    (x_inner, y_hole_bot)
]

# Left Cutout (Mirror of Right)
pts_hole_left = [(-x, y) for x, y in pts_hole_right]

# Create the 3D Model
result = (
    cq.Workplane("XY")
    .polyline(pts_outer).close()
    .polyline(pts_hole_right).close()
    .polyline(pts_hole_left).close()
    .extrude(thickness)
)