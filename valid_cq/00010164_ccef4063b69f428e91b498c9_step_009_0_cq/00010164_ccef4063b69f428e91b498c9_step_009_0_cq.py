import cadquery as cq

# --- Parameter Definitions ---
# Overall block dimensions
block_length = 60.0   # Dimension along X
block_width = 30.0    # Dimension along Y (thickness)
block_height_front = 40.0 # Height at the front (lower side)
block_height_back = 50.0  # Height at the back (higher side)

# Slot dimensions
slot_width = 4.0
slot_depth = 5.0
slot_length = block_length - 10.0 # Length of the slots
slot_spacing = 8.0 # Center-to-center distance between slots

# Hole dimensions
hole_diameter = 6.0
hole_depth = 10.0 # Depth of the holes (blind holes)
hole_spacing_x = 30.0 # Distance between hole centers horizontally
hole_z_pos = 20.0 # Height of the holes from the bottom

# --- Geometry Construction ---

# 1. Create the base profile (Trapezoidal cross-section on YZ plane extruded along X)
# The block has a sloping top face.
# Let's define the points for the side profile (YZ plane).
# Origin (0,0) is bottom-front-left corner.

# Points for the YZ profile (Looking from the side)
pts = [
    (0, 0),                       # Bottom-front
    (block_width, 0),             # Bottom-back
    (block_width, block_height_back), # Top-back
    (0, block_height_front)       # Top-front
]

# Extrude the trapezoid along X-axis
base_block = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(block_length)
)

# 2. Cut the slots on the top face
# We need to orient ourselves to the top angled face or just project from top (XY)
# Since the top is angled, using a simple XY cut works if projected, but let's try 
# to select the top face directly to be precise, or just cut down from a plane above.
# Given the image, the slots run parallel to the length.

# Let's find the top face and sketch on it.
top_face = base_block.faces(">Z")

# Create the slots.
# We will create two rectangular cuts.
# The slots are centered on the top face relative to the Y-axis (width).

result = (
    base_block
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    # Move to the start position of the slots
    # Slot 1
    .center(0, -slot_spacing/2)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
    # Slot 2 (resetting center first)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(0, slot_spacing/2)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# 3. Create the holes on the front face
# The front face is the one with height = block_height_front (on the XZ plane at Y=0)

result = (
    result
    .faces("<Y") # Select the front face
    .workplane()
    # Position the holes. 
    # The workplane center is at (block_length/2, block_height_front/2).
    # We want holes at specific absolute heights or relative positions.
    # Let's assume they are symmetric horizontally.
    .pushPoints([
        (-hole_spacing_x/2, hole_z_pos - block_height_front/2), 
        (hole_spacing_x/2, hole_z_pos - block_height_front/2)
    ])
    .hole(hole_diameter, depth=hole_depth)
)

# Final result variable
result = result