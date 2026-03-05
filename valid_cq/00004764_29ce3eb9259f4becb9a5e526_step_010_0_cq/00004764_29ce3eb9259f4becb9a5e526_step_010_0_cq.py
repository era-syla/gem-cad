import cadquery as cq

# Parametric dimensions
plate_length = 100.0
plate_height = 50.0
plate_thickness = 5.0

# Slot parameters (the large horizontal slot on the left)
large_slot_width = 25.0
large_slot_height = 12.0
large_slot_x_offset = -20.0  # Center position relative to plate center
large_slot_y_offset = -10.0

# Radial slots pattern parameters (the four slots on the right)
pattern_center_x = 20.0
pattern_center_y = 5.0
radial_distance = 12.0     # Distance from pattern center to slot centers
slot_length = 10.0         # Length of the small radial slots
slot_width = 6.0           # Width of the small radial slots

# Create the main plate
plate = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# Create the large horizontal slot
# We define a slot by two points and a diameter (height in this case)
large_slot = (
    cq.Workplane("XY")
    .center(large_slot_x_offset, large_slot_y_offset)
    .slot2D(large_slot_width, large_slot_height)
    .extrude(plate_thickness)
)

# Create the four radial slots
# We'll create a single slot shape and then rotate/place it
small_slots = cq.Workplane("XY")

# Define the positions and rotations for the 4 slots
# Angles: 0, 90, 180, 270 relative to the pattern center
# We need to position them radially.
for angle in [0, 90, 180, 270]:
    # Create a slot at the origin
    # Then translate it out by radial_distance
    # Then rotate it around the pattern center
    
    # Using a local workplane approach relative to the pattern center
    slot = (
        cq.Workplane("XY")
        .center(pattern_center_x, pattern_center_y)
        .transformed(rotate=cq.Vector(0, 0, angle))
        .center(radial_distance, 0)
        .slot2D(slot_length, slot_width)
        .extrude(plate_thickness)
    )
    small_slots = small_slots.union(slot)

# Combine operations: Cut the large slot and the pattern from the plate
result = plate.cut(large_slot).cut(small_slots)