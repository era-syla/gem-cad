import cadquery as cq
import math

# Create a funnel/horn shape - large bell on one side tapering to a small tube

# Parameters
bell_radius = 40
bell_depth = 35
neck_radius = 8
neck_length = 20
tube_outer_radius = 6
tube_inner_radius = 3.5
tube_length = 25
collar_radius = 9
collar_length = 5

# Build the main bell/horn shape using revolve
# Profile points for the bell shape (x=radius, y=height along axis)
# The bell opens up like a flower/funnel

# Create the outer shell profile for revolve
# Points go from the tube end to the bell rim
pts_outer = [
    (tube_outer_radius, 0),
    (tube_outer_radius, tube_length),
    (collar_radius, tube_length + collar_length),
    (neck_radius, tube_length + collar_length + neck_length),
    (bell_radius * 0.3, tube_length + collar_length + neck_length + bell_depth * 0.3),
    (bell_radius * 0.7, tube_length + collar_length + neck_length + bell_depth * 0.65),
    (bell_radius, tube_length + collar_length + neck_length + bell_depth),
]

pts_inner = [
    (tube_inner_radius, 0),
    (tube_inner_radius, tube_length),
    (tube_inner_radius + 1, tube_length + collar_length),
    (tube_inner_radius + 2, tube_length + collar_length + neck_length),
    (bell_radius * 0.3 - 3, tube_length + collar_length + neck_length + bell_depth * 0.3),
    (bell_radius * 0.7 - 3, tube_length + collar_length + neck_length + bell_depth * 0.65),
    (bell_radius - 3, tube_length + collar_length + neck_length + bell_depth),
]

total_height = tube_length + collar_length + neck_length + bell_depth

# Build outer profile
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(pts_outer[0][0], pts_outer[0][1])
    .spline(pts_outer[1:], includeCurrent=True)
    .lineTo(0, total_height)
    .lineTo(0, 0)
    .close()
)

outer_solid = outer_profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Build inner profile for hollowing
inner_profile = (
    cq.Workplane("XZ")
    .moveTo(pts_inner[0][0], pts_inner[0][1])
    .spline(pts_inner[1:], includeCurrent=True)
    .lineTo(0, total_height)
    .lineTo(0, pts_inner[0][1])
    .close()
)

inner_solid = inner_profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Subtract inner from outer
result = outer_solid.cut(inner_solid)

# Rotate so the tube points to the right and bell faces upper-left
result = result.rotate((0, 0, 0), (0, 0, 1), -90)