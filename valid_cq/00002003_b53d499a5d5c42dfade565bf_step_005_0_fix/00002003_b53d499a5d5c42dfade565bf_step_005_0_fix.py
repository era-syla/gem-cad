import cadquery as cq

# Parameters
outer_dia = 50.0
knurl_dia = 36.0
knurl_height = 4.0
body_height = 8.0
total_height = knurl_height + body_height

counterbore1_dia = 20.0
counterbore1_depth = 2.0
counterbore2_dia = 12.0
counterbore2_depth = 4.0
through_hole_dia = 6.0

num_teeth = 36
tooth_width = 2.0  # angular width thickness
r_inner = knurl_dia / 2.0
r_outer = outer_dia / 2.0

# Main solid: cylinder with total height
base = cq.Workplane("XY").circle(outer_dia / 2.0).extrude(total_height)

# Counterbores and through hole on top face
result = (
    base
    .faces(">Z")
    .workplane()
    # first wide shallow counterbore
    .circle(counterbore1_dia / 2.0).cutBlind(-counterbore1_depth)
    # second narrower deeper counterbore
    .faces(">Z")
    .workplane()
    .circle(counterbore2_dia / 2.0).cutBlind(-counterbore2_depth)
    # through hole
    .faces(">Z")
    .workplane()
    .hole(through_hole_dia, depth=total_height + 1)
)

# Create one tooth as a triangular prism
tooth = (
    cq.Workplane("XY")
    .moveTo(r_inner, 0)
    .lineTo(r_outer, tooth_width/2.0)
    .lineTo(r_outer, -tooth_width/2.0)
    .close()
    .extrude(knurl_height + 1)  # +1 to ensure full cut
)

# Build all teeth by rotating the single tooth
teeth = None
angle_step = 360.0 / num_teeth
for i in range(num_teeth):
    rot = tooth.rotate((0,0,0), (0,0,1), angle_step * i)
    if teeth is None:
        teeth = rot
    else:
        teeth = teeth.union(rot)

# Subtract teeth from result to create knurl pattern
result = result.cut(teeth)

# Result holds the final solid
# (In a script you might show it, but here we assign to result)
result