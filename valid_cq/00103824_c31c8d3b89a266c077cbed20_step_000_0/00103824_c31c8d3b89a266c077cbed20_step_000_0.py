import cadquery as cq
import math

# --- Parameters ---
# Bracket dimensions
b_width = 24.0
b_thickness = 10.0
arm1_len = 50.0  # Length of the slotted arm (from bend)
arm2_len = 50.0  # Length of the hole arm (from bend)
bend_angle = 35.0  # Bend deflection angle in degrees
slot_w = 6.0
slot_l = 20.0     # Depth of slot from end
hole_d = 10.0
hole_offset = 15.0 # Hole center distance from end tip

# Pin dimensions
pin_d = 9.5
pin_l = 45.0
head_d = 18.0
head_t = 4.0

# --- Geometry Generation ---

# 1. Bracket Construction
# Define the centerline path coordinates
rad = math.radians(bend_angle)
p_start = (-arm1_len, 0)
p_bend = (0, 0)
p_end = (arm2_len * math.cos(rad), -arm2_len * math.sin(rad))

# Create the base shape using a 2D offset of the centerline wire
# kind='intersection' produces sharp corners at the bend
bracket_wire = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    .lineTo(*p_bend)
    .lineTo(*p_end)
    .wire()
    .offset2D(b_width / 2, kind="intersection")
)

# Extrude the base profile
bracket = bracket_wire.extrude(b_thickness)

# Cut the Slot (Left Arm)
# Position a cutter rectangle centered on the tip of the arm
# Length is doubled and centered to ensure it cuts through the open end
slot_cutter = (
    cq.Workplane("XY")
    .moveTo(p_start[0], p_start[1]) 
    .rect(slot_l * 2, slot_w)
    .extrude(b_thickness * 2, both=True)
)
bracket = bracket.cut(slot_cutter)

# Cut the Hole (Right Arm)
# Calculate position along the vector of the second arm
vec_x = math.cos(rad)
vec_y = -math.sin(rad)
hole_x = p_end[0] - hole_offset * vec_x
hole_y = p_end[1] - hole_offset * vec_y

hole_cutter = (
    cq.Workplane("XY")
    .moveTo(hole_x, hole_y)
    .circle(hole_d / 2)
    .extrude(b_thickness * 2, both=True)
)
bracket = bracket.cut(hole_cutter)

# 2. Pin Construction
# Create pin shaft aligned with X axis
pin = (
    cq.Workplane("YZ")
    .circle(pin_d / 2)
    .extrude(pin_l)
)
# Add head at the start face (extrude in negative X direction)
pin_head = (
    cq.Workplane("YZ")
    .circle(head_d / 2)
    .extrude(-head_t)
)
pin = pin.union(pin_head)

# Position the Pin (Floating above the bracket as in the image)
# Flip orientation and apply rotations/translation
pin = pin.rotate((0,0,0), (0,1,0), 180)  # Flip so shaft points negative X
pin = pin.rotate((0,0,0), (0,1,0), -30)  # Tilt up
pin = pin.rotate((0,0,0), (0,0,1), 20)   # Rotate slightly in plan
pin = pin.translate((20, 30, 50))        # Move to position

# --- Final Result ---
result = bracket.union(pin)