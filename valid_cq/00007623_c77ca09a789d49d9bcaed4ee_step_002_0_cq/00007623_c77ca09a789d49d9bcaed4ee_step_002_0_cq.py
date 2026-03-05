import cadquery as cq

# Parameters for a standard servo motor (e.g., MG996R style)
# Main Body
body_width = 20.0
body_length = 40.6
body_height = 36.0  # Height excluding mounting tabs and output shaft
fillet_radius = 1.0

# Mounting Tabs
tab_thickness = 2.5
tab_width = body_width
tab_length = 54.0  # Total length including tabs
tab_offset_z = 26.5 # Height from bottom to the mounting tab plane
tab_hole_dist = 48.0 # Approximate distance between mounting holes
tab_hole_dia = 4.4 # Diameter of the U-shaped cutout
tab_inner_cutout_width = 2.5

# Output Shaft / Top Gear
top_boss_dia = 20.0
top_boss_height = 3.5  # Height above main body
output_shaft_dia = 6.0
output_shaft_height = 4.0 # Height above boss
spline_dia = 5.8
spline_teeth = 25 # Just for visual approximation

# Cable Exit
cable_exit_width = 6.0
cable_exit_depth = 4.0
cable_exit_height = 5.0
cable_pos_x = (body_length / 2) - 3.0
cable_pos_y = 0

# Bottom Cap
bottom_cap_height = 4.0

# ---------------------------------------------------------
# Modeling
# ---------------------------------------------------------

# 1. Main Body Box
# We center the body on X and Y, and Z=0 is the bottom of the main case
main_body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
    .translate((0, 0, body_height / 2))
)

# Apply fillets to vertical edges
main_body = main_body.edges("|Z").fillet(fillet_radius)

# 2. Mounting Tabs (The "ears")
# We create a plate at the specific Z height
tabs = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_thickness)
    .translate((0, 0, tab_offset_z))
)

# Create the U-shaped cutouts on the tabs
# Left Tab Cutout
left_cutout = (
    cq.Workplane("XY")
    .translate((-tab_hole_dist/2, 0, tab_offset_z))
    .circle(tab_hole_dia / 2)
    .extrude(tab_thickness * 2, both=True)
)
# Slot for left cutout to edge
left_slot = (
    cq.Workplane("XY")
    .translate((-tab_hole_dist/2 - 5, 0, tab_offset_z))
    .box(10, tab_inner_cutout_width, tab_thickness * 2)
)

# Right Tab Cutout
right_cutout = (
    cq.Workplane("XY")
    .translate((tab_hole_dist/2, 0, tab_offset_z))
    .circle(tab_hole_dia / 2)
    .extrude(tab_thickness * 2, both=True)
)
# Slot for right cutout to edge
right_slot = (
    cq.Workplane("XY")
    .translate((tab_hole_dist/2 + 5, 0, tab_offset_z))
    .box(10, tab_inner_cutout_width, tab_thickness * 2)
)

# Combine tabs and cut holes
tabs = tabs.cut(left_cutout).cut(left_slot).cut(right_cutout).cut(right_slot)

# Add reinforcing ribs to the tabs (triangular supports)
rib_thk = 1.5
rib_h = 5.0
rib_l = 4.0

def make_rib(x_offset, flip=False):
    pts = [(0, 0), (rib_l, 0), (0, rib_h)]
    if flip:
        pts = [(0, 0), (-rib_l, 0), (0, rib_h)]
        
    rib = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .extrude(rib_thk/2, both=True)
        .translate((x_offset, 0, tab_offset_z - tab_thickness/2))
    )
    return rib

# Add 4 ribs
rib1 = make_rib(body_length/2, flip=False).translate((0, body_width/4, 0))
rib2 = make_rib(body_length/2, flip=False).translate((0, -body_width/4, 0))
rib3 = make_rib(-body_length/2, flip=True).translate((0, body_width/4, 0))
rib4 = make_rib(-body_length/2, flip=True).translate((0, -body_width/4, 0))


