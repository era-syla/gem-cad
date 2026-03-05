import cadquery as cq
import math

# Parameters
outer_radius = 50
inner_radius = 45
height = 8
lip_height = 3
notch_width = 8
notch_depth = 5

# Create the main semicircle body
# Start with a full circle profile, then cut to semicircle

# Create the outer semicircle extrusion
outer_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .threePointArc((0, outer_radius), (-outer_radius, 0))
    .lineTo(0, 0)
    .close()
)

main_body = outer_profile.extrude(height)

# Create inner cutout (to make it a shell/lip shape - the rim)
# The top surface has a recessed inner area
inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=lip_height)
    .moveTo(0, 0)
    .lineTo(inner_radius, 0)
    .threePointArc((0, inner_radius), (-inner_radius, 0))
    .lineTo(0, 0)
    .close()
    .extrude(height - lip_height + 1)
)

result = main_body.cut(inner_cut)

# Add notch on the flat edge (middle of the straight edge)
notch = (
    cq.Workplane("XY")
    .rect(notch_width, notch_depth * 2)
    .extrude(height + 1)
    .translate((0, notch_depth / 2, -0.5))
)

result = result.cut(notch)

# Apply fillets to top edges
result = (
    result
    .edges("|Z")
    .fillet(1.0)
)