import cadquery as cq

# --- Parameter Definitions ---
disk_diameter = 200.0   # Diameter of the main disk
disk_thickness = 5.0    # Thickness of the disk
center_hole_diam = 5.0  # Diameter of the central hole

# Slot parameters
slot_width = 12.0       # Width of the rectangular slot
slot_length = 30.0      # Length of the rectangular slot
slot_depth = 2.0        # Depth of the cut into the disk
slot_offset = 85.0      # Distance from center to the center of the slot
num_slots = 4           # Number of slots

# Ridge parameters (the raised feature inside the slot)
ridge_width = 2.0       # Width of the small ridges inside the slot
ridge_height = slot_depth # Height of ridges (flush with top surface or slightly recessed)
num_ridges = 2          # Two ridges per slot

# --- Geometry Construction ---

# 1. Create the base disk
result = cq.Workplane("XY").circle(disk_diameter / 2).extrude(disk_thickness)

# 2. Cut the center hole
result = result.faces(">Z").workplane().hole(center_hole_diam)

# 3. Create the slots with ridges
# We'll create a single slot shape first, then use polarArray to distribute it.

def create_slot_feature(loc):
    # This function creates the negative volume for one slot 
    # and leaves the positive volume for the ridges.
    
    # Define the base rectangle for the slot cut
    slot_cut = (
        cq.Workplane("XY")
        .rect(slot_length, slot_width)
        .extrude(slot_depth)
    )
    
    # Define the ridges. We want two parallel ridges running along the length.
    # We can model them as a single object to subtract from the cut, 
    # or just model the specific shape to cut.
    # A cleaner way: Cut the full rectangle, then add the ridges back.
    
    # Let's model the shape to REMOVE.
    # It's a rectangle minus the two ridges.
    
    # Distance between ridge centers
    ridge_spacing = slot_width / 3.0 
    
    # Left ridge
    r1 = (
        cq.Workplane("XY")
        .center(-0, -ridge_spacing/2) # Centered on Y
        .rect(slot_length, ridge_width)
        .extrude(slot_depth)
    )
    # Right ridge
    r2 = (
        cq.Workplane("XY")
        .center(-0, ridge_spacing/2)
        .rect(slot_length, ridge_width)
        .extrude(slot_depth)
    )
    
    ridges = r1.union(r2)
    
    # The final shape to CUT is the slot_cut MINUS the ridges
    # Wait, CadQuery Boolean operations are usually done on the main solid.
    # Let's do it directly on the main workplane using a custom cut shape.
    
    return slot_cut.cut(ridges).val().moved(loc)

# Create the cutting tool for all 4 slots
# We position the slots radially. The 'slot_length' is aligned radially.
slot_tool = (
    cq.Workplane("XY")
    .polarArray(radius=slot_offset, startAngle=0, angle=360, count=num_slots, fill=True)
    .eachpoint(create_slot_feature)
)

# Cut the slots from the main disk
# We need to make sure the tool is positioned correctly in Z.
# The disk top is at Z = disk_thickness. The tool was extruded from Z=0 to Z=slot_depth.
# We need to move the tool up so its top aligns with the disk top, 
# or simply cut from the top face down.

# Let's recreate the logic simpler:
# 1. Select top face.
# 2. Use polar array.
# 3. For each point, draw the profile of the slot (rectangle) and cut.
# 4. Then draw the profile of the ridges (rectangles) and extrude (add material back).

