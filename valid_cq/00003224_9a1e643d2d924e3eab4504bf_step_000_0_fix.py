import cadquery as cq
import math

# Parameters
outer_radius = 50
inner_radius = 32
thickness = 3

# Clover/flower cutout parameters
clover_base_radius = 22
clover_lobe_radius = 8
clover_lobes = 4

# Mounting holes on outer ring
outer_hole_radius = 1.5
outer_hole_pcd = 45
outer_hole_count = 20

# Large holes on ring
large_hole_radius = 4
large_hole_pcd = 38
large_hole_count = 6

# Start with outer disk
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)

# Create the clover/flower shaped inner cutout
# Build clover profile using a series of arcs approximated by points
# The clover shape: 4 lobes centered at 90-degree intervals
clover_points = []
steps = 200
for i in range(steps + 1):
    angle = 2 * math.pi * i / steps
    # Clover shape: r = base_radius + lobe_radius * cos(lobes * angle)
    r = clover_base_radius + clover_lobe_radius * math.cos(clover_lobes * angle)
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    clover_points.append((x, y))

# Cut clover from disk
clover_wire = (
    cq.Workplane("XY")
    .spline(clover_points)
)

# Build clover solid to subtract
clover_solid = (
    cq.Workplane("XY")
    .spline(clover_points)
    .close()
    .extrude(thickness + 2)
    .translate((0, 0, -1))
)

result = result.cut(clover_solid)

# Add small holes around outer edge
for i in range(outer_hole_count):
    angle = 360.0 * i / outer_hole_count
    angle_rad = math.radians(angle)
    x = outer_hole_pcd * math.cos(angle_rad)
    y = outer_hole_pcd * math.sin(angle_rad)
    hole_solid = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(outer_hole_radius)
        .extrude(thickness + 2)
        .translate((0, 0, -1))
    )
    result = result.cut(hole_solid)

# Add large holes on the ring
for i in range(large_hole_count):
    angle = 360.0 * i / large_hole_count + 30
    angle_rad = math.radians(angle)
    x = large_hole_pcd * math.cos(angle_rad)
    y = large_hole_pcd * math.sin(angle_rad)
    hole_solid = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(large_hole_radius)
        .extrude(thickness + 2)
        .translate((0, 0, -1))
    )
    result = result.cut(hole_solid)