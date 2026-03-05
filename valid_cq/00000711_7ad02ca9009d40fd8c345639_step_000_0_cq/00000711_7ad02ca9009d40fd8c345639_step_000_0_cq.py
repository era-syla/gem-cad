import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions of the plate
plate_length = 150.0
plate_height = 40.0
plate_thickness = 2.0

# Dimensions for the central horizontal slot/groove
# Looking at the image, it appears to be a shallow groove rather than a through-hole,
# but often these are reinforcement ribs or slots. I will model it as a through-slot
# based on common bracket designs, but parameterized so depth can be changed easily.
# If it's a groove, set cut_depth < plate_thickness.
center_slot_length = 100.0
center_slot_width = 2.0
center_slot_depth = 1.0 # Partial depth groove based on visual cue

# Dimensions for the vertical side slots
side_slot_height = 20.0
side_slot_width = 3.0
side_slot_margin = 8.0 # Distance from edge to center of slot

# --- Geometry Construction ---

# 1. Create the base plate
base = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Create the central horizontal groove/slot
# The image shows a thin line running horizontally.
# It looks recessed. We'll cut it into the front face.
result = (
    base.faces(">Z")
    .workplane()
    .slot2D(center_slot_length, center_slot_width)
    .cutBlind(-center_slot_depth)
)

# 3. Create the vertical slots on the left and right ends
# These clearly look like through-holes for mounting.

# Calculate X positions for the side slots
x_pos_right = (plate_length / 2) - side_slot_margin
x_pos_left = -((plate_length / 2) - side_slot_margin)

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(x_pos_left, 0), (x_pos_right, 0)])
    .rect(side_slot_width, side_slot_height) # Using rect for sharp corners, or slot2D for rounded
    # Looking closely at the image, the vertical slots appear to have squared ends, 
    # but slot2D is safer for manufacturing. The image is low res but they look like simple rectangles.
    # Let's use rect based on the sharp corners visible in the pixelation, but standard practice suggests slots.
    # I will stick to rect to match the visual sharpness.
    .cutBlind(-plate_thickness) 
)

# To ensure the result is correctly oriented as per the image (standing up),
# we might want to rotate it, but keeping it flat on XY is standard for export.
# The user wants "result".

# Refinement: Looking very closely at the crop, the vertical slots seem to have
# rounded ends (stadium shape). I will switch to slot2D for a more realistic mechanical part.
# The central line also looks like a groove.

result = (
    base.faces(">Z")
    .workplane()
    # Central Groove
    .slot2D(center_slot_length, center_slot_width)
    .cutBlind(-center_slot_depth)
    # Side Slots
    .faces(">Z").workplane()
    .pushPoints([(x_pos_left, 0), (x_pos_right, 0)])
    # The side features look like vertical slots (stadium shape)
    # The width is the smaller dimension, height is the length
    # slot2D takes length (major axis) and width (minor axis).
    # Since we want vertical slots, we need to rotate 90 degrees or just create rects with fillets.
    # A cleaner way with CadQuery slot2D is to orient the workplane or use rect+fillet.
    # Let's use rect and allow the user to interpret, or rotate the slot.
    # Actually, slot2D creates a slot along the X axis of the current workplane.
    # To make them vertical, we can create them as rects and then fillet, 
    # or use a rotated workplane, or just swap dimensions if using a generic shape.
    # Let's use rect for simplicity and robustness matching the visual 'sharpness'.
    .rect(side_slot_width, side_slot_height)
    .cutBlind(-plate_thickness)
)
