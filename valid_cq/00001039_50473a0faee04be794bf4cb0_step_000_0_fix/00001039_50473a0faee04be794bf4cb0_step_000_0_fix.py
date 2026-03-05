import cadquery as cq
import math

# Parameters
outer_radius = 50
rim_inner_radius = 45
thickness = 5
num_teeth = 60
tooth_height = 3
hub_radius = 5
hole_radius = 2.5
num_spokes = 5
spoke_width = 3

# Start with the basic ring
result = cq.Workplane("XY") \
    .circle(outer_radius) \
    .circle(rim_inner_radius) \
    .extrude(thickness)

# Add teeth around the outer radius
tooth_width = 2 * outer_radius * math.sin(math.pi / num_teeth) * 0.9
for i in range(num_teeth):
    angle = 2 * math.pi * i / num_teeth
    x = (outer_radius + tooth_height / 2) * math.cos(angle)
    y = (outer_radius + tooth_height / 2) * math.sin(angle)
    tooth = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(tooth_width, tooth_height)
        .extrude(thickness)
    )
    result = result.union(tooth)

# Add central hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(thickness)
result = result.union(hub)

# Add spokes
spoke_length = rim_inner_radius - hub_radius
for i in range(num_spokes):
    ang_deg = 360.0 * i / num_spokes
    spoke = (
        cq.Workplane("XY")
        .rect(spoke_width, spoke_length)
        .extrude(thickness)
        .translate((hub_radius + spoke_length / 2, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), ang_deg)
    )
    result = result.union(spoke)

# Cut central hole
hole = cq.Workplane("XY").circle(hole_radius).extrude(thickness + 1)
result = result.cut(hole)