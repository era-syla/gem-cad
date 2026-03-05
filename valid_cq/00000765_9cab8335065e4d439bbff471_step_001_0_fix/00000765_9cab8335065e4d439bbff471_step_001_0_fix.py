import cadquery as cq
import math

# Parameters
arm_length = 120
arm_width = 12
arm_height = 10
cylinder_od = 22
cylinder_id = 16
cylinder_height = 35
fin_height = 25
fin_width = 20

# Create the main curved arm connecting two cylinders
# The arm curves from lower-left to upper-right with a bend

# Left cylinder (lower)
left_cyl = (
    cq.Workplane("XY")
    .cylinder(cylinder_height, cylinder_od / 2)
    .translate((-50, -20, 0))
)

# Add bore to left cylinder
left_bore = (
    cq.Workplane("XY")
    .cylinder(cylinder_height + 2, cylinder_id / 2)
    .translate((-50, -20, 0))
)

# Right cylinder (upper, slightly different position)
right_cyl = (
    cq.Workplane("XY")
    .cylinder(cylinder_height, cylinder_od / 2)
    .translate((50, 20, 5))
)

right_bore = (
    cq.Workplane("XY")
    .cylinder(cylinder_height + 2, cylinder_id / 2)
    .translate((50, 20, 5))
)

# Create the curved arm body using a swept profile
# Define path points for the arm curve
path_pts = [
    (-50, -20, 0),
    (-20, -10, 5),
    (0, 5, 8),
    (25, 15, 8),
    (50, 20, 5),
]

# Build the arm as a series of boxes/primitives blended together
# Use a simpler approach: loft between cross-sections

# Create arm as extruded shape along a path
arm = (
    cq.Workplane("XZ")
    .moveTo(-50, 0)
    .threePointArc((0, 15), (50, 0))
    .lineTo(50, -arm_height)
    .threePointArc((0, 5), (-50, -arm_height))
    .close()
    .extrude(arm_width)
    .translate((0, -arm_width / 2, 0))
)

# Rotate arm to match the diagonal orientation
arm = arm.rotate((0, 0, 0), (0, 0, 1), 20)

# Left cylinder assembly
left_cylinder = (
    cq.Workplane("XY")
    .circle(cylinder_od / 2)
    .extrude(cylinder_height)
    .translate((-55, -15, -cylinder_height / 2))
)

left_cylinder = left_cylinder.cut(
    cq.Workplane("XY")
    .circle(cylinder_id / 2)
    .extrude(cylinder_height + 2)
    .translate((-55, -15, -cylinder_height / 2 - 1))
)

# Right cylinder assembly
right_cylinder = (
    cq.Workplane("XY")
    .circle(cylinder_od / 2)
    .extrude(cylinder_height)
    .translate((55, 15, -cylinder_height / 2 + 5))
)

right_cylinder = right_cylinder.cut(
    cq.Workplane("XY")
    .circle(cylinder_id / 2)
    .extrude(cylinder_height + 2)
    .translate((55, 15, -cylinder_height / 2 + 4))
)

# Triangular fin at the top of the arc
fin = (
    cq.Workplane("XY")
    .polyline([(0, 0), (fin_width, 0), (fin_width / 2, fin_height)])
    .close()
    .extrude(arm_width)
    .translate((-fin_width / 2, -arm_width / 2, 8))
    .rotate((0, 0, 0), (0, 0, 1), 20)
    .translate((5, 5, 0))
)

# Combine everything
combined = arm.union(left_cylinder).union(right_cylinder).union(fin)

# Add small holes along the arm
hole_positions_left = [(-30, -8, 0), (-20, -3, 0), (-10, 2, 0)]
hole_positions_right = [(20, 10, 5), (30, 14, 5), (40, 17, 5)]

for pos in hole_positions_left + hole_positions_right:
    hole = (
        cq.Workplane("XY")
        .circle(2.5)
        .extrude(arm_height + 20)
        .translate((pos[0], pos[1], -5))
    )
    combined = combined.cut(hole)

# Add split clamp cut to left cylinder
clamp_cut_left = (
    cq.Workplane("XZ")
    .rect(2, cylinder_height + 2)
    .extrude(cylinder_od + 2)
    .translate((-55, -15 - (cylinder_od + 2) / 2 + 1, 0))
)
combined = combined.cut(clamp_cut_left)

result = combined