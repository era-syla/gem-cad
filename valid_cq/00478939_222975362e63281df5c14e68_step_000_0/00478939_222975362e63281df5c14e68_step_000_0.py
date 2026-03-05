import cadquery as cq

# --- Parameters ---
thickness = 4.0

# Dimensions approximating the geometry in the image
# Origin (0,0) is defined at the inner corner where the left arm meets the vertical leg
leg_width = 45.0
leg_drop = 45.0        # Distance from origin to bottom edge
arm_length = 60.0
arm_tip_height = 16.0  # Height of the vertical tip of the arm
chamfer_width = 10.0   # Horizontal span of the chamfer at the arm tip
chamfer_height = 10.0  # Vertical rise of the chamfer
top_slope_height = 50.0 # Height of the top-right corner relative to origin

# Derived coordinates
p_origin = (0, 0)
p_arm_bottom = (-arm_length, 0)
p_arm_tip_bottom = (-arm_length, arm_tip_height)
p_chamfer_end = (-arm_length + chamfer_width, arm_tip_height + chamfer_height)
p_top_right = (leg_width, top_slope_height)
p_bottom_right = (leg_width, -leg_drop)
p_bottom_left_leg = (0, -leg_drop)

# --- Base Geometry ---
# Define the outer profile
pts = [
    p_origin,
    p_arm_bottom,
    p_arm_tip_bottom,
    p_chamfer_end,
    p_top_right,
    p_bottom_right,
    p_bottom_left_leg
]

# Create the main solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# --- Fillets ---
# Apply fillets to smooth specific corners
# Top Right Corner
result = result.edges(cq.selectors.NearestToPointSelector(p_top_right)).fillet(6.0)
# Bottom Right Corner (Large Radius)
result = result.edges(cq.selectors.NearestToPointSelector(p_bottom_right)).fillet(18.0)
# Bottom Left Corner of the vertical leg
result = result.edges(cq.selectors.NearestToPointSelector(p_bottom_left_leg)).fillet(8.0)
# Arm Tip Corners (Small Radius)
result = result.edges(cq.selectors.NearestToPointSelector(p_arm_bottom)).fillet(2.0)
result = result.edges(cq.selectors.NearestToPointSelector(p_arm_tip_bottom)).fillet(2.0)
# Chamfer to Slope transition
result = result.edges(cq.selectors.NearestToPointSelector(p_chamfer_end)).fillet(3.0)

# --- Features (Holes and Slots) ---

# 1. Slot on the Right Edge
# Horizontal slot near the top
slot_right_y = top_slope_height - 15
result = (
    result.faces(">Z").workplane()
    .moveTo(leg_width, slot_right_y)
    .rect(12, 4.2)  # Centered on edge: 6mm cut depth
    .cutThruAll()
)

# 2. Slot on the Left Arm Bottom
# Vertical slot near the tip
slot_arm_x = -arm_length + 12
result = (
    result.faces(">Z").workplane()
    .moveTo(slot_arm_x, 0)
    .rect(4.2, 14)  # Centered on edge: 7mm cut depth
    .cutThruAll()
)

# 3. Small Mounting Holes
# Hole on the arm
result = (
    result.faces(">Z").workplane()
    .moveTo(-arm_length + 10, arm_tip_height - 4)
    .hole(3.2)
)

# Hole in the middle body
result = (
    result.faces(">Z").workplane()
    .moveTo(leg_width / 2.0 - 5, 8)
    .hole(3.2)
)

# 4. Large Keyhole Slots (Bottom Right)
large_hole_dia = 10.0
slot_width = 4.2

# Lower Left Keyhole
kh1_x, kh1_y = 12, -28
result = (
    result.faces(">Z").workplane()
    .moveTo(kh1_x, kh1_y)
    .hole(large_hole_dia)
    .moveTo(kh1_x, kh1_y - 10)
    .rect(slot_width, 25) # Cut slot downwards through bottom edge
    .cutThruAll()
)

# Upper Right Keyhole
kh2_x, kh2_y = 32, -18
result = (
    result.faces(">Z").workplane()
    .moveTo(kh2_x, kh2_y)
    .hole(large_hole_dia)
    .moveTo(kh2_x, kh2_y - 12)
    .rect(slot_width, 25) # Cut slot downwards through curved edge
    .cutThruAll()
)