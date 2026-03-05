import cadquery as cq

# Parametric Dimensions
# Main block dimensions
base_length = 50.0  # Overall length of the main protruding arm
base_width = 20.0   # Width of the main arm
base_height = 15.0  # Height of the main arm

# Rear vertical block (the mounting part)
rear_width = 30.0   # Width of the wider rear section
rear_height = 30.0  # Total height of the rear section
rear_thickness = 10.0 # Thickness of the rear block

# Front tip details
tip_length = 10.0    # Length of the pointed tip section
tip_width = base_width # Starts at base width
tip_chamfer = 5.0    # Amount to chamfer the top corners near the tip

# Cutout details on the rear block
top_slot_width = 12.0
top_slot_depth = 5.0

# Hole details
hole_diameter = 5.0
hole_dist_from_rear = 15.0 # Distance from the junction with the rear block

# Create the Rear Vertical Block
# We will center it on X=0 for symmetry
rear_block = (
    cq.Workplane("XY")
    .box(rear_width, rear_thickness, rear_height)
    .translate((0, -rear_thickness/2, rear_height/2))
)

# Create the Top Slot on the Rear Block
rear_block_slotted = (
    rear_block
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(top_slot_width, rear_thickness)
    .cutBlind(-top_slot_depth)
)

# Create the Main Horizontal Arm
# This extends from the front face of the rear block
arm = (
    cq.Workplane("XY")
    .box(base_width, base_length, base_height)
    .translate((0, base_length/2, base_height/2))
)

# Create the Tip
# The tip looks like a wedge. We can create it by lofting or cutting.
# Let's try creating a basic prism shape for the tip and adding it to the arm.
# Actually, the image shows the arm itself tapers or has a specific wedge shape at the end.
# Let's model the arm as a single extrusion with a specific profile or just cut the box.

# Let's refine the Arm + Tip strategy:
# 1. Start with the main arm block.
# 2. Add the pointed tip.
# 3. Apply the side chamfers/cuts.

# Simpler approach for the tip geometry seen in image:
# It looks like a wedge attached to the end.
# Let's make the tip a separate wedge and union it, or cut the arm.
# Looking closely, the tip has a vertical face, then a slope down.
# And the sides near the tip are chamfered.

# Let's build the arm + tip as one sketch extrusion for the side profile?
# No, the top view shape is complex too.

# Method: Constructive Solid Geometry (CSG)
# 1. Combine Rear Block and Main Arm
main_body = rear_block_slotted.union(arm)

# 2. Create the wedge shape at the tip.
# The tip extends further than 'base_length'. 
# Let's say the base_length includes the rectangular part, and we add a triangle.
tip_wedge = (
    cq.Workplane("YZ")
    .workplane(offset=base_width/2) # Start at one side
    .moveTo(base_length, 0) # Bottom right of arm
    .lineTo(base_length + tip_length, 0) # Tip point
    .lineTo(base_length, base_height/2) # Mid-height on face
    .close()
    .extrude(-base_width) # Extrude across width
)

# The tip in the image actually looks like the bottom face is flat, 
# and the top face slopes down to a sharp edge.
# Let's redefine the tip cut.
# We will cut the existing arm to form the tip.
# Extend the arm length first to include the tip area.
total_arm_length = base_length + tip_length
arm_extended = (
    cq.Workplane("XY")
    .box(base_width, total_arm_length, base_height)
    .translate((0, total_arm_length/2, base_height/2))
)
combined_raw = rear_block_slotted.union(arm_extended)

# Cut the slope on the tip
# Define a cutting wedge
cut_plane_angle = (
    cq.Workplane("YZ")
    .workplane(offset=20) # Move out of the way
    .moveTo(base_length, base_height) # Top of the straight section
    .lineTo(total_arm_length, 0)      # The very tip at bottom
    .lineTo(total_arm_length, base_height + 5) # Go high
    .lineTo(base_length, base_height + 5)
    .close()
    .extrude(-40) # Cut across
)

result_step1 = combined_raw.cut(cut_plane_angle)

# Apply Side Chamfers to the front section
# The image shows 45-degree chamfers on the vertical corners where the tip starts.
# We need to select the vertical edges at y = base_length
# However, the tip itself is now a wedge. The chamfers appear to be on the
# transition from the straight arm to the tip.

# Let's try selecting the vertical edges at the "shoulder" of the tip.
# This might be tricky with selectors. Let's make a cutting tool for the side chamfers.

chamfer_cut_left = (
    cq.Workplane("XY")
    .moveTo(-base_width/2, base_length)
    .lineTo(-base_width/2 + tip_chamfer, base_length + tip_chamfer)
    .lineTo(-base_width/2 - 5, base_length + tip_chamfer + 5) # Outer
    .lineTo(-base_width/2 - 5, base_length)
    .close()
    .extrude(base_height)
)

chamfer_cut_right = (
    cq.Workplane("XY")
    .moveTo(base_width/2, base_length)
    .lineTo(base_width/2 - tip_chamfer, base_length + tip_chamfer)
    .lineTo(base_width/2 + 5, base_length + tip_chamfer + 5) # Outer
    .lineTo(base_width/2 + 5, base_length)
    .close()
    .extrude(base_height)
)

result_step2 = result_step1.cut(chamfer_cut_left).cut(chamfer_cut_right)

# Add the Hole in the side of the arm
# Hole is on the YZ plane (side of the arm)
result = (
    result_step2
    .faces(">X") # Select the right side face of the arm (or rear block)
    .workplane()
    # We need to position relative to the arm start (Y=0)
    # The workplane center is likely at the center of the face bounding box.
    # It's safer to use absolute coordinates or reference the global origin.
    .transformed(offset=(0,0,0), rotate=(0,0,0)) # Reset to global alignment somewhat
    .center(hole_dist_from_rear, base_height/2)
    .circle(hole_diameter/2)
    .cutBlind(-base_width) # Cut through the arm width
)

# Final cleanup/Fillets if needed (image looks fairly sharp except specifically designed chamfers)
# Re-orient for better viewing if exported, but 'result' is the standard variable.