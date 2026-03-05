import cadquery as cq

# Parametric dimensions
total_length = 80.0
width = 12.0
height = 8.0

# Fork/Slot dimensions
slot_length = 35.0
slot_width = 4.0

# Wedge/Taper dimensions
taper_length = 35.0
tip_height = 3.0  # Height at the very tip of the wedge

# Derived values
straight_section_length = total_length - taper_length

# Create the main body
# We'll start with the profile of the wedge and the straight section from the side view
# Then extrude it to the width.

# Define the points for the side profile
# Origin (0,0) is at the bottom-back corner (the thick end)
pts = [
    (0, 0),                           # Bottom-back corner
    (straight_section_length, 0),     # Start of taper on bottom
    (total_length, 0),                # Tip bottom
    (total_length, tip_height),       # Tip top
    (straight_section_length, height),# Start of taper on top
    (0, height)                       # Top-back corner
]

# Create the base solid
base = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(width/2.0, both=True) # Extrude symmetrically along Y
)

# Create the slot (fork) at the back end
# The slot cuts through the thick part
# It looks like a slot with rounded ends, essentially a "slot" operation
result = (
    base
    .faces("<X")             # Select the back face
    .workplane()
    .center(0, 0)            # Center on the face
    .slot2D(slot_length * 2, slot_width, 90) # Cut a slot. Length is doubled because we only need it to go in one way, but slot2D centers.
                                             # Alternatively, we can just cut a rectangle if the end isn't rounded inside.
                                             # Looking closer at the image, the internal end of the slot looks rounded.
    .cutBlind(-slot_length)  # Cut into the part
)

# Optional: Fillet the transition between the wedge and the straight part if needed, 
# but the image shows a relatively sharp transition line. 
# We will leave it sharp as per the typical geometric interpretation of such diagrams unless a fillet is obvious.
# The transition at the bottom (straight_section_length, 0) looks like it might have a very small curve or just be a sharp angle.
# I will adhere to the polyline definition which creates sharp edges.

# Ensure the slot orientation is correct.
# The slot is horizontal relative to the width. 
# Let's re-verify the slot cut.
# base is extruded along Y. <X face is the flat back face.
# On the <X face (YZ plane essentially), the slot width should be along Y.
# The slot2D command takes (length, diameter, angle).
# If angle=0, length is along X of the workplane.
# On the <X workplane, X is likely global Y and Y is global Z.
# Let's use a simpler rect cut with fillets to be precise about orientation.

result = (
    base
    .faces("<X")
    .workplane()
    # The workplane on <X has its X axis along global Y (width) usually, and Y axis along global Z (height).
    .rect(slot_width, height + 2) # Cut a rectangle vertically through the center? No, the slot is horizontal.
    # The image shows the slot cutting horizontally through the width of the part?
    # No, wait. The image shows a side view. The slot is in the middle of the thickness.
    # Let's look at the "fork" end. The slot creates two prongs.
    # The slot is visible on the side face in the image? No, the slot is in the back.
    # The visible hole on the side suggests the slot goes all the way through side-to-side?
    # Rereading the image: The slot is longitudinal. It splits the thick end into top and bottom halves? 
    # Or left and right halves?
    # If I look at the end, it looks like a "U" shape or a fork.
    # The dark area inside the side suggests the cut goes deep.
    # The shadow implies the slot separates the part into two vertical walls.
    # Let's assume the slot creates two parallel plates (left and right).
    # So the cut is vertical (along Z) if looking from top, or horizontal if looking from back?
    
    # Interpretation A: The slot splits the width. (Left prong, Right prong).
    # Interpretation B: The slot splits the height. (Top prong, Bottom prong).
    
    # Looking at the shadow/shading inside the slot on the side face (the long face), 
    # it looks like a through-slot from side to side? 
    # No, that's a "long hole" or "slot" cut into the side.
    # Wait, looking closer at the "fork" end (top right of image).
    # It creates a C-shape or U-shape profile.
    # The slot runs along the length of the part.
    # If the slot was cutting the height, we would see a gap between top and bottom surfaces.
    # If the slot was cutting the width, we would see a gap between left and right surfaces.
    # The image shows a gap between LEFT and RIGHT.
    # Therefore, the slot width is along the Y axis (width dimension).
    
    # Correction: The previous slot logic `slot2D(slot_length * 2, slot_width, 90)` might have been trying to cut along the height.
    # Let's rebuild the cut more explicitly.
    
    .rect(slot_width, height * 2) # Cut a wide rectangle in the middle? No that cuts the whole back off.
    
    # Let's try a different approach for the cut.
    # We want to remove material in the center of the block, starting from the back face.
    # The material removed has width = slot_width.
    # The material removed has height = total height (it's a through cut top-to-bottom? No.)
    
    # Let's look at the reflection/shadow. 
    # Actually, looking at the crop, there is a rounded end INSIDE the part.
    # This is a classic "clevis" or "fork" end.
    # Usually, the slot is vertical, allowing a flat plate to insert.
    # So the cut is a vertical slot.
    # Dimensions: 
    # Cut Width = slot_width (along the 12mm width axis).
    # Cut Height = through all (along the 8mm height axis).
    # Cut Depth = slot_length (along the 80mm length axis).
    
    # If it's a vertical slot, the "fork" creates a left wall and a right wall.
    # The slot ends with a full radius or flat? The image shows a rounded termination.
)

