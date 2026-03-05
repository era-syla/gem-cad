import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
length = 80.0
width = 80.0
thickness = 25.0

# Central Bore
bore_diameter = 35.0
bore_depth = thickness 

# The clamping slot
slot_width = 4.0
slot_length_from_edge = 35.0 # How far the split goes in

# The side cutout/pocket
side_pocket_width = 30.0
side_pocket_depth = 15.0 # Into the side
side_pocket_height = 12.0

# The large hole on the front face (transverse)
transverse_hole_diameter = 16.0
transverse_hole_pos_x = length/2.0 - 15.0 # Approximate position based on image

# Mounting holes (top surface)
# Looks like a pattern of 4 holes, plus maybe 2 near the split
mount_hole_dia = 5.0
mount_hole_spacing_x = 55.0
mount_hole_spacing_y = 60.0

# Holes on the split face (clamping screw holes)
clamp_hole_dia = 5.0
clamp_counterbore_dia = 9.0  # Guessing for a socket head cap screw
clamp_counterbore_depth = 5.0

# --- Geometry Construction ---

# 1. Base Block
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Central Bore
result = result.faces(">Z").workplane().hole(bore_diameter)

# 3. Transverse Hole (Front Face)
# This hole goes through the side. In the image, it's on the right face.
result = (result.faces(">X").workplane()
          .center(0, 0) # Centered on the face
          .hole(transverse_hole_diameter))

# 4. The Clamping Slot
# This is a slit cut from one side (left in image, -X direction) towards the center.
# The slot cuts through the entire height.
result = (result.faces("<X").workplane()
          .center(0, 0) # Center of the left face
          .rect(thickness * 2, slot_width) # Height is exaggerated to ensure cut
          .cutBlind(slot_length_from_edge))

# 5. The Rectangular Side Pocket (on the -X face)
# This creates the recess for the clamping mechanism.
result = (result.faces("<X").workplane()
          .center(0, 0)
          .rect(side_pocket_height, side_pocket_width) # Note orientation on the face plane
          .cutBlind(side_pocket_depth))

# 6. Clamping Screw Holes (on the -X face)
# These holes go through the "fingers" created by the slot.
# We need two holes on the -X face, above and below the slot.
clamp_hole_offset = 8.0 # Distance from center line (slot)
clamp_hole_x_pos = -width/2 + 6.0 # Depth from the edge

# Create top clamp hole
result = (result.faces("<X").workplane()
          .center(0, clamp_hole_offset)
          .cboreHole(clamp_hole_dia, clamp_counterbore_dia, clamp_counterbore_depth, depth=side_pocket_depth + 5.0))

# Create bottom clamp hole
result = (result.faces("<X").workplane()
          .center(0, -clamp_hole_offset)
          .cboreHole(clamp_hole_dia, clamp_counterbore_dia, clamp_counterbore_depth, depth=side_pocket_depth + 5.0))

# 7. Top Mounting Holes
# Four main corner holes
result = (result.faces(">Z").workplane()
          .rect(mount_hole_spacing_x, mount_hole_spacing_y, forConstruction=True)
          .vertices()
          .hole(mount_hole_dia))

# Two additional holes near the split (left side)
extra_holes_x_offset = -length/2 + 15.0
extra_holes_y_spacing = 30.0
result = (result.faces(">Z").workplane()
          .center(extra_holes_x_offset, 0)
          .rect(0, extra_holes_y_spacing, forConstruction=True) # Trick to get two points
          .vertices()
          .hole(mount_hole_dia))

# 8. Small detail: Keyway/Notch inside the main bore
# The image shows a small square notch at the bottom of the main bore.
keyway_width = 6.0
keyway_height = 4.0
result = (result.faces(">Z").workplane()
          .center(0, -bore_diameter/2) # Position at the bottom edge of the bore
          .rect(keyway_width, keyway_height*2) # Rectangle centered on edge
          .cutBlind(-thickness))

# 9. Center hole for tensioner/aligner?
# There is a small hole right near the slot on the top surface.
result = (result.faces(">Z").workplane()
          .center(-length/4 + 2, 0) 
          .hole(mount_hole_dia))
          
# 10. Inner Clamping mechanism detail
# Inside the side pocket, there appears to be a cylindrical boss or screw head detail.
# Let's add a cylinder inside that pocket to represent the screw/mechanism.
# We select the back face of the pocket we just cut.
# Since selecting based on history can be tricky, let's locate relative to global coords.
# The pocket was cut into the -X face.
pocket_back_x = -length/2 + side_pocket_depth
result = (result.faces("<X").workplane(offset=-side_pocket_depth)
          .center(0,0)
          # A simple cylinder to represent the hardware inside
          .circle(4).extrude(side_pocket_depth - 2)) 

# Final result is stored in 'result' variable