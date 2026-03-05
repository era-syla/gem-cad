import cadquery as cq

# --- Parametric Dimensions ---
stool_height = 700.0
seat_diameter = 320.0
seat_thickness = 35.0
seat_fillet = 10.0

leg_width = 32.0
leg_spread_bottom = 360.0  # Center-to-center distance at floor
leg_spread_top = 180.0     # Center-to-center distance under seat

rung_diameter = 22.0
rung_height_lower = 220.0
rung_height_upper = 380.0

# --- Derived Calculations ---
leg_length = stool_height - seat_thickness
offset_bot = leg_spread_bottom / 2.0
offset_top = leg_spread_top / 2.0

# --- Helper Function ---
def get_offset_at_height(h):
    """Calculates the XY offset of the leg center from origin at a specific height."""
    t = h / leg_length
    return offset_bot + (offset_top - offset_bot) * t

# --- Geometry Construction ---

# 1. Create the Seat
seat = (
    cq.Workplane("XY")
    .workplane(offset=leg_length)
    .circle(seat_diameter / 2.0)
    .extrude(seat_thickness)
    .edges()
    .fillet(seat_fillet)
)

# 2. Create the Legs
# We generate 4 legs by lofting squares from the floor to the seat underside
legs = None
quadrants = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

for qx, qy in quadrants:
    # Start and End coordinates for this leg
    x1, y1 = qx * offset_bot, qy * offset_bot
    x2, y2 = qx * offset_top, qy * offset_top
    
    leg = (
        cq.Workplane("XY")
        .center(x1, y1)
        .rect(leg_width, leg_width)
        .workplane(offset=leg_length)
        .center(x2 - x1, y2 - y1)  # Shift relative to previous plane center
        .rect(leg_width, leg_width)
        .loft()
    )
    
    if legs is None:
        legs = leg
    else:
        legs = legs.union(leg)

# 3. Create the Rungs
# Lower Rungs (Side connections along Y-axis)
off_low = get_offset_at_height(rung_height_lower)

# Right Side Rung (X+)
rung_right = (
    cq.Workplane("XZ")
    .center(off_low, rung_height_lower)
    .circle(rung_diameter / 2.0)
    .extrude(off_low * 2.0, both=True)
)

# Left Side Rung (X-)
rung_left = (
    cq.Workplane("XZ")
    .center(-off_low, rung_height_lower)
    .circle(rung_diameter / 2.0)
    .extrude(off_low * 2.0, both=True)
)

# Upper Rungs (Front/Back connections along X-axis)
off_high = get_offset_at_height(rung_height_upper)

# Back Rung (Y+)
rung_back = (
    cq.Workplane("YZ")
    .center(off_high, rung_height_upper)
    .circle(rung_diameter / 2.0)
    .extrude(off_high * 2.0, both=True)
)

# Front Rung (Y-)
rung_front = (
    cq.Workplane("YZ")
    .center(-off_high, rung_height_upper)
    .circle(rung_diameter / 2.0)
    .extrude(off_high * 2.0, both=True)
)

# --- Final Assembly ---
result = (
    seat
    .union(legs)
    .union(rung_right)
    .union(rung_left)
    .union(rung_back)
    .union(rung_front)
)