# Re-doing the slot cut with the specific interpretation:
# Vertical slot cutting through the height, entering from the back, creating two side walls.
result = (
    base
    .faces("<X")             # Back face
    .workplane()
    .center(0, 0)
    # We are drawing on the YZ plane (effectively).
    # X of workplane is Y of world (Width).
    # Y of workplane is Z of world (Height).
    # We want a slot that is `slot_width` wide and goes through the full height.
    # However, standard `slot2D` makes a shape with rounded ends.
    # We want the cut to be open at the back and rounded at the inner end.
    # A simple way is to cut a rectangle + a cylinder, or use a slot primitive moved correctly.
    
    # Let's use a simple cut box for the main channel and a cylinder for the rounded end.
    .rect(slot_width, height * 2) # Rectangle width=slot_width, height=oversized
    .cutBlind(-slot_length)       # Cut into the part
)

# Now add the rounded internal end of the slot.
# We need to cut a cylinder at X = (total_length - straight_section_length + (straight_section_length - slot_length))?
# Easier to position relative to global coords.
# The slot starts at X=0 and goes to X=slot_length.
# The end of the rectangular cut is at X=slot_length.
# We need a cylinder at X=slot_length, radius = slot_width/2.
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=0) # Bottom plane
    .moveTo(slot_length, 0)
    .circle(slot_width / 2.0)
    .extrude(height)
)

# Wait, looking at the image again very carefully.
# There is a feature on the SIDE of the part.
# It's an elongated slot (racetrack shape) cut THROUGH the side wall?
# Or is it a depression?
# It looks like the slot I just modeled (the fork) is actually horizontal?
# Let's look at the orientation of the wedge.
# The wedge tapers in height (Z).
# The fork is at the thick end.
# If the fork was vertical (left/right walls), we would see the top face as solid.
# The top face in the image appears solid. 
# The SIDE face shows a dark shape.
# That dark shape is the gap between the top prong and bottom prong.
# Therefore: **The slot is horizontal.** It splits the part into a Top and Bottom half.
# My previous "Vertical slot" theory was likely wrong.
# If the slot splits Top/Bottom, we see the gap from the side view. The image shows exactly this.
# The rounded end of the slot is visible inside the part.

# Revised Geometry Plan:
# 1. Base shape (Wedge profile extruded).
# 2. Horizontal slot cut from the back end.
#    - Width of cut: `slot_width` (this is now the vertical dimension of the gap).
#    - Width of cut (transverse): Through the whole width (12mm) of the part?
#    - No, looking at the end face (right side of image), it looks like a C-channel?
#    - Or does it go all the way through?
#    - Usually, these are clevis joints. 
#    - If I look at the "dark shape" on the side face. It has a border.
#    - This implies it does NOT go all the way through the width. It is a slot cut into the side?
#    - No, that's unlikely for a wedge clamp.
#    - Let's look at the very end face (top right).
#    - We see the top surface, the side surface, and the end surface.
#    - The end surface has a cut out.
#    - The cut out seems to go from left side to right side (through the width).
#    - This would define a fork with a Top leg and a Bottom leg.
#    - This matches the side view showing a "hole" or "gap" running along the length.
#    - The gap has a rounded end.

# Final Geometry Plan:
# 1. Profile in XZ plane (Wedge).
# 2. Extrude Y (Width).
# 3. Cut a slot from the back face (X=0).
#    - The slot is in the XY plane (horizontal).
#    - It enters from X=0.
#    - It goes deep into the part (slot_length).
#    - It has a specific height (slot_gap).
#    - It goes all the way through the Width (Y).

# Dimensions for this plan:
slot_gap = 4.0   # The vertical opening size
slot_depth = 35.0 # How deep it goes
slot_end_radius = slot_gap / 2.0

# Reset result construction
# Create profile on XZ plane
pts = [
    (0, 0),                           # Bottom-back
    (straight_section_length, 0),     # Bottom-taper-start
    (total_length, 0),                # Tip-bottom
    (total_length, tip_height),       # Tip-top
    (straight_section_length, height),# Top-taper-start
    (0, height)                       # Top-back
]

base = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(width/2.0, both=True)
)

# Create the horizontal slot
# We cut from the side (Side view projection) or just subtract a shape.
# Let's subtract a "racetrack" extruded in Y.
# The racetrack is in the XZ plane.
# Center of the slot height-wise: height / 2.
# Center of the slot length-wise: It starts at X=0.
# The inner end is at X = slot_depth.
# The shape to cut is a rectangle from 0 to slot_depth, plus a circle at slot_depth.

cutter_profile = (
    cq.Workplane("XZ")
    .moveTo(0, height/2.0)
    .lineTo(slot_depth, height/2.0) # Line to center of rounded end
    # We need a shape.
    # Let's outline the cut area
    .moveTo(0, height/2.0 - slot_gap/2.0)
    .lineTo(slot_depth, height/2.0 - slot_gap/2.0) # Bottom edge
    .threePointArc((slot_depth + slot_gap/2.0, height/2.0), (slot_depth, height/2.0 + slot_gap/2.0)) # End arc
    .lineTo(0, height/2.0 + slot_gap/2.0) # Top edge
    .close()
)

# Extrude the cutter and subtract
result = base.cut(cutter_profile.extrude(width/2.0 + 1.0, both=True)) 
# width/2 + 1 to ensure it cuts through completely