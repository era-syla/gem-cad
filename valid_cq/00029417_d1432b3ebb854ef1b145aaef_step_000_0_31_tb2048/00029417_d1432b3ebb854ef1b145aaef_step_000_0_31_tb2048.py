import cadquery as cq

# Parameters
thickness = 15.0
collar_r_out = 16.0
collar_r_in = 11.0
arm_width = 14.0
arm_length = 120.0
tab_width = 14.0
tab_length = 26.0  # Total length from center of the collar to the end of tabs
slit_width = 2.5
screw_r = 2.5
screw_offset = 19.0 # Distance from collar center to screw hole center

# 1. Main Solid Body (Collar + Handle Arm + Clamping Tabs)
result = (
    cq.Workplane("XY")
    .cylinder(thickness, collar_r_out)
    .union(
        cq.Workplane("XY")
        .center(arm_length / 2, 0)
        .box(arm_length, arm_width, thickness)
    )
    .union(
        cq.Workplane("XY")
        .center(-tab_length / 2, 0)
        .box(tab_length, tab_width, thickness)
    )
)

# 2. Main Shaft Bore
result = result.faces(">Z").workplane().hole(collar_r_in * 2)

# 3. Clamping Slit
# Extending the cut slightly beyond the tab length to ensure a clean cut
result = (
    result.faces(">Z")
    .workplane()
    .center(-tab_length / 2, 0)
    .rect(tab_length + 5, slit_width)
    .cutThruAll()
)

# 4. Screw Hole
# Use XZ plane so the local Z direction extrudes along the global Y axis
screw_cut_tool = (
    cq.Workplane("XZ")
    .center(-screw_offset, 0)
    .cylinder(tab_width + 10, screw_r)
)
result = result.cut(screw_cut_tool)