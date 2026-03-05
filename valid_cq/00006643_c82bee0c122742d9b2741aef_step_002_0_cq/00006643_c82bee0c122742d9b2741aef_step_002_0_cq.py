import cadquery as cq

# --- Parameters ---
# Main body dimensions
main_width = 80.0
main_depth = 30.0
main_height = 10.0

# Side wings dimensions
wing_width = 25.0
wing_depth_extension = 20.0  # How much further back they go
total_wing_depth = main_depth + wing_depth_extension

# Pillars/Bosses dimensions
pillar_width = 5.0
pillar_depth = 5.0
pillar_height = 8.0  # Height above the main surface

# Cutout details
cutout_width = 15.0
cutout_depth = 10.0

# --- Construction ---

# 1. Create the base shape
# We'll create the central rectangle and unite it with the two side wings.
# Alternatively, sketch the profile on XY plane and extrude. Let's use the sketch approach for clarity.

# Calculate coordinates for the polygon
# Starting from front-left corner, going clockwise
# (0,0) is center of the front face for symmetry convenience later, but let's stick to corner references for polygons.
# Let's center the whole assembly on the origin roughly.

# Left Wing
left_wing = cq.Workplane("XY").box(wing_width, total_wing_depth, main_height) \
    .translate((-main_width/2 + wing_width/2, total_wing_depth/2 - main_depth/2, 0))

# Right Wing
right_wing = cq.Workplane("XY").box(wing_width, total_wing_depth, main_height) \
    .translate((main_width/2 - wing_width/2, total_wing_depth/2 - main_depth/2, 0))

# Center connecting piece
center_piece = cq.Workplane("XY").box(main_width - 2*wing_width, main_depth, main_height) \
    .translate((0, 0, 0))

# Combine to form the base U-shape
base = left_wing.union(right_wing).union(center_piece)

# 2. Add the pillars
# There are four visible pillars:
# - One on the far left rear corner
# - One on the far right rear corner
# - Two in the middle, flanking the central cutout area

# Rear Left Pillar
p1 = cq.Workplane("XY").box(pillar_width, pillar_depth, pillar_height) \
    .translate((-main_width/2 + pillar_width/2 + 2, # x: offset slightly from edge
                total_wing_depth - main_depth/2 - pillar_depth/2 - 2, # y: near back edge
                main_height/2 + pillar_height/2)) # z: on top

# Rear Right Pillar
p2 = cq.Workplane("XY").box(pillar_width, pillar_depth, pillar_height) \
    .translate((main_width/2 - pillar_width/2 - 2, # x
                total_wing_depth - main_depth/2 - pillar_depth/2 - 2, # y
                main_height/2 + pillar_height/2)) # z

# Middle Left Pillar
# Positioned near the inner corner of the U-shape
p3 = cq.Workplane("XY").box(pillar_width, pillar_depth, pillar_height) \
    .translate((-cutout_width/2 - pillar_width/2 - 2, # x: to the left of cutout
                main_depth/2 - pillar_depth/2 - 2, # y: near the back of the center section
                main_height/2 + pillar_height/2))

# Middle Right Pillar
p4 = cq.Workplane("XY").box(pillar_width, pillar_depth, pillar_height) \
    .translate((cutout_width/2 + pillar_width/2 + 2, # x: to the right of cutout
                main_depth/2 - pillar_depth/2 - 2, # y
                main_height/2 + pillar_height/2))

# Combine pillars with base
result = base.union(p1).union(p2).union(p3).union(p4)

# 3. Create the central cutout
# The image shows a rectangular notch in the back-center of the main connecting piece.
# It seems to have a small step or feature inside, but based on the resolution, 
# a simple rectangular cut or a stepped cut is plausible. 
# Looking closely, it looks like a simple rectangular cutout.

cutout = cq.Workplane("XY").box(cutout_width, cutout_depth, main_height) \
    .translate((0, main_depth/2 - cutout_depth/2, 0))

result = result.cut(cutout)

# Optional: Add the specific horizontal groove/slot feature seen on the inner left wall of the cutout area
# The image shows horizontal lines inside the cutout area on the left side, suggesting a slot.
slot_height = 2.0
slot_depth_cut = 2.0
side_slot = cq.Workplane("YZ").workplane(offset=-cutout_width/2).moveTo(main_depth/2 - cutout_depth/2, 0).rect(cutout_depth, slot_height).extrude(-slot_depth_cut)

# Let's interpret the image simpler: usually these are just simple notches. 
# However, looking at the "left" inner wall of the central gap, there are two horizontal lines.
# This implies a horizontal slot or groove running along that face.
# Let's cut a slot on the left inner face of the cutout.

slot_cut = (cq.Workplane("YZ")
            .workplane(offset=-cutout_width/2 + 0.1) # Start slightly inside the empty space to ensure cut
            .moveTo(main_depth/2 - cutout_depth/2, 0) # Center of the cutout depth, vertically centered
            .rect(cutout_depth, 3.0) # Width along Y, Height along Z
            .extrude(-5.0) # Cut into the material (negative X direction relative to global, local normal)
           )

result = result.cut(slot_cut)

# Re-center for nice view
result = result.translate((0, -main_depth/2, 0))