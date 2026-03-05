import cadquery as cq
import math

# Parameters
outer_radius = 20
inner_radius = 14
height = 18
knurl_height = 12
knurl_count = 48
knurl_depth = 1.2
top_flange_height = 4
top_flange_outer_radius = 21
bore_radius = 4
bore_depth = 14
inner_bore_small_radius = 2
inner_bore_small_depth = 4

# Build the main body - cylinder
body = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
)

# Add top flange
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=height/2)
    .circle(top_flange_outer_radius)
    .extrude(top_flange_height)
)

result = body.union(top_flange)

# Cut knurling grooves around the lower portion of the cylinder
# Using vertical slots around the circumference
for i in range(knurl_count):
    angle = i * 360.0 / knurl_count
    angle_rad = math.radians(angle)
    
    # Position of each groove on the surface
    x = (outer_radius - knurl_depth/2) * math.cos(angle_rad)
    y = (outer_radius - knurl_depth/2) * math.sin(angle_rad)
    
    # Width of each groove
    groove_width = 2 * math.pi * outer_radius / knurl_count * 0.4
    
    groove = (
        cq.Workplane("XY")
        .workplane(offset=-height/2)
        .transformed(rotate=(0, 0, angle))
        .rect(groove_width, outer_radius * 2 + knurl_depth * 2)
        .extrude(knurl_height)
    )
    
    result = result.cut(groove)

# Cut the main inner bore (large)
inner_bore = (
    cq.Workplane("XY")
    .workplane(offset=height/2 + top_flange_height)
    .circle(inner_radius)
    .extrude(-(bore_depth + top_flange_height))
)

result = result.cut(inner_bore)

# Cut the small center bore at bottom
small_bore = (
    cq.Workplane("XY")
    .workplane(offset=height/2 + top_flange_height)
    .circle(inner_bore_small_radius)
    .extrude(-(height + top_flange_height))
)

result = result.cut(small_bore)