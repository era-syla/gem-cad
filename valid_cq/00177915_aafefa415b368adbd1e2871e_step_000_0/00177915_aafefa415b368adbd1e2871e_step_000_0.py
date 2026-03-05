import cadquery as cq

# --- Parameters ---
height = 130
depth = 300
wall_thickness = 2.0
slot_width = 6.0
slot_gap = 4.0

# --- Helper Functions ---
def make_vented_panel(length, width, thickness, axis='X'):
    """
    Creates a rectangular panel with a grid of ventilation slots.
    axis='X': Panel runs along X-axis (face normal to Y).
    axis='Y': Panel runs along Y-axis (face normal to X).
    """
    if axis == 'X':
        # Create base box aligned with X
        base = cq.Workplane("XY").box(length, thickness, width)
        # Select face for cutting (+Y)
        face = base.faces(">Y").workplane()
        
        # Grid parameters
        slot_h = (width - 25.0) / 2.0
        n_slots = int((length - 20) / (slot_width + slot_gap))
        
        # Cut slots
        panel = (
            face
            .rarray(slot_width + slot_gap, slot_h + 10, n_slots, 2)
            .rect(slot_width, slot_h)
            .cutThruAll()
        )
    else:
        # Create base box aligned with Y
        base = cq.Workplane("XY").box(thickness, length, width)
        # Select face for cutting (+X)
        face = base.faces(">X").workplane()
        
        # Grid parameters
        slot_h = (width - 25.0) / 2.0
        n_slots = int((length - 20) / (slot_width + slot_gap))
        
        # Cut slots
        panel = (
            face
            .rarray(slot_width + slot_gap, slot_h + 10, n_slots, 2)
            .rect(slot_width, slot_h)
            .cutThruAll()
        )
    return panel

# --- Component Construction ---

# 1. Front Left Transverse Panel
# The grill structure at the front left
front_left_len = 180
p_front_left = make_vented_panel(front_left_len, height, 4, axis='X')
p_front_left = p_front_left.translate((-front_left_len/2 - 2, -depth/2, 0))

# 2. Front Right Stub
# Small section of the front panel to the right of the center
p_front_stub = make_vented_panel(40, height, 4, axis='X')
p_front_stub = p_front_stub.translate((22, -depth/2, 0))

# 3. Center Longitudinal Divider
# The spine running front-to-back
p_center = make_vented_panel(depth + 20, height, 3, axis='Y')
p_center = p_center.translate((0, 0, 0))

# 4. Horizontal Tray (Black PCB/Plate)
# Located in the bottom left quadrant
tray_w = 170
tray_d = 280
p_tray = (
    cq.Workplane("XY")
    .box(tray_w, tray_d, 2)
    .translate((-tray_w/2 - 2, 0, -height/2 + 25))
)
# Add grid cutouts to the tray for detail
p_tray = (
    p_tray.faces(">Z").workplane()
    .rarray(40, 50, 4, 4)
    .rect(25, 35)
    .cutThruAll()
)

# 5. Right Side Panel
# Solid sheet metal panel offset to the right
p_right_panel = (
    cq.Workplane("XY")
    .box(2, depth + 40, height + 10)
    .translate((160, 20, 5))
)

# 6. Floating Rear Bracket
# L-profile detached part shown on the right
bracket_height = 110
p_bracket = (
    cq.Workplane("XY")
    .polyline([(0,0), (30,0), (30,2), (2,2), (2,30), (0,30), (0,0)])
    .close()
    .extrude(bracket_height)
    .translate((200, 150, -bracket_height/2 + 10))
)

# --- Assembly ---

result = (
    p_front_left
    .union(p_center)
    .union(p_front_stub)
    .union(p_tray)
    .union(p_right_panel)
    .union(p_bracket)
)