import cadquery as cq

# Parameters
bar_length = 100
bar_width = 10
bar_thickness = 5
slot_width = 4
slot_depth = 3

panel_width = 20
panel_height = 40
panel_thickness = 5
panel_v_depth = 10

groove_widths = [panel_width * 0.8, panel_width * 0.6, panel_width * 0.4]
groove_depth = 1
apex_offset = 2

# Long slotted bar
bar = (
    cq.Workplane("XY")
    .box(bar_length, bar_width, bar_thickness)
    .faces(">Z")
    .workplane()
    .rect(bar_length + 1, slot_width)
    .cutBlind(-slot_depth)
)

# Upright V-panel
# Outline of panel in YZ plane
panel_profile = [
    (0, 0),
    (0, panel_height),
    (panel_width / 2, panel_height - panel_v_depth),
    (panel_width, panel_height),
    (panel_width, 0),
]
panel = cq.Workplane("YZ").polyline(panel_profile).close().extrude(panel_thickness)

# Carve V-shaped grooves on the front face (X=0)
for i, width in enumerate(groove_widths):
    z_ape = panel_height - panel_v_depth - i * 3
    left_y = (panel_width - width) / 2
    right_y = left_y + width
    groove_pts = [
        (left_y, z_ape),
        (panel_width / 2, z_ape - apex_offset),
        (right_y, z_ape),
    ]
    panel = (
        panel.faces("<X")
        .workplane()
        .polyline(groove_pts)
        .close()
        .cutBlind(groove_depth)
    )

# Position the panel next to the bar and align bottoms
panel = panel.translate((60, 0, -bar_thickness / 2))

# Small rectangular block
block = (
    cq.Workplane("XY")
    .box(10, 5, 5)
    .translate((70, -15, -bar_thickness / 2))
)

# Combine all parts
result = bar.union(panel).union(block)