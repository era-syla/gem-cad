import cadquery as cq

# Parameters
panel_w = 120.0       # Panel width
panel_h = 100.0       # Panel height
panel_t = 3.0         # Panel thickness
rod_r = 1.5           # Hinge rod radius
bracket_r = 3.5       # Bracket outer radius
bracket_h = 5.0       # Bracket height
gap = 4.0             # Gap between rod and panel
overlap = 2.0         # Overlap between bracket and panel for union

# Calculated parameters
panel_x_center = bracket_r + gap + panel_w / 2.0
bracket_len = bracket_r + gap + overlap

# Main Panel
panel = (
    cq.Workplane("XY")
    .center(panel_x_center, 0)
    .box(panel_w, panel_t, panel_h)
)

# Vertical Hinge Rod
rod = cq.Workplane("XY").cylinder(panel_h, rod_r)

# Bracket base geometry (cylinder + rectangular extension)
bracket_box_center_x = bracket_len / 2.0
bracket_base = (
    cq.Workplane("XY")
    .cylinder(bracket_h, bracket_r)
    .union(
        cq.Workplane("XY")
        .center(bracket_box_center_x, 0)
        .box(bracket_len, bracket_r * 2.0, bracket_h)
    )
)

# Top and Bottom Brackets positioned
top_bracket = bracket_base.translate((0, 0, panel_h / 2.0 - bracket_h / 2.0))
bottom_bracket = bracket_base.translate((0, 0, -panel_h / 2.0 + bracket_h / 2.0))

# Combine all parts
result = (
    panel
    .union(rod)
    .union(top_bracket)
    .union(bottom_bracket)
)