import cadquery as cq

# --- Parametric Dimensions ---
# Rail dimensions
rail_length = 350.0
rail_width = 40.0
rail_height = 20.0
wall_thickness = 3.0
slot_width = 15.0  # Width of the bottom opening

# Motor dimensions (NEMA 17 approx)
motor_size = 42.0
motor_length = 38.0
motor_cap_dia = 22.0
motor_cap_len = 10.0

# Mounting Plate dimensions
plate_thickness = 5.0
plate_size = 45.0

# Carriage (Slider) dimensions
carriage_len = 70.0
carriage_width = 30.0
carriage_height = 15.0  # Height of the block below the rail
carriage_pos = 100.0    # Position along the rail

# Lead Screw dimensions
screw_dia = 6.0

# --- Helper Function for Rail Profile ---
def create_rail_profile(w, h, t, slot):
    """
    Generates a list of points for an inverted U-channel rail profile.
    Centered at (0,0) on the YZ plane.
    """
    hw = w / 2.0
    hh = h / 2.0
    
    # Trace the perimeter of the solid wall
    # Starting top-right, going counter-clockwise
    pts = [
        (hw, hh),              # Top Right
        (-hw, hh),             # Top Left
        (-hw, -hh),            # Bottom Left
        (-slot/2.0, -hh),      # Slot Left Edge
        (-slot/2.0, -hh + t),  # Inner Slot Left
        (-hw + t, -hh + t),    # Inner Bottom Left
        (-hw + t, hh - t),     # Inner Top Left
        (hw - t, hh - t),      # Inner Top Right
        (hw - t, -hh + t),     # Inner Bottom Right
        (slot/2.0, -hh + t),   # Inner Slot Right
        (slot/2.0, -hh),       # Slot Right Edge
        (hw, -hh)              # Bottom Right
    ]
    return pts

# --- Geometry Construction ---

# 1. Main Rail Extrusion
rail_pts = create_rail_profile(rail_width, rail_height, wall_thickness, slot_width)
rail = (
    cq.Workplane("YZ")
    .polyline(rail_pts)
    .close()
    .extrude(rail_length)
)

# 2. Motor Mounting Plate (Left End)
# Centered on the rail axis (0,0)
motor_plate = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_thickness)
    .rect(plate_size, plate_size)
    .extrude(plate_thickness)
)

# 3. Motor Body
motor_body = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_thickness)
    .rect(motor_size, motor_size)
    .extrude(-motor_length)
)

# 4. Motor Rear Cap/Encoder
motor_cap = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_thickness - motor_length)
    .circle(motor_cap_dia / 2.0)
    .extrude(-motor_cap_len)
)

# 5. Lead Screw
# Runs through the center of the rail
screw = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_thickness - 2.0)
    .circle(screw_dia / 2.0)
    .extrude(rail_length + plate_thickness + 4.0)
)

# 6. Carriage Assembly
# Inner block that slides inside the rail
inner_w = rail_width - 2*wall_thickness - 0.5
inner_h = rail_height - wall_thickness - 0.5
carriage_inner = (
    cq.Workplane("YZ")
    .rect(inner_w, inner_h)
    .extrude(carriage_len)
    .translate((carriage_pos, 0, 0))
)

# Neck connecting inner and outer parts through the slot
neck_w = slot_width - 0.5
carriage_neck = (
    cq.Workplane("YZ")
    .rect(neck_w, wall_thickness + 2.0)
    .extrude(carriage_len)
    .translate((carriage_pos, 0, -rail_height/2.0))
)

# Outer block hanging below the rail
carriage_outer = (
    cq.Workplane("YZ")
    .rect(carriage_width, carriage_height)
    .extrude(carriage_len)
    .translate((carriage_pos, 0, -rail_height/2.0 - carriage_height/2.0))
)

# Combine carriage parts and cut hole for screw
carriage = carriage_inner.union(carriage_neck).union(carriage_outer)
# Create a cutting tool for the screw hole
screw_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-100)
    .circle(screw_dia/2.0 + 0.5)
    .extrude(rail_length + 200)
)
carriage = carriage.cut(screw_cutter)

# 7. End Plate (Right End)
end_plate = (
    cq.Workplane("YZ")
    .workplane(offset=rail_length)
    .rect(plate_size, plate_size) # Matching motor plate size
    .extrude(plate_thickness)
)

# --- Final Assembly ---
result = (
    rail
    .union(motor_plate)
    .union(motor_body)
    .union(motor_cap)
    .union(screw)
    .union(carriage)
    .union(end_plate)
)