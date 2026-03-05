import cadquery as cq

# Parametric Dimensions
width = 40.0         # Width of the main block
height = 40.0        # Height of the main block
thickness = 20.0     # Thickness of the main block
fillet_radius = 5.0  # External corner radius

# Bore dimensions
main_bore_dia = 32.0         # Diameter of the large front bore
main_bore_depth = 12.0       # Depth of the large front bore
second_bore_dia = 18.0       # Diameter of the middle step bore
second_bore_depth = 16.0     # Total depth from front face to end of this bore
thru_hole_dia = 8.0          # Diameter of the smallest through hole

# Slot dimensions
slot_width = 6.0
slot_depth = 3.0   # How deep the slot is cut from the bore surface

# Create the main block with rounded corners
# We construct a box centered in X and Y, but sitting on Z=0 initially for easier depth handling
base = cq.Workplane("XY").box(width, height, thickness).edges("|Z").fillet(fillet_radius)

# Create the internal features (counterbores and through hole)
# We work from the front face
result = (
    base.faces(">Z").workplane()
    # 1. Main large bore
    .hole(main_bore_dia, depth=main_bore_depth)
    # 2. Second stepped bore
    .faces(">Z").workplane()
    .hole(second_bore_dia, depth=second_bore_depth)
    # 3. Through hole
    .faces(">Z").workplane()
    .hole(thru_hole_dia)
)

# Create the keyway/slot at the bottom
# We need to cut a rectangular slot. The image shows a slot at the bottom (negative Y direction relative to center)
# cutting into the bore.
# We'll create a cutting tool for the slot.
slot_cutter = (
    cq.Workplane("XZ")
    .center(0, thickness - main_bore_depth/2) # Position roughly in Z
    .rect(slot_width, main_bore_depth)        # Width of slot and length along Z
    .extrude(height/2)                        # Extrude upwards enough to intersect the bottom of the bore
)

# However, looking closely at the image, the slot is cut into the bottom of the large bore.
# A cleaner way is to sketch on the front face and extrude-cut backwards.

result = result.faces(">Z").workplane().center(0, -main_bore_dia/2).rect(slot_width, slot_depth * 2).cutBlind(-main_bore_depth)

# Note: The rect center is positioned at the bottom edge of the hole. 
# We make the rect height (slot_depth * 2) to ensure it cuts fully into the material upwards 
# without needing precise boundary alignment.

# Export or Render preparation
# (This line is not strictly required by the prompt "Return ONLY the Python code", 
# but 'result' variable is required)