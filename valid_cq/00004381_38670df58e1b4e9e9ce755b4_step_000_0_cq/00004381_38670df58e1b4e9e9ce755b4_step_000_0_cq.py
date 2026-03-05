import cadquery as cq

# --- Parametric Dimensions ---
# Main Frame Dimensions
frame_length = 50.0
frame_width = 30.0
frame_thickness = 2.0
rim_height = 1.0  # Height of the small rim around the frame
rim_thickness = 1.5

# Vertical Latch Dimensions
latch_pos_from_end = 15.0  # Where the vertical part starts
latch_width = 15.0
latch_height = 25.0
latch_thickness = 2.0
latch_head_overhang = 3.0
latch_head_height = 8.0
latch_head_angle_offset = 2.0 # Taper at the top

# Front Clip Dimensions
front_clip_radius = 2.5
front_clip_width = frame_width + 4.0 # Slightly wider than frame

# Internal Features
crossbar_pos = 15.0 # Position of the divider bar
crossbar_thickness = 2.0
cutout_slot_width = 6.0
cutout_slot_length = 8.0

# --- Modeling ---

# 1. Base Frame (Rectangular frame with cutouts)
# Start with a solid block
base = cq.Workplane("XY").box(frame_length, frame_width, frame_thickness)

# Create the two main cutouts to form the frame
# Calculate cutout sizes
cutout_1_length = crossbar_pos - (2 * rim_thickness)
cutout_2_length = frame_length - crossbar_pos - crossbar_thickness - (2 * rim_thickness)
cutout_width = frame_width - (2 * rim_thickness)

# Cutout 1 (Front)
cutout1 = (cq.Workplane("XY")
           .rect(cutout_1_length, cutout_width)
           .extrude(frame_thickness * 2, both=True)
           .translate((-frame_length/2 + rim_thickness + cutout_1_length/2, 0, 0)))

# Cutout 2 (Back)
cutout2 = (cq.Workplane("XY")
           .rect(cutout_2_length, cutout_width)
           .extrude(frame_thickness * 2, both=True)
           .translate((frame_length/2 - rim_thickness - cutout_2_length/2, 0, 0)))

frame = base.cut(cutout1).cut(cutout2)

# 2. Add Rim (Small elevated border)
# We select the top face, offset the outer wire inwards to create the rim profile, and extrude
# A simpler way is to just create a box outline on top
rim_outer = cq.Workplane("XY").rect(frame_length, frame_width).extrude(rim_height + frame_thickness/2)
rim_inner = cq.Workplane("XY").rect(frame_length - 2*rim_thickness, frame_width - 2*rim_thickness).extrude(20, both=True)
rim = rim_outer.cut(rim_inner).translate((0,0, frame_thickness/2))

# Combine frame and rim
main_body = frame.union(rim)

# 3. Vertical Latch Mechanism
# This is located near the middle/back.
# Define the profile on the XZ plane (side view)
latch_pts = [
    (0, 0),
    (0, latch_height),
    (latch_thickness + latch_head_overhang, latch_height),
    (latch_thickness, latch_height - latch_head_height),
    (latch_thickness, 0),
    (0,0) # Close loop
]

latch = (cq.Workplane("XZ")
         .polyline(latch_pts)
         .close()
         .extrude(latch_width) # Extrude symmetrically? No, default is one direction Z
         .translate((crossbar_pos - frame_length/2 + crossbar_thickness, -latch_width/2, frame_thickness/2))
         )

# Add chamfer to the top back of the latch for the angled look
latch = latch.edges(">Z and >X").chamfer(latch_head_angle_offset)


# 4. Front Cylindrical Catch
# A cylinder/rounded feature at the front (-X) end
front_cyl = (cq.Workplane("YZ")
             .circle(front_clip_radius)
             .extrude(front_clip_width)
             .translate((-frame_length/2, -front_clip_width/2, 0))
             )

# Cut a slot in the cylinder for the clip action
cyl_slot = (cq.Workplane("XY")
            .rect(2.0, front_clip_width + 2)
            .extrude(10)
            .translate((-frame_length/2 + 1.0, 0, 2)) # Adjust height for slot depth
           )
front_feature = front_cyl.cut(cyl_slot)

# Add small retaining nubs on top of the frame near the front
nub_h = 1.5
nub_w = 2.0
nub_l = 2.0
nub1 = (cq.Workplane("XY")
        .box(nub_l, nub_w, nub_h)
        .translate((-frame_length/2 + rim_thickness + nub_l/2, frame_width/2 - rim_thickness/2, frame_thickness/2 + rim_height + nub_h/2))
        )
nub2 = (cq.Workplane("XY")
        .box(nub_l, nub_w, nub_h)
        .translate((-frame_length/2 + rim_thickness + nub_l/2, -frame_width/2 + rim_thickness/2, frame_thickness/2 + rim_height + nub_h/2))
        )
# Chamfer nubs to make them look like catches
nub1 = nub1.edges(">Z and >X").chamfer(0.5)
nub2 = nub2.edges(">Z and >X").chamfer(0.5)


# 5. Internal platform near the latch
# There is a solid platform extending from the latch base into the rear cutout
platform_len = 12.0
platform = (cq.Workplane("XY")
            .box(platform_len, latch_width, frame_thickness)
            .translate((crossbar_pos - frame_length/2 + crossbar_thickness + platform_len/2, 0, 0))
           )

# Slot cutout in the platform
plat_slot = (cq.Workplane("XY")
             .rect(cutout_slot_length, cutout_slot_width)
             .extrude(10, both=True)
             .translate((crossbar_pos - frame_length/2 + crossbar_thickness + platform_len - cutout_slot_length/2, 0, 0))
            )
# Add rounded end to slot
plat_slot_fillet_tool = (cq.Workplane("XY")
                         .circle(cutout_slot_width/2)
                         .extrude(10, both=True)
                         .translate((crossbar_pos - frame_length/2 + crossbar_thickness + platform_len - cutout_slot_length, 0, 0))
                        )

platform_modified = platform.cut(plat_slot).cut(plat_slot_fillet_tool)


# --- Assembly ---
result = main_body.union(latch).union(front_feature).union(nub1).union(nub2).union(platform_modified)

# Final cleanup/fillets if necessary for realism (optional but makes it look nicer)
# Fillet vertical edges of the latch base for strength
try:
    result = result.edges("|Z").filter(lambda e: e.Center().z > 0 and e.Center().x > 0).fillet(0.5)
except:
    pass # Skip if geometry is too tight

# Export or Render
if 'show_object' in globals():
    show_object(result)