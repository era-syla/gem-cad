import cadquery as cq

# --- Parametric Dimensions ---

# Lever dimensions
lever_arm_length = 50.0    # Length of the rectangular section
lever_height = 25.0        # Height of the lever
lever_thickness = 10.0     # Thickness of the lever body
hole_diameter = 12.0       # Diameter of the main pivot hole
fillet_radius = lever_height / 2.0

# Lever side pin dimensions
side_pin_dia = 8.0
side_pin_length = 18.0
side_pin_offset_x = -35.0  # Distance from hole center along the arm
side_pin_offset_y = -6.0   # Vertical offset from center line

# Cap dimensions
cap_diameter = 24.0
cap_thickness = 12.0
cap_offset_x = 40.0        # Distance from lever origin
cap_pin_dia = 4.0
cap_pin_len = 8.0
cap_pin_spacing = 10.0

# Loose pins dimensions
dowel_dia = 5.0
dowel_len = 25.0
dowel_spacing = 15.0
dowel_pos_y = -40.0        # Y position relative to main assembly
dowel_pos_z = -40.0        # Z position (base)

# --- Modeling ---

# 1. Main Lever Arm
# Create the rectangular body
lever_rect = (
    cq.Workplane("XZ")
    .rect(lever_arm_length, lever_height)
    .translate((-lever_arm_length / 2, 0, 0)) # Shift to align right edge to origin
    .extrude(lever_thickness)
)

# Create the rounded end
lever_round = (
    cq.Workplane("XZ")
    .circle(fillet_radius)
    .extrude(lever_thickness)
)

# Union body parts and cut the main hole
lever = lever_rect.union(lever_round)
lever = (
    lever.faces(">Y").workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Add the side pin to the lever
# Selecting the front face (>Y)
lever = (
    lever.faces(">Y").workplane()
    .moveTo(side_pin_offset_x, side_pin_offset_y)
    .circle(side_pin_dia / 2)
    .extrude(side_pin_length)
)

# 2. Cap Component
# Oriented along X axis, positioned to the right
cap = (
    cq.Workplane("YZ")
    .workplane(offset=cap_offset_x)
    .circle(cap_diameter / 2)
    .extrude(cap_thickness)
)

# Add two small pins to the cap (facing the lever)
cap = (
    cap.faces("<X").workplane()
    .pushPoints([(0, cap_pin_spacing / 2), (0, -cap_pin_spacing / 2)])
    .circle(cap_pin_dia / 2)
    .extrude(cap_pin_len)
)

# 3. Three Loose Dowel Pins
# Positioned below the main assembly
pin_objects = []
for i in range(3):
    x_pos = 15.0 + (i * dowel_spacing)
    pin = (
        cq.Workplane("XY")
        .translate((x_pos, dowel_pos_y, dowel_pos_z))
        .circle(dowel_dia / 2)
        .extrude(dowel_len)
    )
    pin_objects.append(pin)

# --- Combine Final Result ---
result = lever.union(cap)
for p in pin_objects:
    result = result.union(p)
