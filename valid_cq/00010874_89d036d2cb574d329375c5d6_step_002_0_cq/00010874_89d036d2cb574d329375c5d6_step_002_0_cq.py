import cadquery as cq

# Parametric dimensions
rod_diameter = 6.0
rod_length = 50.0
head_diameter = 14.0
head_length = 15.0
slot_width = 6.0
slot_depth = 12.0
hole_diameter = 5.0
chamfer_size = 0.5
fillet_radius = 0.5

# 1. Create the main rod (shaft)
rod = cq.Workplane("XY").circle(rod_diameter / 2).extrude(rod_length)

# 2. Create the larger head at the end of the rod
# The head starts where the rod ends
head = (
    cq.Workplane("XY")
    .workplane(offset=rod_length)
    .circle(head_diameter / 2)
    .extrude(head_length)
)

# 3. Combine the rod and the head
part = rod.union(head)

# 4. Create the U-shaped slot (clevis) in the head
# We cut a rectangular slot from the top of the head
part = part.faces(">Z").workplane().center(0, 0).rect(slot_width, head_diameter * 1.5).cutBlind(-slot_depth)

# 5. Create the cross-hole through the clevis ears
# The hole goes through the side (Y-axis relative to the slot orientation)
# We need to position the workplane correctly.
# The slot was cut along Y (width along X), so the ears are on +X and -X sides? 
# Let's re-verify the slot cut.
# .rect(slot_width, head_diameter * 1.5) creates a rectangle centered on Z axis.
# Width is X, Height is Y.
# So the slot removes material where -slot_width/2 < x < slot_width/2.
# The "ears" remain on the left and right (if looking along Y) or top/bottom (if looking along X).
# Wait, if rect width is `slot_width` (X dimension) and height is large (Y dimension),
# the material is removed in the middle along X.
# So the ears are at +X and -X? No, the remaining material is at +Y and -Y?
# No, if I cut a rectangle WxH:
#   X goes from -W/2 to W/2
#   Y goes from -H/2 to H/2
# The cylinder is intersected by this large rectangle.
# The result is material removed in the center. The remaining material (ears) is on the Y-axis sides?
# No, that would be a slot across the full face.
# Let's assume standard clevis orientation.
# Let's cut a slot of width `slot_width` along the Y axis.
# This means the rectangle is `head_diameter` wide (X) and `slot_width` high (Y).
# Actually, looking at the image, the slot has flat faces.
# Let's just use a center rectangle cut.
# If I use `rect(head_diameter*1.1, slot_width)`, I cut a channel along X, leaving ears on +Y/-Y.
# The cross hole should then go along the Y axis.

# Let's refine step 4: Cut the slot.
# Let's align the slot so the open faces are normal to the X-axis (ears on +Y and -Y is confusing).
# Let's make the ears on the +/- X axis sides.
# Therefore, we cut out the middle Y-section.
# Rectangle: width (X) = slot_width, height (Y) = huge.
part = part.faces(">Z").workplane().rect(slot_width, head_diameter * 2).cutBlind(-slot_depth)

# 6. Create the hole
# Now the ears are separated by the X-axis slot. The faces of the ears are planar on the inside (X-normal planes).
# The hole should go through the ears, perpendicular to the slot.
# Since the slot is cut along Y (removing X material), the hole should go along X.
# Wait, if I cut a rect of width `slot_width` (X dimension), I remove the center X material.
# The ears are on the left (-X) and right (+X)? No.
# If I remove geometry where -3 < x < 3, the remaining geometry is where x < -3 or x > 3.
# So the ears are at +/- X.
# The hole needs to go through both ears, so the hole axis is X.
# Let's position the hole center.
# Z-position: from the top face, down by some amount. Usually half the hole depth or centered in the ear.
hole_center_offset = slot_depth / 2.0
part = (
    part.faces(">X")  # Select one of the outer ear faces
    .workplane()
    .center(0, -hole_center_offset) # Adjust local coordinates (Z becomes Y in this local plane usually, check needed)
    # When selecting >X face, normal is X. Local X is likely global Y, Local Y is global Z.
    # We want to move down in global Z. So that's local Y.
    .circle(hole_diameter / 2)
    .cutBlind(-head_diameter * 2) # Cut through everything
)

# 7. Add details: Chamfer the bottom of the rod
part = part.edges("<Z").chamfer(chamfer_size)

# 8. Add details: Fillet the transition between rod and head
# We need to select the edge at Z = rod_length
part = part.edges(cq.selectors.NearestToPointSelector((0, 0, rod_length))).fillet(fillet_radius)

# 9. Add details: Chamfer/Fillet the top edge of the head (optional but looks nice)
part = part.edges(">Z").chamfer(chamfer_size)

result = part