import cadquery as cq

# --- Dimensions and Parameters ---
# Pulley Wheel Parameters
pulley_od = 40.0
shaft_diam = 5.0
hub_od = 12.0
rim_width = 4.0      # Radial width of the outer rim
half_height = 5.0    # Height of one pulley half
web_thickness = 2.0  # Thickness of the connecting web
web_z_offset = 2.5   # Z-height of the web top surface relative to mating face

# Base Parameters
base_cyl_r = 8.0
base_cyl_h = 10.0
arm_length = 25.0
arm_width = 10.0
arm_height = 8.0
post_height = 25.0   # Height of the central shaft post

# Derived Dimensions
shaft_r = shaft_diam / 2.0
hub_r = hub_od / 2.0
rim_inner_r = (pulley_od / 2.0) - rim_width
rim_outer_r = pulley_od / 2.0

def create_pulley_half():
    """
    Creates one half of the pulley assembly.
    Designed with the mating face at Z=0 and features extending to +Z.
    """
    # 1. Define the profile for revolution on the XZ plane
    # Points correspond to the cross-section of the right side
    pts = [
        (shaft_r, 0),                   # Start at shaft hole, mating face
        (shaft_r, half_height),         # Up shaft wall
        (hub_r, half_height),           # Out to Hub OD
        (hub_r, web_z_offset),          # Down to Web top
        (rim_inner_r, web_z_offset),    # Across Web to Rim
        (rim_inner_r, half_height),     # Up Rim inner wall
        (rim_outer_r, half_height),     # Out to Rim OD
        (rim_outer_r, 1.5),             # Down Rim outer wall (start of bevel)
        (rim_outer_r - 2.0, 0),         # Bevel/Taper down to mating face (creates V-groove)
        (shaft_r, 0)                    # Close loop at start
    ]
    
    # 2. Revolve to create the base solid
    part = cq.Workplane("XZ").polyline(pts).close().revolve()
    
    # 3. Cut Kidney Slots in the web
    # We use slot2D on a polar array. 
    # Slot is rotated 90 degrees to align tangentially with the radius.
    slot_center_r = (hub_r + rim_inner_r) / 2.0
    slot_len = 10.0
    slot_width = 3.5
    
    part = (part.faces(">Z").workplane()
            .polarArray(slot_center_r, 0, 360, 4)
            .slot2D(slot_len, slot_width, 90)
            .cutBlind(-half_height)
           )
           
    # 4. Optional: Fillet edges for aesthetics (commented out for stability)
    # part = part.edges("|Z").fillet(0.2)
    
    return part

def create_base():
    """
    Creates the base unit with a vertical post and a horizontal arm.
    """
    # Main Cylindrical Base
    base = cq.Workplane("XY").circle(base_cyl_r).extrude(base_cyl_h)
    
    # Horizontal Arm
    # Positioned to extend from the center to the left (-X)
    arm = (cq.Workplane("XY")
           .center(-arm_length/2.0, 0)
           .rect(arm_length, arm_width)
           .extrude(arm_height)
          )
    
    base = base.union(arm)
    
    # Central Post (Shaft)
    # Slightly smaller than hole for clearance logic, but same size for model visual
    post = cq.Workplane("XY").circle(shaft_r - 0.05).extrude(post_height)
    base = base.union(post)
    
    # Mounting hole at the end of the arm
    base = (base.faces(">Z").workplane()
            .moveTo(-arm_length + 5, 0)
            .circle(2.0)
            .cutBlind(-arm_height)
           )
           
    # Fillet the junction between arm and cylinder
    # Selecting vertical edges near the origin
    try:
        base = base.edges("|Z").filterByPos((0,0,0), 10).fillet(1.0)
    except:
        pass # Skip if selection fails
        
    return base

# --- Assembly Construction ---

# Generate components
base_geo = create_base()
pulley_half_1 = create_pulley_half()
pulley_half_2 = create_pulley_half()

# Position Components
# The base top surface is at Z = base_cyl_h

# Bottom Pulley Half:
# Needs to be inverted so the mating face (Z=0) points UP.
# Rotating 180 deg around X makes Z range [-5, 0] with mating face at 0.
# We move it up so the back face (now at -5) sits on the base (Z=10).
# Translation Z = 10 + 5 = 15.
# Final Z range: [10, 15]. Mating face at 15.
p1_loc = (0, 0, base_cyl_h + half_height)
p1_rotated = pulley_half_1.rotate((0,0,0), (1,0,0), 180).translate(p1_loc)

# Top Pulley Half:
# Mating face (Z=0) points DOWN.
# Geometry Z range is [0, 5].
# We move it up so mating face (0) touches the bottom half mating face (15).
# Translation Z = 15.
# Final Z range: [15, 20].
p2_loc = (0, 0, base_cyl_h + half_height)
p2_translated = pulley_half_2.translate(p2_loc)

# Combine into a single result
result = base_geo.union(p1_rotated).union(p2_translated)