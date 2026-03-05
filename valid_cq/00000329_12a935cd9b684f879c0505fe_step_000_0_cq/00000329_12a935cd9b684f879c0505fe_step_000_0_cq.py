import cadquery as cq

# Parametric dimensions
length = 150.0       # Total length of the plate
width = 30.0         # Width of the plate
thickness = 3.0      # Thickness of the plate

# Slot dimensions
slot_length = 70.0   # Length of the central slot (center-to-center)
slot_width = 15.0    # Width of the slot

# Mounting hole dimensions
hole_diameter = 5.0  # Diameter of the small holes at the ends
hole_offset = 10.0   # Distance from the edge to the center of the hole

# Create the base plate
# We start with a centered box
base = cq.Workplane("XY").box(length, width, thickness)

# Create the central slot
# We sketch a slot and cut it through the base
# The slot method in CadQuery takes a boolean for centering
# But a more explicit way is to sketch points and use the slot2D method
result = (
    base
    .faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)

# Create the mounting holes
# Calculate positions relative to the center
# x_pos is half the length minus the offset distance
hole_x_pos = (length / 2) - hole_offset

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_x_pos, 0), (hole_x_pos, 0)])
    .hole(hole_diameter)
)

# The 'result' variable contains the final geometry as requested