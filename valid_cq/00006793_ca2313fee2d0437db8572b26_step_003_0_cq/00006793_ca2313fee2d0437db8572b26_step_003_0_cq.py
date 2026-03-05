import cadquery as cq

# --- Parameters ---
ladder_height = 200.0
ladder_width = 40.0
rail_thickness_x = 5.0
rail_thickness_y = 10.0

# Rungs
rung_count = 6
rung_height = 4.0
rung_spacing = 25.0  # Center-to-center distance approx
start_rung_offset = 15.0 # Distance from bottom to first rung center

# Top feature (extensions)
top_extension_length = 60.0 # Length of rails extending past the top rung area
notch_depth = 2.0
notch_start_height = ladder_height - top_extension_length

# --- Modeling ---

# 1. Create the main rails
# We'll create one rail and mirror it, or create both directly.
# Let's create a base rectangle for the rail profile and extrude.

# Left Rail
rail_left = (
    cq.Workplane("XY")
    .box(rail_thickness_x, rail_thickness_y, ladder_height)
    .translate((-ladder_width / 2 + rail_thickness_x / 2, 0, ladder_height / 2))
)

# Right Rail
rail_right = (
    cq.Workplane("XY")
    .box(rail_thickness_x, rail_thickness_y, ladder_height)
    .translate((ladder_width / 2 - rail_thickness_x / 2, 0, ladder_height / 2))
)

ladder_structure = rail_left.union(rail_right)

# 2. Create the Rungs
# We will create a rung and pattern it, or iterate to place them.
rungs = cq.Workplane("XY")

for i in range(rung_count):
    z_pos = start_rung_offset + (i * rung_spacing)
    
    # Check to ensure rungs don't go into the top extension area too far
    if z_pos < notch_start_height:
        rung = (
            cq.Workplane("XY")
            .box(ladder_width - 2 * rail_thickness_x, rail_thickness_y, rung_height)
            .translate((0, 0, z_pos))
        )
        rungs = rungs.union(rung)

# Combine rails and rungs
ladder_structure = ladder_structure.union(rungs)

# 3. Create the Notch / Cutout at the top
# The image shows the top part of the rails is slightly thinner on the inside or has a step.
# It looks like a cutout on the inner face of the rails starting from a certain height.

# Cutout on Left Rail (inner side is +X relative to rail center)
# The left rail is at x = -ladder_width/2 + thickness/2. 
# Its inner face is at x = -ladder_width/2 + thickness.
cutout_left = (
    cq.Workplane("XY")
    .workplane(offset=notch_start_height)
    .box(notch_depth, rail_thickness_y, top_extension_length, centered=(False, True, False))
    .translate((-ladder_width / 2 + rail_thickness_x - notch_depth, 0, 0))
)

# Cutout on Right Rail (inner side is -X relative to rail center)
# The right rail is at x = ladder_width/2 - thickness/2.
# Its inner face is at x = ladder_width/2 - thickness.
cutout_right = (
    cq.Workplane("XY")
    .workplane(offset=notch_start_height)
    .box(notch_depth, rail_thickness_y, top_extension_length, centered=(False, True, False))
    .translate((ladder_width / 2 - rail_thickness_x, 0, 0))
)

# Apply the cuts
result = ladder_structure.cut(cutout_left).cut(cutout_right)

# 4. Angled Cut at the very top (optional based on image interpretation)
# The very tips look slightly angled or just flat. The image shows them flat, so we leave them.
# However, there is a small chamfer or angle at the transition of the notch.
# The simple box cut creates a sharp 90 degree step. The image shows a slight angle/taper at the notch start.
# Let's refine the cut to be a chamfered transition.

# Instead of a simple box cut, let's make a cutting tool that has a chamfer at the bottom.
# Re-doing the cut logic for better detail matching the image (sloped transition).

# Reset structure
ladder_structure = rail_left.union(rail_right).union(rungs)

