import cadquery as cq

# Parametric dimensions
height_total = 40.0
height_bottom_section = 15.0  # The step seems to be around 1/3 to 1/2 of total height
width = 20.0
depth = 20.0

# Define the coordinates for the polygon profile
# Looking at the top face, it's a pentagon or a clipped rectangle.
# Let's approximate it as a rectangle with one corner chamfered significantly.
# (0,0) will be the center.
# Points order: Top-Left, Top-Right (chamfer start), Right-Side (chamfer end), Bottom-Right, Bottom-Left
# Let's adjust coordinates to make it symmetric around Y axis but offset on X to match the pointy look
# Actually, looking closer, it looks like a house shape (pentagon).
# Base is a rectangle, top is a triangle. Or simply a 5-sided polygon.
# Let's define points relative to a center.

pts = [
    (-width/2, -depth/2),  # Bottom-Left
    (width/2, -depth/2),   # Bottom-Right
    (width/2, 0),          # Right-Middle (start of angle)
    (0, depth/2),          # Top Tip
    (-width/2, 0)          # Left-Middle (start of angle)
]

# Create the main top body (the larger section)
top_body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height_total - height_bottom_section)
    .translate((0, 0, height_bottom_section))
)

# Create the bottom body (the smaller, stepped-in section)
# It appears to be the same shape but scaled down or offset inwards.
# Based on the vertical edges aligning perfectly, it is likely just the same profile
# extruded downwards, but visual inspection suggests a slight inset or step.
# Wait, looking very closely at the image:
# The vertical edges *don't* align perfectly. There is a "shelf" or overhang.
# The top part is wider than the bottom part.
# Let's create a scale factor for the bottom part.

scale_factor = 0.7
pts_bottom = [(x * scale_factor, y * scale_factor) for x, y in pts]

bottom_body = (
    cq.Workplane("XY")
    .polyline(pts_bottom)
    .close()
    .extrude(height_bottom_section)
)

# However, looking at the provided image again very carefully:
# The bottom section aligns with the top section on the *back* or *center*, 
# but simply looks smaller.
# Let's try a simpler approach often seen in these generated datasets:
# It's a single profile extruded, but wait, there is a clear step.
# Let's stick to the two-part construction.
# To ensure the "back" or specific edges align if necessary, we could offset,
# but a centered scaling is the most robust parametric assumption without multiple views.

# Refined Plan:
# 1. Define the pentagon shape.
# 2. Extrude the bottom part (smaller).
# 3. Extrude the top part (larger) on top of it.

# Dimensions
top_width = 15.0
top_depth = 20.0 # From tip to flat bottom edge
tip_y = top_depth / 2
base_y = -top_depth / 2
side_x = top_width / 2

# Top profile points (Pentagon/House shape)
top_pts = [
    (-side_x, base_y),  # Bottom Left
    (side_x, base_y),   # Bottom Right
    (side_x, 0),        # Right shoulder
    (0, tip_y),         # Top Tip
    (-side_x, 0)        # Left shoulder
]

# Bottom profile (smaller version)
offset = 2.0 # The step size
bottom_pts = [
    (-side_x + offset, base_y + offset),
    (side_x - offset, base_y + offset),
    (side_x - offset, 0), 
    (0, tip_y - offset), 
    (-side_x + offset, 0)
]

# Create the top solid
top_part = (
    cq.Workplane("XY")
    .workplane(offset=height_bottom_section)
    .polyline(top_pts)
    .close()
    .extrude(height_total - height_bottom_section)
)

# Create the bottom solid
# Note: simple scaling creates a centered smaller shape. 
# Looking at the image, the step looks uniform around the perimeter.
bottom_part = (
    cq.Workplane("XY")
    .polyline(bottom_pts)
    .close()
    .extrude(height_bottom_section)
)

result = top_part.union(bottom_part)