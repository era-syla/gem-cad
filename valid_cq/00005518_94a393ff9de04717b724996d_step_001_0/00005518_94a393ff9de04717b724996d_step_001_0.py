import cadquery as cq

# Parametric dimensions based on the image analysis
frame_width = 80.0
frame_height = 50.0
thickness = 5.0
border_size = 10.0
corner_boss_radius = 10.0

# 1. Create the base rectangular plate
# We start with a solid rectangle
base_plate = cq.Workplane("XY").rect(frame_width, frame_height).extrude(thickness)

# 2. Create the corner cylinder (Boss)
# The image shows a cylindrical feature on the bottom-right corner.
# Assuming origin is center, bottom-right is at (width/2, -height/2).
boss_x = frame_width / 2.0
boss_y = -frame_height / 2.0

corner_boss = (
    cq.Workplane("XY")
    .center(boss_x, boss_y)
    .circle(corner_boss_radius)
    .extrude(thickness)
)

# 3. Create the cutting tool for the inner hole
# The hole creates the frame effect
hole_width = frame_width - (2 * border_size)
hole_height = frame_height - (2 * border_size)

cutout = (
    cq.Workplane("XY")
    .rect(hole_width, hole_height)
    .extrude(thickness * 2)  # Over-extrude to ensure clean cut
    .translate((0, 0, -thickness/2))  # Center the cut vertically
)

# 4. Combine parts to form the final geometry
# Union the plate and boss, then subtract the center hole
result = base_plate.union(corner_boss).cut(cutout)