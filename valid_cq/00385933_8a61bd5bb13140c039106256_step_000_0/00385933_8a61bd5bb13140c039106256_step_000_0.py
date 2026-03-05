import cadquery as cq

# --- Parameters ---
# Dimensions in mm
num_bays = 3
bay_length = 1500.0
frame_width = 800.0    # Center-to-center distance of legs
frame_height = 1000.0  # Height to top of legs

# Derived dimensions
total_frame_length = num_bays * bay_length
rail_length = total_frame_length + 400.0 # Rails overhang the frame

# Component sizes
leg_size = 80.0        # Square tube profile for legs
beam_size = 60.0       # Square tube profile for cross/longitudinal beams
foot_size = 150.0      # Square foot plate
foot_thick = 15.0
cap_thick = 15.0       # Plate between leg and rail

# Rail (I-Beam) Profile
rail_height = 160.0
rail_width = 100.0
rail_web_t = 10.0
rail_flange_t = 12.0

# Beam positions
lower_beam_elevation = 250.0  # Center height of lower beams

# --- Helper Functions ---

def create_ibeam_profile(workplane, w, h, tw, tf):
    """
    Draws an I-beam profile on the provided workplane.
    Origin is at the geometric center of the profile.
    """
    # Points defined clockwise starting from bottom-left
    pts = [
        (-w/2, -h/2), (w/2, -h/2),                # Bottom edge
        (w/2, -h/2 + tf), (tw/2, -h/2 + tf),      # Bottom right fillet area
        (tw/2, h/2 - tf), (w/2, h/2 - tf),        # Web right
        (w/2, h/2), (-w/2, h/2),                  # Top edge
        (-w/2, h/2 - tf), (-tw/2, h/2 - tf),      # Top left fillet area
        (-tw/2, -h/2 + tf), (-w/2, -h/2 + tf),    # Web left
        (-w/2, -h/2)                              # Close loop
    ]
    return workplane.polyline(pts).close()

# --- Geometry Construction ---

parts = []

# 1. Legs, Feet, and Cap Plates
start_x = -total_frame_length / 2
leg_positions = [] # Store for cross beams

for i in range(num_bays + 1):
    x = start_x + i * bay_length
    leg_positions.append(x)
    
    for side in [-1, 1]:
        y = side * frame_width / 2
        
        # Leg (Vertical Column)
        # Extrudes from foot thickness up to frame height
        leg = (
            cq.Workplane("XY")
            .workplane(offset=foot_thick)
            .center(x, y)
            .box(leg_size, leg_size, frame_height - foot_thick, centered=(True, True, False))
        )
        parts.append(leg)
        
        # Foot Plate
        foot = (
            cq.Workplane("XY")
            .center(x, y)
            .box(foot_size, foot_size, foot_thick, centered=(True, True, False))
        )
        parts.append(foot)
        
        # Cap Plate (Top of leg)
        cap = (
            cq.Workplane("XY")
            .workplane(offset=frame_height)
            .center(x, y)
            .box(leg_size, leg_size, cap_thick, centered=(True, True, False))
        )
        parts.append(cap)

# 2. Longitudinal Beams (Lengthwise)
# We create continuous beams for structural rigidity visuals
# Lower Level
for side in [-1, 1]:
    y = side * frame_width / 2
    
    # Lower Beam
    beam_low = (
        cq.Workplane("XY")
        .workplane(offset=lower_beam_elevation)
        .center(0, y)
        .box(total_frame_length + leg_size, beam_size, beam_size) # Flush with leg outsides
    )
    parts.append(beam_low)
    
    # Upper Beam (Just below the cap plate)
    upper_beam_z = frame_height - beam_size/2
    beam_high = (
        cq.Workplane("XY")
        .workplane(offset=upper_beam_z)
        .center(0, y)
        .box(total_frame_length + leg_size, beam_size, beam_size)
    )
    parts.append(beam_high)

# 3. Cross Beams (Widthwise)
# Placed at each leg location
for x in leg_positions:
    
    # Lower Cross Beam
    cb_low = (
        cq.Workplane("XY")
        .workplane(offset=lower_beam_elevation)
        .center(x, 0)
        .box(beam_size, frame_width - leg_size, beam_size) # Span between legs
    )
    parts.append(cb_low)
    
    # Upper Cross Beam
    upper_beam_z = frame_height - beam_size/2
    cb_high = (
        cq.Workplane("XY")
        .workplane(offset=upper_beam_z)
        .center(x, 0)
        .box(beam_size, frame_width - leg_size, beam_size)
    )
    parts.append(cb_high)

# 4. Top Rails (I-Beams)
# Rails sit on top of the cap plates
rail_base_z = frame_height + cap_thick

# Create base I-beam extrusion centered on origin
rail_geo = (
    create_ibeam_profile(cq.Workplane("YZ"), rail_width, rail_height, rail_web_t, rail_flange_t)
    .extrude(rail_length, both=True) # Extrude along X
)

# Position Rails
for side in [-1, 1]:
    y = side * frame_width / 2
    # Shift rail to correct Y and Z position
    # Initial rail center is at (0,0,0). 
    # Move Z up by rail_base_z + rail_height/2
    rail = rail_geo.translate((0, y, rail_base_z + rail_height/2))
    parts.append(rail)

# --- Final Assembly ---
# Combine all parts into a single compound object
result = parts[0]
for part in parts[1:]:
    result = result.union(part)

# Export or Render
if 'show_object' in globals():
    show_object(result)