# 3. Top Cap Features (Boss and Shaft)
# The output shaft is usually offset from center on these servos
shaft_offset_x = -body_length/2 + 10.0 # Approximate offset

top_boss = (
    cq.Workplane("XY")
    .circle(top_boss_dia / 2)
    .extrude(top_boss_height)
    .translate((shaft_offset_x, 0, body_height))
)

# Decorative detail on top boss (smaller tier)
top_boss_tier2 = (
    cq.Workplane("XY")
    .circle(top_boss_dia / 2 * 0.7)
    .extrude(top_boss_height + 1.0)
    .translate((shaft_offset_x, 0, body_height))
)

# Output Shaft (Spline approximation)
output_shaft = (
    cq.Workplane("XY")
    .circle(output_shaft_dia / 2)
    .extrude(output_shaft_height)
    .translate((shaft_offset_x, 0, body_height + top_boss_height))
)

# Add a screw hole in the shaft
shaft_hole = (
    cq.Workplane("XY")
    .circle(1.5) # M3 screw hole
    .extrude(10)
    .translate((shaft_offset_x, 0, body_height + top_boss_height - 5))
)
output_shaft = output_shaft.cut(shaft_hole)

# 4. Cable Strain Relief / Exit
cable_exit = (
    cq.Workplane("XY")
    .box(cable_exit_width, cable_exit_depth, cable_exit_height)
    .translate((body_length/2 - cable_exit_width/2, 0, body_height))
)
# Add small nubs for wires
wires = (
    cq.Workplane("XY")
    .translate((body_length/2 - cable_exit_width/2, 0, body_height + cable_exit_height))
)
w1 = wires.translate((0, -1.2, 0)).circle(0.8).extrude(1.0)
w2 = wires.translate((0, 0, 0)).circle(0.8).extrude(1.0)
w3 = wires.translate((0, 1.2, 0)).circle(0.8).extrude(1.0)
cable_exit = cable_exit.union(w1).union(w2).union(w3)


# 5. Sticker / Indentation area on the side
sticker_depth = 0.5
sticker_width = 25.0
sticker_height = 18.0
sticker_offset_z = 15.0
sticker_offset_x = -3.0

side_indent = (
    cq.Workplane("XZ")
    .rect(sticker_width, sticker_height, centered=True)
    .extrude(sticker_depth)
    .translate((sticker_offset_x, body_width/2, sticker_offset_z))
)

# 6. Bottom Cap Screws
# Just represented as small cylinders on the bottom corners
screw_dia = 2.0
screw_head_h = 1.0
screws = cq.Workplane("XY")
positions = [
    (body_length/2 - 2, body_width/2 - 2),
    (body_length/2 - 2, -body_width/2 + 2),
    (-body_length/2 + 2, body_width/2 - 2),
    (-body_length/2 + 2, -body_width/2 + 2),
]
for p in positions:
    s = (
        cq.Workplane("XY")
        .circle(screw_dia/2)
        .extrude(screw_head_h)
        .translate((p[0], p[1], -screw_head_h))
    )
    screws = screws.union(s)


# Combine everything
result = (
    main_body
    .union(tabs)
    .union(rib1).union(rib2).union(rib3).union(rib4)
    .union(top_boss)
    .union(top_boss_tier2)
    .union(output_shaft)
    .union(cable_exit)
    .cut(side_indent)
    .union(screws)
)

# Optional: Add seam lines to suggest assembly parts
# Top seam
seam_cut_top = (
    cq.Workplane("XY")
    .rect(body_length + 5, body_width + 5)
    .extrude(0.2)
    .translate((0, 0, tab_offset_z))
)

# Bottom seam
seam_cut_bottom = (
    cq.Workplane("XY")
    .rect(body_length + 5, body_width + 5)
    .extrude(0.2)
    .translate((0, 0, bottom_cap_height + 2))
)

result = result.cut(seam_cut_top).cut(seam_cut_bottom)