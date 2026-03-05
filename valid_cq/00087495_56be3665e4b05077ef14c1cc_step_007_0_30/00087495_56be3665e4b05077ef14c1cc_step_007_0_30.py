import cadquery as cq

# --- Parameters ---
# Base dimensions
base_width = 50.0
base_length = 70.0
base_height = 4.0
base_fillet_radius = 6.0

# Slot dimensions
slot_width = 8.0
slot_length = 25.0
slot_y_pos = -18.0

# Head (Cylinder) dimensions
head_diameter = 38.0
head_length = 32.0
head_z_center = 55.0
head_y_center = -5.0

# Rim dimensions
rim_diameter = 42.0
rim_length = 6.0

# Arm dimensions
arm_base_width = 36.0
arm_base_length = 30.0
arm_base_y_pos = 15.0

# --- Modeling ---

# 1. Base Plate
base = (
    cq.Workplane("XY")
    .box(base_width, base_length, base_height)
    .edges("|Z")
    .fillet(base_fillet_radius)
)

# Add a small chamfer/fillet to the top edge of the base
base = base.edges(">Z").fillet(1.0)

# Cut the adjustment slot
slot = (
    cq.Workplane("XY")
    .center(0, slot_y_pos)
    .slot2D(slot_length, slot_width)
    .extrude(base_height * 2, combine=False)
)
base = base.cut(slot)

# 2. Head Assembly (Cylindrical Housing)
# Main Cylinder Body
head_main = (
    cq.Workplane("XZ")
    .circle(head_diameter / 2.0)
    .extrude(head_length)
    # Center the extrusion on the Y axis relative to the desired center point
    .translate((0, head_y_center - head_length / 2.0, head_z_center))
)

# Front Rim (larger diameter)
# Positioned at the front (-Y end) of the main cylinder
rim = (
    cq.Workplane("XZ")
    .circle(rim_diameter / 2.0)
    .extrude(rim_length)
    .translate((0, head_y_center - head_length / 2.0 - rim_length, head_z_center))
)

# Combine Head parts
head = head_main.union(rim)

# Detail: Recess in the front face
recess = (
    cq.Workplane("XZ")
    .circle(head_diameter / 2.0 - 2.0)
    .extrude(2.0)
    .translate((0, head_y_center - head_length / 2.0 - rim_length, head_z_center))
)
head = head.cut(recess)

# Detail: Pinhole in the center of front face
pinhole = (
    cq.Workplane("XZ")
    .circle(1.5)
    .extrude(5.0)
    .translate((0, head_y_center - head_length / 2.0 - rim_length - 1.0, head_z_center))
)
head = head.cut(pinhole)

# Detail: Set screw hole on top of the rim
set_screw = (
    cq.Workplane("XY")
    .circle(1.5)
    .extrude(10.0) # Length of cut
    .translate((0, head_y_center - head_length / 2.0 - rim_length / 2.0, head_z_center + rim_diameter / 2.0))
)
# Shift down to intersect
set_screw = set_screw.translate((0, 0, -5.0))
head = head.cut(set_screw)

# 3. Arm (Connecting Base to Head)
# We use a loft to transition from the rectangular base footprint to the cylindrical head
# Top profile of the arm needs to intersect the cylinder bottom
loft_z_top = head_z_center - head_diameter / 3.0 # Go somewhat inside the cylinder

arm = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(0, arm_base_y_pos)
    .rect(arm_base_width, arm_base_length) # Bottom Profile
    .workplane(offset=loft_z_top - base_height)
    .center(0, head_y_center - arm_base_y_pos) # Shift to align with head
    .rect(head_diameter, head_length * 0.8)   # Top Profile (approximate cylinder footprint)
    .loft(combine=False)
)

# 4. Final Assembly
# Union all parts
result = base.union(arm).union(head)

# 5. Filleting
# Fillet the intersection between Arm and Base
# We select edges within a bounding box at the base height
result = result.edges(cq.selectors.BoxSelector(
    (-base_width, -base_length, base_height - 1.0),
    (base_width, base_length, base_height + 1.0)
)).fillet(5.0)

# Fillet the intersection between Arm and Head (Neck)
# We select edges in the neck region
neck_selector = cq.selectors.BoxSelector(
    (-head_diameter, -50, loft_z_top - 5.0),
    (head_diameter, 50, head_z_center)
)
# Apply a smaller fillet to smooth the neck transition
try:
    result = result.edges(neck_selector).fillet(2.0)
except Exception:
    # Fallback if geometry is too complex for specific edge selection
    pass