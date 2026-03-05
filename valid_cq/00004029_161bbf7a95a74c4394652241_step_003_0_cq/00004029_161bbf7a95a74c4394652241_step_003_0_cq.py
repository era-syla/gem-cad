import cadquery as cq

# --- Parameters ---
# Based on visual estimation, this appears to be a 2040 (20mm x 40mm) T-slot extrusion.
# These are common dimensions for V-Slot or T-Slot profiles.
width = 40.0
depth = 20.0
length = 300.0  # Arbitrary length based on aspect ratio
slot_width = 6.0  # Standard slot width for 20-series
wall_thickness = 1.5
center_hole_dia = 5.0
corner_radius = 1.0

# --- Helper Function: Single T-Slot Profile ---
# We will create one 20x20 cell and then mirror/duplicate it to make the 2040.
def create_2020_profile_sketch():
    s = (
        cq.Sketch()
        .rect(20, 20)  # Base square
        .vertices()
        .fillet(corner_radius)
        
        # Create the center hole
        .circle(center_hole_dia / 2, mode='s')
        
        # Create the T-slots
        # We define one slot shape and subtract it from the 4 sides
        .push([(0, 10), (0, -10), (10, 0), (-10, 0)])
        .rect(slot_width, 5.0, mode='s') # Basic slot opening
        .clean()
    )
    
    # Refine the T-slot shape (internal widening)
    # A proper T-slot has a "T" shape cut out. 
    # Let's subtract the inner wide part of the T-slot
    inner_slot_width = 10.0 # wider part inside
    inner_slot_depth = 2.0  # depth of the wider part
    slot_entry_depth = 1.5 # depth before it widens
    
    # Coordinates for the internal cutouts relative to center (0,0)
    # Top slot internal
    s = s.push([(0, 10 - slot_entry_depth - inner_slot_depth/2)]) \
         .rect(inner_slot_width, inner_slot_depth, mode='s')
    
    # Bottom slot internal
    s = s.push([(0, -10 + slot_entry_depth + inner_slot_depth/2)]) \
         .rect(inner_slot_width, inner_slot_depth, mode='s')
         
    # Right slot internal
    s = s.push([(10 - slot_entry_depth - inner_slot_depth/2, 0)]) \
         .rect(inner_slot_depth, inner_slot_width, mode='s')
         
    # Left slot internal
    s = s.push([(-10 + slot_entry_depth + inner_slot_depth/2, 0)]) \
         .rect(inner_slot_depth, inner_slot_width, mode='s')
    
    # Corner voids (weight reduction)
    corner_void_size = 3.0
    s = s.push([(5.5, 5.5), (5.5, -5.5), (-5.5, 5.5), (-5.5, -5.5)]) \
         .circle(corner_void_size/2, mode='s')

    return s

# --- Assembly Construction ---

# Create the base sketch for one 20x20 section
profile_sketch = create_2020_profile_sketch()

# We need a 20x40 profile. This is essentially two 20x20s side-by-side.
# However, the internal wall where they join is often a single wall, not double.
# For simplicity and visual accuracy of the *outer* shape shown in the image,
# we can place two sketches and extrude them.

# Extrude the first section
part_left = cq.Workplane("XY").placeSketch(profile_sketch).extrude(length)

# Extrude the second section, shifted by 20mm
part_right = (
    cq.Workplane("XY")
    .center(0, 20) # Shift position for the second block
    .placeSketch(profile_sketch)
    .extrude(length)
)

# Combine them into a single object
result = part_left.union(part_right)

# The image shows a black section in the middle, likely a V-slot wheel or a cover.
# However, the prompt asks for the CAD model of the object. 
# The object shown is a single extrusion piece with a visual texture applied in the middle 
# (often indicating a specific finish or highlighting the V-groove area).
# Since CadQuery generates geometry, not texture maps, we return the geometric solid.

# Rotate to match the vertical orientation in the image
# The image shows the long dimension (40mm) facing us, standing upright.
# Currently Z is length. 
# Let's orient it so the 40mm face is roughly aligned with the view.
# Our current cross section is on XY plane. The 2040 is 20 wide (X) and 40 tall (Y).
# The extrusion is along Z.
# The image shows the extrusion standing up.

# The result is already standing up along Z.