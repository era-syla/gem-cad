import cadquery as cq

# Parameters
plate_width = 80.0
plate_height = 50.0
thickness = 2.0
fillet_radius = 4.0

# Base Plate
# Create a rectangular plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Cutout 1: Top Horizontal Bar
# Dimensions derived from image proportions
# Width 70 (margin 5 each side), Height 10, Positioned in top half
top_cutout = (
    cq.Workplane("XY")
    .rect(70, 10)
    .translate((0, 15))
    .extrude(thickness)
)

# Cutout 2: Right Vertical Bar
# Connects to top bar to form an inverted L/7 shape
# Width 10, Height 25, Positioned on right side
right_cutout = (
    cq.Workplane("XY")
    .rect(10, 25)
    .translate((30, -2.5))
    .extrude(thickness)
)

# Cutout 3: Center 'U' Shape
# Constructed using a custom profile with arcs and lines
u_center_x = 5.0
u_center_y = -13.0
u_outer_r = 8.0
u_inner_r = 3.0
u_top_y = 5.0

u_profile = (
    cq.Workplane("XY")
    # Outer contour
    .moveTo(u_center_x - u_outer_r, u_top_y)
    .lineTo(u_center_x - u_outer_r, u_center_y)
    .threePointArc(
        (u_center_x, u_center_y - u_outer_r),
        (u_center_x + u_outer_r, u_center_y)
    )
    .lineTo(u_center_x + u_outer_r, u_top_y)
    # Inner contour (returning)
    .lineTo(u_center_x + u_inner_r, u_top_y)
    .lineTo(u_center_x + u_inner_r, u_center_y)
    .threePointArc(
        (u_center_x, u_center_y - u_inner_r),
        (u_center_x - u_inner_r, u_center_y)
    )
    .lineTo(u_center_x - u_inner_r, u_top_y)
    .close()
    .extrude(thickness)
)

# Cutout 4: Left Angled Polygon
# Irregular quadrilateral shape found on the left
# Coordinates estimated to match the angled top edge and straight sides
p1 = (-35, -15) # Bottom Left
p2 = (-15, -15) # Bottom Right
p3 = (-15, 5)   # Top Right (Vertical edge)
p4 = (-35, -5)  # Top Left (Angled top edge)

left_cutout = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(thickness)
)

# Apply all cuts to the base plate
result = result.cut(top_cutout).cut(right_cutout).cut(u_profile).cut(left_cutout)