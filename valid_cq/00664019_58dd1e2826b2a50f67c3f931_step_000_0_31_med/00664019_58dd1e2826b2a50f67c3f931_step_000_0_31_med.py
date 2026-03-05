import cadquery as cq

# Parametric dimensions
thickness = 5.0
center_r = 14.0
center_hole_r = 7.0

arm_dist = 28.0
arm_r_outer = 14.0
arm_hole_r = 9.0

small_dist = 21.0
small_r_outer = 6.0
small_hole_r = 2.5

# Build the central hub
base = cq.Workplane("XY").cylinder(thickness, center_r)

# Create a single main arm and its blade component
arm_base = cq.Workplane("XY").center(arm_dist, 0).cylinder(thickness, arm_r_outer)

# Crescent blade created by boolean difference
blade_pos = cq.Workplane("XY").center(arm_dist, 10).cylinder(thickness, 14)
blade_neg = cq.Workplane("XY").center(arm_dist - 6, 20).cylinder(thickness, 18)
blade = blade_pos.cut(blade_neg)

single_arm = arm_base.union(blade)

# Add the 3 main lobes via rotational array
for i in range(3):
    angle = i * 120
    rotated_arm = single_arm.rotate((0, 0, 0), (0, 0, 1), angle)
    base = base.union(rotated_arm)

# Create and add the 3 small intermediate lobes
small_arm = cq.Workplane("XY").center(small_dist, 0).cylinder(thickness, small_r_outer)
for i in range(3):
    angle = i * 120 + 60
    rotated_small = small_arm.rotate((0, 0, 0), (0, 0, 1), angle)
    base = base.union(rotated_small)

# Create the tool body containing all the holes to be cut out
holes = cq.Workplane("XY").cylinder(thickness * 2, center_hole_r)

for i in range(3):
    # Main arm holes
    main_angle = i * 120
    hole = cq.Workplane("XY").center(arm_dist, 0).cylinder(thickness * 2, arm_hole_r)
    hole = hole.rotate((0, 0, 0), (0, 0, 1), main_angle)
    holes = holes.union(hole)

    # Small intermediate holes
    small_angle = i * 120 + 60
    small_hole = cq.Workplane("XY").center(small_dist, 0).cylinder(thickness * 2, small_hole_r)
    small_hole = small_hole.rotate((0, 0, 0), (0, 0, 1), small_angle)
    holes = holes.union(small_hole)

# Apply the cuts to get the final geometry
result = base.cut(holes)