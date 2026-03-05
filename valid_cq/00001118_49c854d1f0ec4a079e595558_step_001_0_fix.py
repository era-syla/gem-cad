import cadquery as cq

# Build a lifting eye bolt / pad eye fitting
# Components:
# 1. Bottom pin/stem (cylinder going down)
# 2. Base flange (wide flat disk)
# 3. Upper dome/body
# 4. Eye/ring on top

# Dimensions
stem_r = 4
stem_h = 12

flange_r = 14
flange_h = 3

body_r = 11
body_h = 8

eye_outer_r = 6
eye_inner_r = 3.5
eye_thickness = 3
eye_height = 10

# Start building
# Stem (pointing down, so z goes negative)
stem = (
    cq.Workplane("XY")
    .cylinder(stem_h, stem_r)
    .translate((0, 0, -stem_h / 2))
)

# Flange
flange = (
    cq.Workplane("XY")
    .cylinder(flange_h, flange_r)
    .translate((0, 0, flange_h / 2))
)

# Body dome on top of flange
body = (
    cq.Workplane("XY")
    .workplane(offset=flange_h)
    .cylinder(body_h, body_r)
    .translate((0, 0, body_h / 2 + flange_h))
)

# Actually let's build it step by step by union
result = (
    cq.Workplane("XY")
    .union(
        cq.Workplane("XY")
        .cylinder(stem_h, stem_r)
        .translate((0, 0, -stem_h / 2))
    )
    .union(
        cq.Workplane("XY")
        .cylinder(flange_h, flange_r)
        .translate((0, 0, flange_h / 2))
    )
    .union(
        cq.Workplane("XY")
        .cylinder(body_h, body_r)
        .translate((0, 0, flange_h + body_h / 2))
    )
)

# Eye ring sitting on top of the body, oriented in XZ plane
# The eye is a torus-like ring: create as a revolved circle
eye_center_z = flange_h + body_h + eye_height / 2 - 2
eye_center_y = 0

# Create the eye as a solid ring (torus section)
# Build eye as extruded annulus standing upright
eye_ring = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .circle(eye_outer_r)
    .circle(eye_inner_r)
    .extrude(eye_thickness)
    .translate((0, -eye_thickness / 2, flange_h + body_h - 2))
)

# Eye base/neck connecting ring to body
eye_base = (
    cq.Workplane("XY")
    .workplane(offset=flange_h + body_h - 2)
    .rect(eye_outer_r * 2 + 2, eye_thickness)
    .extrude(eye_height)
    .translate((0, 0, 0))
)

# Combine everything
result = result.union(eye_base).union(eye_ring)

# Add a small fillet to the flange top edge
try:
    result = result.edges("|Z").edges(cq.selectors.NearestToPointSelector((flange_r, 0, flange_h))).fillet(1.5)
except:
    pass

# Cut hole through eye ring
eye_hole = (
    cq.Workplane("XZ")
    .workplane(offset=-eye_thickness)
    .circle(eye_inner_r)
    .extrude(eye_thickness * 4)
    .translate((0, 0, flange_h + body_h - 2))
)

result = result.cut(eye_hole)

# Clean up top of body to be slightly domed - skip for simplicity
# Final result
result = result