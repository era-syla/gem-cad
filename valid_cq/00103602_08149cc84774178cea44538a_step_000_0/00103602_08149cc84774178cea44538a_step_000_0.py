import cadquery as cq

# Parametric dimensions
total_length = 100.0       # Total width of the part
pillar_height = 60.0       # Vertical height of the end pillars
pillar_width = 15.0        # Horizontal width of the end pillars
web_height = 40.0          # Height of the central connecting web
thickness = 12.0           # Thickness (depth) of the extrusion

# Calculate position offset for pillars
# Positions are relative to center, ensuring pillars are flush with ends
pillar_x_offset = (total_length / 2.0) - (pillar_width / 2.0)

# Create the central web
# Base Workplane on XY, creating a box centered at origin
web = cq.Workplane("XY").box(total_length, web_height, thickness)

# Create the side pillars
# Push points to left and right locations, create boxes, and combine them
pillars = (
    cq.Workplane("XY")
    .pushPoints([(-pillar_x_offset, 0), (pillar_x_offset, 0)])
    .box(pillar_width, pillar_height, thickness)
)

# Union the web and pillars to form the final geometry
result = web.union(pillars)