import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
height = 120.0
base_width = 60.0
top_width = 30.0
thickness = 20.0
side_curvature = 5.0  # Controls the convexity (bulge) of the sides

# Define key points for the profile sketch on the XZ plane
# The shape is centered around the Z axis horizontally
x_base = base_width / 2.0
x_top = top_width / 2.0

pt_base_left = (-x_base, 0)
pt_base_right = (x_base, 0)
pt_top_right = (x_top, height)
pt_top_left = (-x_top, height)

# Calculate mid-points for the 3-point arcs
# The mid-point X coordinate is the average linear width plus the curvature offset
mid_y = height / 2.0
mid_x = ((base_width + top_width) / 4.0) + side_curvature

pt_mid_right = (mid_x, mid_y)
pt_mid_left = (-mid_x, mid_y)

# Create the solid geometry
result = (
    cq.Workplane("XZ")
    .moveTo(*pt_base_left)
    .lineTo(*pt_base_right)  # Bottom straight edge
    .threePointArc(pt_mid_right, pt_top_right)  # Right convex curve
    .lineTo(*pt_top_left)    # Top straight edge
    .threePointArc(pt_mid_left, pt_base_left)   # Left convex curve
    .close()
    .extrude(thickness)
)