# Step 3: Cut the main rectangular slots
result = (
    result.faces(">Z").workplane()
    .polarArray(radius=slot_offset, startAngle=0, angle=360, count=num_slots)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Step 4: Add the ridges back inside the slots
# We need two ridges per slot.
ridge_spacing = slot_width / 3.5

# Ridge 1 (inner/upper relative to slot center)
result = (
    result.faces(">Z").workplane() # Workplane on top of disk
    .polarArray(radius=slot_offset, startAngle=0, angle=360, count=num_slots)
    .rect(slot_length, ridge_width) # This creates a rect at the center of the slot
    .translate((0, ridge_spacing))  # Shift it in local Y (which rotates with polar array context? No, usually not in standard chain)
    # The translate inside polarArray context can be tricky.
    # Let's use a composite shape approach for the sketch instead.
)

# Reset and try a cleaner sketch-based approach for the ridges to ensure alignment
result = cq.Workplane("XY").circle(disk_diameter / 2).extrude(disk_thickness)
result = result.faces(">Z").workplane().hole(center_hole_diam)

# Iterate to cut slots and add ridges
for i in range(num_slots):
    angle = i * (360.0 / num_slots)
    
    # Create a workplane rotated to the correct angle
    wp = (
        result.faces(">Z").workplane()
        .transformed(rotate=(0, 0, angle))
        .center(slot_offset, 0)
    )
    
    # Cut the main slot
    result = wp.rect(slot_length, slot_width).cutBlind(-slot_depth)
    
    # Add ridges back
    # Ridge 1
    result = (
        result.faces(">Z").workplane()
        .transformed(rotate=(0, 0, angle))
        .center(slot_offset, slot_width/4) # Approximate spacing
        .rect(slot_length, ridge_width)
        .extrude(-slot_depth + 0.5) # Make them slightly lower than surface or just up from bottom? Image shows flush.
        # Actually, simpler to just cut the 'grooves' instead of slot+ridge.
    )
    # Let's rethink: The feature is 3 parallel grooves or 2 ridges.
    # Looking at the image, it looks like a rectangular recess with two raised ribs inside.
    # Or, it's three narrow slots side-by-side. 
    # Let's assume it's a rectangular pocket with 2 ribs.
    
    # Re-doing the add-back logic to be robust:
    # We are adding material from the BOTTOM of the cut we just made.
    # The bottom of the cut is at Z = disk_thickness - slot_depth.
    
    # Define ridge height (same as depth for flush)
    h_ridge = slot_depth
    
    # Ridge 1 geometry
    result = (
        result.faces(">Z").workplane() # Top surface
        .transformed(rotate=(0,0,angle))
        .center(slot_offset, slot_width/4.0)
        .rect(slot_length, ridge_width)
        .extrude(-slot_depth, combine="cut") # Oh wait, if I cut, I remove material. 
        # If I want to make the "groove" look, I should cut 3 separate rectangles instead of 1 big one.
    )

# --- Final Refined Approach: Cut 3 grooves to leave 2 ridges ---
# This is much more robust than cutting and adding back.
# The "Slot" is visually composed of three parallel indentations.
# Or, a wide indentation with two thin strips remaining at original height?
# The image shows the ridges are RECESSED slightly or FLUSH.
# They look flush with the top surface.
# So, the geometry is actually just 3 parallel slots cut into the disk per location.

# Re-initialize
result = cq.Workplane("XY").circle(disk_diameter / 2).extrude(disk_thickness)
result = result.faces(">Z").workplane().hole(center_hole_diam)

groove_width = 2.0
groove_len = 30.0
groove_depth = 1.5
# Total width of the feature is about 12mm. 
# Center groove + 2 side grooves?
# The image shows two thin ridges. This implies 3 dark areas (cuts).
# Cut 1 (Top), Cut 2 (Middle), Cut 3 (Bottom) inside the grouping.

# Let's parametrize the cutting of 3 parallel rectangles.
gap_between_grooves = 2.0 # Thickness of the ridge
total_group_width = (3 * groove_width) + (2 * gap_between_grooves) # ~10mm

for i in range(num_slots):
    angle = i * 90
    
    # We will create a local workplane for the group of cuts
    wp = (
        result.faces(">Z").workplane()
        .transformed(rotate=(0, 0, angle))
        .center(slot_offset, 0)
    )
    
    # Center cut
    result = wp.rect(groove_len, groove_width).cutBlind(-groove_depth)
    
    # Upper cut (Y+)
    result = (
        result.faces(">Z").workplane()
        .transformed(rotate=(0, 0, angle))
        .center(slot_offset, groove_width + gap_between_grooves)
        .rect(groove_len, groove_width)
        .cutBlind(-groove_depth)
    )
    
    # Lower cut (Y-)
    result = (
        result.faces(">Z").workplane()
        .transformed(rotate=(0, 0, angle))
        .center(slot_offset, -(groove_width + gap_between_grooves))
        .rect(groove_len, groove_width)
        .cutBlind(-groove_depth)
    )

# Export or display is handled by the environment, 'result' is the variable needed.