import cadquery as cq

# Parameter definitions
thickness = 12.0
width = 100.0          # Total width of the plate
height_top = 35.0      # Y coordinate of top edge (relative to center)
height_shoulder = 5.0  # Y coordinate where vertical side meets angled bottom
height_tip = -45.0     # Y coordinate of the bottom tip

center_bore_dia = 25.0 # Large central hole
bolt_circle_dia = 55.0 # Diameter of the 6-hole pattern
bolt_hole_dia = 5.0    # Diameter of pattern holes
side_hole_dia = 5.0    # Diameter of edge-drilled holes
side_hole_depth = 20.0 # Depth for side holes

# Define the points for the main pentagonal profile
# Counter-clockwise starting from top-left
pts = [
    (-width/2, height_top),
    (width/2, height_top),
    (width/2, height_shoulder),
    (0, height_tip),
    (-width/2, height_shoulder)
]

# Create the base solid extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Create the central large bore
result = (
    result.faces(">Z")
    .workplane()
    .hole(center_bore_dia)
)

# Create the 6-hole circular pattern
# Orientation: Holes aligned at 90 (top) and 270 (bottom) degrees
# startAngle=30 yields angles: 30, 90, 150, 210, 270, 330
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=bolt_circle_dia/2, startAngle=30, angle=360, count=6)
    .hole(bolt_hole_dia)
)

# Create side holes on the perimeter edges
# 1. Right Vertical Face
result = (
    result.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_dia, depth=side_hole_depth)
)

# 2. Left Vertical Face
result = (
    result.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_dia, depth=side_hole_depth)
)

# 3. Bottom Right Angled Face
# Calculate midpoint for reliable face selection
mid_br_x = width/4
mid_br_y = (height_shoulder + height_tip) / 2
result = (
    result.faces(cq.NearestToPointSelector((mid_br_x, mid_br_y, thickness/2)))
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_dia, depth=side_hole_depth)
)

# 4. Bottom Left Angled Face
mid_bl_x = -width/4
mid_bl_y = (height_shoulder + height_tip) / 2
result = (
    result.faces(cq.NearestToPointSelector((mid_bl_x, mid_bl_y, thickness/2)))
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_dia, depth=side_hole_depth)
)