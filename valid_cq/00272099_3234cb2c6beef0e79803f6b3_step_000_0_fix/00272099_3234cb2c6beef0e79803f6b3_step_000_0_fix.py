import cadquery as cq

# Parameters for the small cup
H_small = 5.0
hole_depth_small = 4.0
R_out_small = 10.0
R_in_small = 8.0

# Parameters for the large cup
H_large = 7.0
hole_depth_large = 6.0
R_out_large = 15.0
R_in_large = 13.0

# Build the small cup
small = (
    cq.Workplane("XY")
    .cylinder(H_small, R_out_small)
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, H_small - hole_depth_small/2.0))
        .cylinder(hole_depth_small, R_in_small)
    )
    .translate((-25, 0, 0))
)

# Build the large cup
large = (
    cq.Workplane("XY")
    .cylinder(H_large, R_out_large)
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, H_large - hole_depth_large/2.0))
        .cylinder(hole_depth_large, R_in_large)
    )
    .translate((25, 0, 0))
)

# Combine into final result
result = small.union(large)