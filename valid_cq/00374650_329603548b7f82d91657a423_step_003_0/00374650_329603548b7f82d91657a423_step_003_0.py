import cadquery as cq

# --- Parameters ---
num_bays = 4
bay_length = 1200.0           # Distance between leg supports
track_width = 500.0           # Center-to-center width between rails
total_length = num_bays * bay_length

# Leg Dimensions
leg_height = 800.0
leg_size = 50.0               # Square tube dimension
base_plate_size = 100.0
base_plate_thick = 10.0
cap_plate_size = 80.0
cap_plate_thick = 10.0

# Rail Dimensions
rail_overhang = 250.0         # Rail extension past the first/last leg
rail_width = 80.0
rail_height = 40.0
rail_thickness = 6.0

# Bracing Dimensions
brace_size = 30.0             # Square tube for cross-bracing
lower_brace_h = 250.0         # Height of lower bracing from floor
upper_brace_h = 650.0         # Height of upper bracing from floor

# --- Helper Functions ---

def create_leg_assembly():
    """Creates a single leg with base plate and top cap."""
    # Base Plate
    base = cq.Workplane("XY").box(base_plate_size, base_plate_size, base_plate_thick) \
        .translate((0, 0, base_plate_thick / 2))
    
    # Vertical Leg Tube
    leg_z_center = base_plate_thick + (leg_height / 2)
    leg = cq.Workplane("XY").box(leg_size, leg_size, leg_height) \
        .translate((0, 0, leg_z_center))
    
    # Top Cap Plate
    cap_z_center = base_plate_thick + leg_height + (cap_plate_thick / 2)
    cap = cq.Workplane("XY").box(cap_plate_size, cap_plate_size, cap_plate_thick) \
        .translate((0, 0, cap_z_center))
        
    return base.union(leg).union(cap)

def create_rail_profile(length):
    """Creates a C-channel rail facing upwards."""
    w, h, t = rail_width, rail_height, rail_thickness
    
    # Points for U-shape (on YZ plane, Local Y is World Z)
    pts = [
        (-w/2, h), (-w/2, 0), (w/2, 0), (w/2, h),
        (w/2 - t, h), (w/2 - t, t), (-w/2 + t, t), (-w/2 + t, h)
    ]
    
    # Extrude along X axis
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

# --- Assembly Generation ---

# 1. Create reusable components
leg_unit = create_leg_assembly()
transverse_brace_len = track_width - leg_size
transverse_brace_geo = cq.Workplane("XY").box(transverse_brace_len, brace_size, brace_size)

# 2. Build Support Structure
supports = cq.Workplane("XY")

for i in range(num_bays + 1):
    x_pos = i * bay_length
    
    # Place Left and Right Legs
    left_leg = leg_unit.translate((x_pos, -track_width / 2, 0))
    right_leg = leg_unit.translate((x_pos, track_width / 2, 0))
    
    # Place Transverse Braces (connecting the pair)
    # Lower brace
    brace_low = transverse_brace_geo.translate((x_pos, 0, lower_brace_h))
    # Upper brace
    brace_high = transverse_brace_geo.translate((x_pos, 0, upper_brace_h))
    
    supports = supports.union(left_leg).union(right_leg).union(brace_low).union(brace_high)

# 3. Build Longitudinal Braces (running along the length)
# We model this as a continuous beam intersecting the legs
long_brace_geo = cq.Workplane("XY").box(total_length, brace_size, brace_size)
long_brace_z = lower_brace_h
long_brace_center_x = total_length / 2

longitudinal_braces = (
    long_brace_geo.translate((long_brace_center_x, -track_width / 2, long_brace_z))
    .union(long_brace_geo.translate((long_brace_center_x, track_width / 2, long_brace_z)))
)

# 4. Build Top Rails
total_rail_len = total_length + (2 * rail_overhang)
rail_z_pos = base_plate_thick + leg_height + cap_plate_thick
rail_geo = create_rail_profile(total_rail_len)

# Translate rails to position (accounting for overhang start position)
rails = (
    rail_geo.translate((-rail_overhang, -track_width / 2, rail_z_pos))
    .union(rail_geo.translate((-rail_overhang, track_width / 2, rail_z_pos)))
)

# 5. Final Result
result = supports.union(longitudinal_braces).union(rails)