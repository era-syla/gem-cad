import cadquery as cq

# Geometric Parameters
L_centers = 110.0   # Distance between the centers of the end radii
H_large = 30.0      # Height of the larger (left) end
H_small = 18.0      # Height of the smaller (right) end
R_large = H_large / 2.0
R_small = H_small / 2.0
Thickness = 3.0     # Plate thickness
Step_x = 55.0       # X position where the top straight edge ends and notch begins
Step_depth = 2.0    # Depth of the notch/step on top edge
Hole_dia = 3.0      # Diameter of the hole

# Derived Points and Control Vertices
# We set the origin (0,0) at the bottom tangent point of the large left arc.
# The bottom edge lies on the X-axis (y=0).

# Start point: Bottom-Left tangent (0,0)
# Path proceeds counter-clockwise
pt_bottom_right = (L_centers, 0)
pt_arc_right_mid = (L_centers + R_small, R_small)
pt_top_right = (L_centers, H_small)

# The concave curve connects the top-right to the bottom of the step
pt_step_bottom = (Step_x, H_large - Step_depth)
# Control point for concave curve (saddle shape)
# Located midway in X, slightly lower in Y to create the dip
pt_curve_mid = ((L_centers + Step_x) / 2.0, H_small - 1.0)

pt_step_top = (Step_x, H_large)
pt_top_left = (0, H_large)
pt_arc_left_mid = (-R_large, R_large)

# Create the single part geometry
part = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(pt_bottom_right[0], pt_bottom_right[1])
    # 180 degree arc for the right nose
    .threePointArc(pt_arc_right_mid, pt_top_right)
    # Concave curve along the top edge
    .threePointArc(pt_curve_mid, pt_step_bottom)
    # Vertical step up
    .lineTo(pt_step_top[0], pt_step_top[1])
    # Straight top edge
    .lineTo(pt_top_left[0], pt_top_left[1])
    # 180 degree arc for the left nose
    .threePointArc(pt_arc_left_mid, (0, 0))
    .close()
    .extrude(Thickness)
)

# Cut the hole at the center of the right radius
# Center is at (L_centers, R_small) relative to our sketch origin
part = (
    part.faces(">Z")
    .workplane()
    .moveTo(L_centers, R_small)
    .circle(Hole_dia / 2.0)
    .cutThruAll()
)

# Arrange two parts as shown in the image (offset vertically)
part1 = part.translate((0, 5, 0))
part2 = part.translate((0, -H_large - 5, 0))

# Combine into final result
result = part1.union(part2)