import cadquery as cq

# Parameters for the L-bracket with slot
length = 120.0        # Total length of the part
width = 40.0          # Width of the part
thickness = 6.0       # Thickness of the base plate and flange
flange_height = 25.0  # Total height of the vertical flange
slot_width = 12.0     # Width of the slot
margin_tip = 15.0     # Distance from the flat end to the slot
margin_flange = 10.0  # Distance from the flange to the slot

# 1. Create the Base Plate
# Centered on XY plane, extending from Z=0 to Z=thickness
base = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))

# 2. Create the Vertical Flange
# Positioned at the +X end of the base plate
# Aligning the outer face of the flange with the edge of the base
flange_x_pos = (length / 2.0) - (thickness / 2.0)
flange = (
    cq.Workplane("XY")
    .center(flange_x_pos, 0)
    .box(thickness, width, flange_height, centered=(True, True, False))
)

# Combine the base and the flange into a single solid
body = base.union(flange)

# 3. Cut the Slot
# Calculate geometry for the slot
# Coordinates of key features along X axis
x_plate_start = -length / 2.0
x_flange_inner = (length / 2.0) - thickness

# Determine start and end X coordinates of the slot (tip-to-tip)
slot_x_start = x_plate_start + margin_tip
slot_x_end = x_flange_inner - margin_flange

# Derived slot parameters
slot_len_total = slot_x_end - slot_x_start
slot_len_c2c = slot_len_total - slot_width  # Center-to-center length for slot2D
slot_center_x = (slot_x_start + slot_x_end) / 2.0

# Apply the cut
# We select the bottom face (<Z) to establish the workplane at Z=0
# and cut through the entire thickness
result = (
    body
    .faces("<Z")
    .workplane()
    .center(slot_center_x, 0)
    .slot2D(slot_len_c2c, slot_width)
    .cutThruAll()
)