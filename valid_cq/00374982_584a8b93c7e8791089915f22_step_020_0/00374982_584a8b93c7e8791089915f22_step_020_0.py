import cadquery as cq

# --- Parameters ---
# Main body dimensions
length_c2c = 100.0       # Distance between centers of the outer radii
arm_width = 30.0         # Width of the arm (outer diameter of ends)
plate_thickness = 5.0    # Thickness of the base plate

# Slot dimensions
slot_width = 12.0        # Width of the internal slot
boss_clearance = 8.0     # Solid material between slot end and boss
boss_base_dia = 18.0     # Diameter of the boss flange

# Calculate slot geometry
# We want the slot to be concentric with the left end, but stop short of the boss on the right.
slot_start_x = -length_c2c / 2.0
slot_end_x = (length_c2c / 2.0) - (boss_base_dia / 2.0) - boss_clearance
slot_length = slot_end_x - slot_start_x
slot_center_x = (slot_start_x + slot_end_x) / 2.0

# Boss dimensions
boss_x_pos = length_c2c / 2.0
boss_height_1 = 3.0      # Height of the flange
boss_top_dia = 12.0      # Diameter of the top cylinder
boss_height_2 = 6.0      # Height of the top cylinder
hole_size = 6.0          # Side length of the square hole

# --- Modeling ---

# 1. Create the base plate (slotted arm shape)
result = (
    cq.Workplane("XY")
    .slot2D(length_c2c, arm_width)
    .extrude(plate_thickness)
)

# 2. Cut the internal slot
# Use ProjectedOrigin to define the center relative to the global origin
result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .center(slot_center_x, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-plate_thickness)
)

# 3. Add the Boss (Lower Flange)
result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .center(boss_x_pos, 0)
    .circle(boss_base_dia / 2.0)
    .extrude(boss_height_1)
)

# 4. Add the Boss (Upper Cylinder)
# Use CenterOfMass to center on the previous circular face
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(boss_top_dia / 2.0)
    .extrude(boss_height_2)
)

# 5. Cut the Square Hole
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(hole_size, hole_size)
    .cutThruAll()
)