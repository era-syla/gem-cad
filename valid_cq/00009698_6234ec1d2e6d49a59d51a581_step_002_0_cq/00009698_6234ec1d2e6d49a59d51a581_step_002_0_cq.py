import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
overall_length = 60.0  # Length along the X axis
overall_width = 40.0   # Width along the Y axis
base_thickness = 5.0   # Thickness of the main flat base

# Right-side block/channel dimensions
block_width = 20.0     # Width of the thicker section on the right
block_height = 20.0    # Total height of the right block
channel_thickness = 5.0 # Wall thickness of the channel feature

# Boss dimensions
boss_diameter = 25.0
boss_height = 2.0      # Height of the boss above the base surface
hole_diameter = 12.0

# --- Modeling ---

# 1. Create the base plate (the left part)
# We will center the whole assembly roughly for easier positioning later, 
# or build from left to right. Let's build from the origin.
# The base plate spans the full length initially, then we'll modify the right side.

# Let's start with the flat base section on the left.
# Length is roughly overall_length - block_width if we think of them as separate,
# but it's cleaner to make the base shape L-shaped or just union shapes.

# Base plate part
base = cq.Workplane("XY").box(overall_length, overall_width, base_thickness)

# 2. Create the right-side "C-channel" or block feature.
# Looking at the image, there is a distinct gap/undercut.
# It looks like a C-channel attached to the side, or an extrusion with a cutout.
# Let's model the right block.
right_block = (
    cq.Workplane("XY")
    .workplane(offset=block_height/2 - base_thickness/2) # align bottom relative to base center
    .box(block_width, overall_width, block_height)
    .translate((overall_length/2 - block_width/2, 0, (block_height - base_thickness)/2))
)

# 3. Create the cutout in the right block to make it a C-shape/channel.
# The cutout goes through the side (Y-axis) based on the profile visible.
# Wait, looking closely at the image:
# The base plate continues under the "overhang".
# It looks like a Z-section or a clip.
# Left part is flat. Right part goes UP, then RIGHT (or LEFT depending on view).
# Actually, it looks like a rectangular tube or C-channel where the top leg is longer than the bottom leg?
# No, simpler interpretation:
# A flat plate of size (Length x Width x Thickness).
# On the right side, there is an upper structure.
# Let's re-evaluate the profile from the side (XZ plane).
# It looks like an 'h' shape or a reversed 'h'.
# Let's sketch the profile on the XZ plane and extrude it along Y.

# Profile sketch points (starting bottom-left of the profile, moving counter-clockwise):
# 1. (0, 0)
# 2. (overall_length, 0)
# 3. (overall_length, block_height)
# 4. (overall_length - block_width, block_height)
# 5. (overall_length - block_width, base_thickness + channel_gap) 
#    Wait, there is a gap between the top flange and the bottom base?
#    Looking at the shadow, yes.
#    Let's assume the top flange is `channel_thickness` thick.
#    Let's assume the vertical web is `channel_thickness` thick.
#    
#    Let's try a constructive solid geometry (CSG) approach, it's often more robust for simple shapes.

# Part A: The main base plate
part_a = cq.Workplane("XY").box(overall_length, overall_width, base_thickness)

# Part B: The vertical wall on the right side
# Position: centered on Y, offset in X to be at the right edge, sitting on top of base
vertical_wall = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .box(channel_thickness, overall_width, block_height - base_thickness)
    .translate((overall_length/2 - channel_thickness/2, 0, (block_height - base_thickness)/2))
)

# Part C: The top flange extending back to the left
# Position: Top of the vertical wall, extending leftwards
top_flange_length = block_width
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=block_height - base_thickness/2 - (block_height - base_thickness)) # Reset to Z=0
    .workplane(offset=base_thickness/2 + (block_height - base_thickness) - channel_thickness/2) # Move to top center
    .box(top_flange_length, overall_width, channel_thickness)
    .translate((overall_length/2 - top_flange_length/2, 0, 0))
)

# However, looking at the image very closely, the rightmost face is flush.
# The "C" shape is formed by the base, a vertical wall at the right edge, and a top flange.
# But the image shows the top flange OVERLAPPING the base.
# And there's a gap between the base and the top flange.
# Let's adjust dimensions to match visual proportions.
# Let's use a single sketch extrusion for the main body profile.

# Defined on XZ plane (Front view), extruded along Y (Width)
# Origin at bottom-left corner of the profile
pts = [
    (0, 0),                                     # Bottom-left of base
    (overall_length, 0),                        # Bottom-right of base
    (overall_length, block_height),             # Top-right outer corner
    (overall_length - block_width, block_height), # Top-left of top flange
    (overall_length - block_width, block_height - channel_thickness), # Bottom-left of top flange
    (overall_length - channel_thickness, block_height - channel_thickness), # Inner corner top
    (overall_length - channel_thickness, base_thickness), # Inner corner bottom
    (0, base_thickness),                        # Top-left of base
    (0, 0)                                      # Close
]

main_body = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(overall_width/2, both=True) # Extrude symmetrically along Y
)

# 4. Create the Boss and Hole
# The boss sits on the top face of the base section (the lower level).
# We need to find the center of the available flat area on the left.
# Available length on left = overall_length - block_width (roughly)
# Let's center it in that area.

left_section_length = overall_length - block_width
# Center of the boss relative to the global origin (which is at bottom-left-center of extrusion)
# X coordinate: The extrusion started at X=0. The left section ends at X=overall_length - block_width.
# So center X = left_section_length / 2.
boss_center_x = left_section_length / 2
# Z coordinate: The boss sits on the base, which is base_thickness high.

# Create Boss
boss = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(boss_center_x, 0) # Relative to center. 
    # Wait, the extrusion was based on origin at bottom-left XZ.
    # The default workplane center is (0,0,0).
    # Since we extruded along Y symmetrically, Y=0 is the center.
    # X=0 is the left edge.
    # So we need to move X to boss_center_x.
    .transformed(offset=cq.Vector(boss_center_x - overall_length/2, 0, 0)) 
    # Workplane default origin is center of bounding box? No.
    # Let's be explicit with coordinates.
)

# Actually, it's safer to select the face.
base_face_selector = main_body.faces("<Z").workplane(offset=base_thickness)
# The X range of the flat part is 0 to (overall_length - channel_thickness).
# But visually the boss is centered in the open area.
# Open area X range: 0 to (overall_length - block_width).
# Center X = (overall_length - block_width) / 2.

boss_x_pos = (overall_length - block_width) / 2

main_body_with_boss = (
    main_body
    .faces(">Z[1]") # Select the lower "top" face (the base plate surface)
    .workplane(centerOption="CenterOfMass") # This centers on the face selected
    # The face selected is the long strip on the left.
    # Its center of mass is exactly where we want the boss generally.
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 5. Create the through hole
# Hole goes through the boss and the base.
result = (
    main_body_with_boss
    .faces(">Z") # Select the very top face of the boss
    .workplane() 
    .circle(hole_diameter / 2)
    .cutBlind(-100) # Cut through everything downwards
)

# The result variable is required