import cadquery as cq
import math

# Parameters
outer_radius = 20.0
inner_radius = 5.0
total_height = 10.0
knurl_height = 3.0
knurl_count = 36
knurl_depth = 1.2
top_fillet = 3.0
chamfer_top = 1.0

# Main body - cylinder
body = (
    cq.Workplane("XY")
    .cylinder(total_height, outer_radius)
)

# Add top fillet on the outer edge
body = body.edges(">Z").fillet(top_fillet - 0.1)

# Subtract inner hole with countersink-like shape
# First the main through hole
body = (
    body
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

# Add countersink cone on top
cone_top_r = inner_radius * 2.5
cone_bot_r = inner_radius
cone_height = 3.0

cone = (
    cq.Workplane("XY")
    .workplane(offset=total_height / 2)
    .add(
        cq.CQ(
            cq.Solid.makeCone(cone_top_r, cone_bot_r, cone_height)
        ).val()
    )
)

cone_solid = (
    cq.Workplane("XY")
    .workplane(offset=total_height / 2 - cone_height)
    .circle(cone_top_r)
    .workplane(offset=cone_height)
    .circle(cone_bot_r)
    .loft()
)

body = body.cut(cone_solid)

# Add knurling around the bottom edge
# Create knurl teeth as small rectangular cuts around the circumference
knurl_result = body

angle_step = 360.0 / knurl_count
tooth_width_angle = angle_step * 0.5  # half the step is tooth, half is gap

for i in range(knurl_count):
    angle = i * angle_step
    angle_rad = math.radians(angle)
    
    # Position of cut
    cx = outer_radius * math.cos(angle_rad)
    cy = outer_radius * math.sin(angle_rad)
    
    # Create a small rectangular cut on the outer surface
    cut_box = (
        cq.Workplane("XY")
        .workplane(offset=-total_height / 2)
        .transformed(rotate=cq.Vector(0, 0, angle))
        .rect(knurl_depth * 2, outer_radius * math.radians(tooth_width_angle))
        .extrude(knurl_height)
        .translate((outer_radius - knurl_depth, 0, -total_height / 2))
    )

# Redo knurling with polar array approach
# Create a single knurl tooth cutter
tooth_angle = 360.0 / knurl_count
tooth_arc = 2 * math.pi * outer_radius * (tooth_angle / 360.0) * 0.45

knurl_cutter = (
    cq.Workplane("XY")
    .box(knurl_depth * 2 + 1, tooth_arc, knurl_height + 0.1)
    .translate((outer_radius + knurl_depth / 2, 0, -total_height / 2 + knurl_height / 2 - 0.05))
)

# Cut all knurl teeth
for i in range(knurl_count):
    angle = i * (360.0 / knurl_count)
    rotated_cutter = knurl_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    body = body.cut(rotated_cutter)

result = body