def create_notch_cutter(x_pos, is_right_side):
    # Profile on YZ plane, extruded in X
    # Points for a trapezoidal cutter to make the angled transition
    
    chamfer_height = 5.0
    
    # We want to remove material from the inner face.
    # Base height of cut
    z_base = notch_start_height
    z_top = ladder_height
    
    # We define a profile in the XZ plane to sweep or extrude
    # But box is easier. Let's make a wedge for the transition.
    
    cutter_main = (
        cq.Workplane("XY")
        .box(notch_depth, rail_thickness_y, top_extension_length - chamfer_height, centered=(False, True, False))
        .translate((x_pos, 0, z_base + chamfer_height))
    )
    
    # Create the angled transition (wedge)
    # The wedge needs to go from 0 depth at z_base to notch_depth at z_base+chamfer_height
    wedge_pts = [
        (0, z_base),
        (notch_depth, z_base + chamfer_height),
        (0, z_base + chamfer_height)
    ]
    if is_right_side: # Direction of notch depth is positive X
         wedge_pts = [
            (0, z_base),
            (notch_depth, z_base + chamfer_height),
            (0, z_base + chamfer_height)
        ]       
    else: # For left side, we need to cut into the rail which is to the left. 
          # The logic gets tricky with offsets. Let's keep it simple:
          # Just make a wedge shape and position it.
          pass

    return cutter_main

# Let's try a simpler approach for the angled notch: direct 3D drafting or chamfering edges.
# The specific edge to chamfer is the inner corner where the thinning starts.
# Actually, modeling the rail with the profile is cleaner.

# --- Revised Approach: Rail Profile Extrusion ---

# Define the side profile of the rail (looking from Front/Y)
# Left Rail Profile (Outer edge is straight, inner edge steps in)
left_rail_x_outer = -ladder_width / 2
left_rail_x_inner_bottom = -ladder_width / 2 + rail_thickness_x
left_rail_x_inner_top = -ladder_width / 2 + rail_thickness_x - notch_depth

pts_left = [
    (left_rail_x_outer, 0),
    (left_rail_x_inner_bottom, 0),
    (left_rail_x_inner_bottom, notch_start_height),
    (left_rail_x_inner_top, notch_start_height + 5.0), # 5.0 is vertical transition length
    (left_rail_x_inner_top, ladder_height),
    (left_rail_x_outer, ladder_height)
]

rail_left_refined = (
    cq.Workplane("XZ")
    .polyline(pts_left)
    .close()
    .extrude(rail_thickness_y)
    .translate((0, -rail_thickness_y/2, 0)) # Center in Y
)

# Right Rail Profile
right_rail_x_outer = ladder_width / 2
right_rail_x_inner_bottom = ladder_width / 2 - rail_thickness_x
right_rail_x_inner_top = ladder_width / 2 - rail_thickness_x + notch_depth

pts_right = [
    (right_rail_x_outer, 0),
    (right_rail_x_inner_bottom, 0),
    (right_rail_x_inner_bottom, notch_start_height),
    (right_rail_x_inner_top, notch_start_height + 5.0),
    (right_rail_x_inner_top, ladder_height),
    (right_rail_x_outer, ladder_height)
]

rail_right_refined = (
    cq.Workplane("XZ")
    .polyline(pts_right)
    .close()
    .extrude(rail_thickness_y)
    .translate((0, -rail_thickness_y/2, 0))
)

# Rungs (re-generating to be sure)
rungs_refined = cq.Workplane("XY")
for i in range(rung_count):
    z_pos = start_rung_offset + (i * rung_spacing)
    # Rung connects the inner faces of the bottom part of the rails
    rung_w = right_rail_x_inner_bottom - left_rail_x_inner_bottom
    rung_center_x = (right_rail_x_inner_bottom + left_rail_x_inner_bottom) / 2
    
    if z_pos < notch_start_height:
        rung = (
            cq.Workplane("XY")
            .box(rung_w, rail_thickness_y, rung_height)
            .translate((rung_center_x, 0, z_pos))
        )
        rungs_refined = rungs_refined.union(rung)

# Final Assembly
result = rail_left_refined.union(rail_right_refined).union(rungs_refined)