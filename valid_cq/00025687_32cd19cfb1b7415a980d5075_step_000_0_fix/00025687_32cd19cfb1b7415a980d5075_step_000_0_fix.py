import cadquery as cq

# Parameters
th = 3                 # thickness
leg_w = 4              # leg width
leg_spacing = 40       # space between legs
leg_h = 50             # leg height
main_h = 30            # main body height above legs
bar_h = 8              # bracket top bar height
slot_w = 3             # slot width in panel
slot_h = 18            # slot height in panel
W = 2 * leg_w + leg_spacing  # total panel width

# Create panel with curved top
panel = (
    cq.Workplane("XY")
      .moveTo(0, 0)
      .lineTo(W, 0)
      .lineTo(W, leg_h)
      .threePointArc((W/2, leg_h + main_h), (0, leg_h))
      .close()
      .extrude(th)
)

# Cut three angled slots in panel
angles = [-15, 0, 15]
for i, angle in enumerate(angles):
    x = W * (i + 1) / (len(angles) + 1)
    y = leg_h + main_h * 0.4
    panel = panel.cut(
        cq.Workplane("XY")
          .transformed(offset=(x, y, 0), rotate=(0, 0, angle))
          .rect(slot_w, slot_h)
          .extrude(th)
    )

# Create U-shaped bracket
pts = [
    (0, 0),
    (W, 0),
    (W, leg_h),
    (W, leg_h + bar_h),
    (0, leg_h + bar_h),
    (0, leg_h),
    (leg_w, leg_h),
    (leg_w, 0)
]
bracket = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(th)
)

# Cut two rectangular slots in the bracket top bar
for x in [leg_w/2, W - leg_w/2]:
    bracket = bracket.cut(
        cq.Workplane("XY")
          .transformed(offset=(x, leg_h + bar_h/2, 0))
          .rect(leg_w, bar_h)
          .extrude(th)
    )

# Position bracket below panel for visualization
bracket = bracket.translate((0, -(leg_h + bar_h + 10), 0))

# Combine into one compound result
result = panel.union(bracket)