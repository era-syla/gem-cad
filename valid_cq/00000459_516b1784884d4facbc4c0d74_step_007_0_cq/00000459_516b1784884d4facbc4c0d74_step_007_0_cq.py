import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the rectangular plate
length = 100.0  # Total length of the plate
width = 25.0    # Total width of the plate
thickness = 8.0 # Thickness of the plate

# Fillet radius for the corners of the plate
corner_radius = 2.0

# Hole dimensions
hole_diameter = 5.0
countersink_diameter = 10.0 # Standard screw head size approximation
countersink_angle = 90.0

# Slot dimensions
slot_length = 15.0 # Center-to-center or overall length
slot_width = 5.0

# Hole positions
# Based on visual estimation:
# - Two holes near the ends
# - One hole slightly off-center
# - One slot near the other end
end_hole_distance = 10.0 # Distance from short edge to hole center
off_center_hole_offset = 15.0 # Offset from center for the inner hole
slot_center_offset = 20.0 # Offset from center for the slot

# --- Modeling ---

# 1. Create the base rectangular plate
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add the two end holes
# Hole 1: Far left
# Hole 2: Far right
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-length/2 + end_hole_distance, 0),
        (length/2 - end_hole_distance, 0)
    ])
    .hole(hole_diameter)
)

# 3. Add the third single hole (slightly off-center to the left)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-off_center_hole_offset, 0)])
    .hole(hole_diameter)
)

# 4. Add the slot (to the right of the center)
result = (
    result.faces(">Z")
    .workplane()
    .center(slot_center_offset, 0)
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)

# Optional: Add small chamfers or fillets to holes if desired, 
# but the image shows simple drilled holes and a milled slot.