import cadquery as cq
import math

# Parameters
thickness = 4
large_r = 12      # outer radius of large circle (top-left)
large_hole_r = 6  # inner hole radius of large circle
small_r = 9       # outer radius of small circle (bottom-right)
small_hole_r = 4.5  # inner hole radius of small circle
strap_w = 8       # width of connecting strap

# Centers
large_center = (0, 0)
small_center = (30, -18)

# Build the 2D profile as a face by creating the outer boundary and subtracting holes

# We'll build the shape using an extruded wire profile
# The outer profile is an S-curve connecting two circles

# Create large circle region
large_disk = (
    cq.Workplane("XY")
    .circle(large_r)
    .extrude(thickness)
)

# Create small circle region
small_disk = (
    cq.Workplane("XY")
    .center(small_center[0], small_center[1])
    .circle(small_r)
    .extrude(thickness)
)

# Create connecting strap between the two circles
# Tangent points connecting circles with a strap
# Vector from large to small center
dx = small_center[0] - large_center[0]
dy = small_center[1] - large_center[1]
dist = math.sqrt(dx**2 + dy**2)

# Angle of line connecting centers
angle = math.atan2(dy, dx)

# For the strap, use a rectangle connecting the two circles
# Offset perpendicular to the connecting line
perp_angle = angle + math.pi/2

# Half width of strap
hw = strap_w / 2

# Points for strap polygon (parallelogram connecting the two circles)
p1 = (large_center[0] + hw * math.cos(perp_angle), large_center[1] + hw * math.sin(perp_angle))
p2 = (large_center[0] - hw * math.cos(perp_angle), large_center[1] - hw * math.sin(perp_angle))
p3 = (small_center[0] - hw * math.cos(perp_angle), small_center[1] - hw * math.sin(perp_angle))
p4 = (small_center[0] + hw * math.cos(perp_angle), small_center[1] + hw * math.sin(perp_angle))

strap = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(thickness)
)

# Union all parts
body = large_disk.union(small_disk).union(strap)

# Cut holes
body = (
    body
    .cut(
        cq.Workplane("XY")
        .circle(large_hole_r)
        .extrude(thickness)
    )
    .cut(
        cq.Workplane("XY")
        .center(small_center[0], small_center[1])
        .circle(small_hole_r)
        .extrude(thickness)
    )
)

result = body