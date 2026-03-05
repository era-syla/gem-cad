import cadquery as cq

# Parameters
plate_thickness = 3        # thickness of central web (Y direction)
gap = 12                   # gap between lug plates
lug_height = 2 * plate_thickness + gap
lug_depth = 20             # depth of each lug along X
web_length = 40            # length of central web along X
plate_height = 10          # extrusion height (Z direction)
hole_d = 10                # diameter of pin holes
pocket_depth = 3           # depth of rectangular pocket (into Z)
pocket_margin = 2          # margin from web ends for pocket

# Derived
total_length = 2 * lug_depth + web_length
half_length = total_length / 2
half_lug_h = lug_height / 2
half_web_h = plate_thickness / 2

# Build 2D profile and extrude
result = (
    cq.Workplane("XY")
    .polyline([
        (-half_length, -half_lug_h),
        (-half_length,  half_lug_h),
        (-half_length + lug_depth,  half_lug_h),
        (-half_length + lug_depth,  half_web_h),
        ( half_length - lug_depth,  half_web_h),
        ( half_length - lug_depth,  half_lug_h),
        ( half_length,              half_lug_h),
        ( half_length,             -half_lug_h),
        ( half_length - lug_depth, -half_lug_h),
        ( half_length - lug_depth, -half_web_h),
        (-half_length + lug_depth, -half_web_h),
        (-half_length + lug_depth, -half_lug_h),
    ])
    .close()
    .extrude(plate_height)
    # Drill pin holes through thickness (Y direction)
    .faces(">Y")
    .workplane()
    .pushPoints([(-half_length + lug_depth/2, 0), ( half_length - lug_depth/2, 0)])
    .hole(hole_d)
    # Cut rectangular pocket on top of central web
    .faces(">Z")
    .workplane()
    .rect(web_length - pocket_margin*2, plate_thickness)
    .cutBlind(-pocket_depth)
)

result