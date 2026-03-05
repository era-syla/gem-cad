import cadquery as cq
import math

# Parameters
R_outer = 10.0
thickness = 1.5
R_inner = R_outer - thickness
main_length = 80.0
flange_radius = 14.0
flange_thickness = 6.0
branch_angle = 45.0  # degrees from vertical
angle_rad = math.radians(branch_angle)
# Compute branch attachment height so the centerline meets the cylinder wall
z_branch = R_outer * math.cos(angle_rad) / math.sin(angle_rad)
branch_length = 80.0  # length of branch pipe (enough to pass through)

# Main outer cylinder
main_outer = (
    cq.Workplane("XY")
    .workplane(offset=-main_length/2)
    .circle(R_outer)
    .extrude(main_length)
)

# Flanges
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=main_length/2)
    .circle(flange_radius)
    .circle(R_inner)
    .extrude(flange_thickness)
)
bottom_flange = (
    cq.Workplane("XY")
    .workplane(offset=-main_length/2 - flange_thickness)
    .circle(flange_radius)
    .circle(R_inner)
    .extrude(flange_thickness)
)

# Branch outer pipes
branch_outer_top = (
    cq.Workplane("XY")
    .transformed(offset=(R_outer, 0,  z_branch), rotate=(0,  branch_angle, 0))
    .circle(R_outer)
    .extrude(branch_length)
)
branch_outer_bottom = (
    cq.Workplane("XY")
    .transformed(offset=(R_outer, 0, -z_branch), rotate=(0, -branch_angle, 0))
    .circle(R_outer)
    .extrude(branch_length)
)

# Assemble outer geometry
result = (
    main_outer
    .union(top_flange)
    .union(bottom_flange)
    .union(branch_outer_top)
    .union(branch_outer_bottom)
)

# Inner cuts (hollow)
main_inner = (
    cq.Workplane("XY")
    .workplane(offset=-main_length/2)
    .circle(R_inner)
    .extrude(main_length)
)
branch_inner_top = (
    cq.Workplane("XY")
    .transformed(offset=(R_outer, 0,  z_branch), rotate=(0,  branch_angle, 0))
    .circle(R_inner)
    .extrude(branch_length)
)
branch_inner_bottom = (
    cq.Workplane("XY")
    .transformed(offset=(R_outer, 0, -z_branch), rotate=(0, -branch_angle, 0))
    .circle(R_inner)
    .extrude(branch_length)
)

# Cut out inner volumes
result = (
    result
    .cut(main_inner)
    .cut(branch_inner_top)
    .cut(branch_inner_bottom)
)