import cadquery as cq

def make_2020_profile(length):
    """
    Creates a detailed 2020 T-slot aluminum extrusion profile of the specified length.
    Includes filleted corners, T-slots on all sides, and a center hole.
    """
    # Profile dimensions
    s = 20.0          # Size of the square profile
    h_s = s / 2.0     # Half size
    
    # Slot dimensions (approximate for generic 2020)
    slot_w1 = 6.0     # Opening width
    slot_w2 = 10.0    # Internal cavity width
    slot_d1 = 1.8     # Neck depth
    slot_d2 = 4.2     # Internal cavity depth
    
    # 1. Create the main body (square with filleted corners)
    # Extruded along the Z-axis
    body = cq.Workplane("XY").rect(s, s).extrude(length)
    # Apply fillets to the four longitudinal edges
    body = body.edges("|Z").fillet(1.0)
    
    # 2. Define the slot cutter shape (T-profile)
    # Coordinates defined for the top face (positive Y) relative to center
    p1 = (-slot_w1/2, h_s)
    p2 = (slot_w1/2, h_s)
    p3 = (slot_w1/2, h_s - slot_d1)
    p4 = (slot_w2/2, h_s - slot_d1)
    p5 = (slot_w2/2, h_s - slot_d1 - slot_d2)
    p6 = (-slot_w2/2, h_s - slot_d1 - slot_d2)
    p7 = (-slot_w2/2, h_s - slot_d1)
    p8 = (-slot_w1/2, h_s - slot_d1)
    
    slot_pts = [p1, p2, p3, p4, p5, p6, p7, p8]
    
    # Create the cutter solid for one slot
    slot_cutter = cq.Workplane("XY").polyline(slot_pts).close().extrude(length)
    
    # Create a unified cutter with slots rotated for all 4 sides
    full_cutter = slot_cutter
    for i in range(1, 4):
        full_cutter = full_cutter.union(slot_cutter.rotate((0, 0, 0), (0, 0, 1), i * 90))
        
    # 3. Create center hole cutter
    center_hole = cq.Workplane("XY").circle(2.5).extrude(length)
    
    # 4. Subtract cutters from the main body
    final_profile = body.cut(full_cutter).cut(center_hole)
    
    return final_profile

# --- Model Construction ---

# Parametric Dimensions
profile_width = 20.0
vert_length_up = 400.0   # Length extending upwards from intersection
vert_length_down = 100.0 # Length extending downwards from intersection
leg_length = 250.0       # Length of horizontal legs

# 1. Vertical Column
# The column is one continuous piece. We position it relative to the intersection point (0,0,0).
# Extrusion creates the object from Z=0 to Z=Length.
total_vert_len = vert_length_up + vert_length_down
v_col = make_2020_profile(total_vert_len)
# Shift down so the intersection point aligns with the global origin
v_col = v_col.translate((0, 0, -vert_length_down))

# 2. Horizontal Leg 1 (X-axis)
# Butt joint against the vertical column face.
leg_x = make_2020_profile(leg_length)
# Rotate 90 degrees around Y-axis to align with X-axis
leg_x = leg_x.rotate((0, 0, 0), (0, 1, 0), 90)
# Translate to start at the face of the vertical profile (X = width/2)
leg_x = leg_x.translate((profile_width / 2, 0, 0))

# 3. Horizontal Leg 2 (Y-axis)
# Butt joint against the vertical column face.
leg_y = make_2020_profile(leg_length)
# Rotate -90 degrees around X-axis to align with Y-axis
leg_y = leg_y.rotate((0, 0, 0), (1, 0, 0), -90)
# Translate to start at the face of the vertical profile (Y = width/2)
leg_y = leg_y.translate((0, profile_width / 2, 0))

# Combine all parts into a single solid assembly
result = v_col.union(leg_x).union(leg_y)