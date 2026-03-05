import cadquery as cq

# Parametric dimensions
# Base block dimensions
L_base = 220.0
W = 50.0
H = 30.0
chamfer_length = 40.0
L_top = L_base - (2 * chamfer_length)

# Hole configuration
# Center counterbored holes
cb_spacing_x = 40.0
cb_spacing_y = 24.0
cb_bore_dia = 6.0    # Through hole diameter
cb_head_dia = 10.0   # Counterbore diameter
cb_depth = 5.0

# Center alignment holes (small holes between the large ones)
center_hole_spacing = 14.0
center_hole_dia = 4.0

# End mounting holes (pairs at far ends)
end_group_spacing_x = 120.0
end_hole_spacing_y = 30.0
end_hole_dia = 5.0

# 1. Create the base trapezoidal prism
# Define the profile in the XZ plane to handle the sloped ends naturally
# (0,0) is at the center of the bottom face
pts = [
    (-L_base / 2, 0),
    (L_base / 2, 0),
    (L_top / 2, H),
    (-L_top / 2, H)
]

# Extrude along Y axis, centered
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(W / 2.0, both=True)
)

# 2. Add features to the top face
top_plane = result.faces(">Z").workplane()

# A. Central Counterbored Holes (4x)
result = (
    top_plane
    .rect(cb_spacing_x, cb_spacing_y, forConstruction=True)
    .vertices()
    .cboreHole(cb_bore_dia, cb_head_dia, cb_depth)
)

# B. Central Alignment Holes (2x)
# Located on the midline (y=0)
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (center_hole_spacing / 2, 0),
        (-center_hole_spacing / 2, 0)
    ])
    .hole(center_hole_dia)
)

# C. End Mounting Holes (4x)
# Two pairs located near the ends of the top surface
end_points = [
    (end_group_spacing_x / 2, end_hole_spacing_y / 2),
    (end_group_spacing_x / 2, -end_hole_spacing_y / 2),
    (-end_group_spacing_x / 2, end_hole_spacing_y / 2),
    (-end_group_spacing_x / 2, -end_hole_spacing_y / 2)
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(end_points)
    .hole(end_hole_dia)
)