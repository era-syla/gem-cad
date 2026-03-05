import cadquery as cq

TL = 5       # tip length
RL = 3       # ring length
BL = 250     # body length
D_tip = 2    # tip diameter
D_body = 5   # main body diameter
groove_depth = 1
groove_width = 1

total_length = 2*TL + 2*RL + BL

# Create the main rod
result = cq.Workplane("XY").circle(D_body/2).extrude(total_length)

# Cut the grooves (two near each end)
groove_positions = [TL, TL+RL, TL+RL+BL, TL+RL+BL+RL]
for pos in groove_positions:
    cutter = (
        cq.Workplane("XY", origin=(0, 0, pos))
        .circle(D_body/2)
        .circle(D_body/2 - groove_depth)
        .extrude(groove_width)
    )
    result = result.cut(cutter)

# Cut the tip profiles (remove outer material to form smaller diameter tips)
cutter_bottom = (
    cq.Workplane("XY")
    .circle(D_body/2)
    .circle(D_tip/2)
    .extrude(TL)
)
result = result.cut(cutter_bottom)

cutter_top = (
    cq.Workplane("XY", origin=(0, 0, total_length - TL))
    .circle(D_body/2)
    .circle(D_tip/2)
    .extrude(TL)
)
result = result.cut(cutter_top)