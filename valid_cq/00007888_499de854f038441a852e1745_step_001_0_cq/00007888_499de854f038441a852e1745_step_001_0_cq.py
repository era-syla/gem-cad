import cadquery as cq

# --- Parametric Variables ---
# GoPro Mount Dimensions
mount_tab_thickness = 3.0
mount_gap_thickness = 3.0
mount_radius = 7.5
mount_hole_dia = 5.0
mount_base_length = 15.0  # Length of the part connecting to the arm
mount_base_width = (3 * mount_tab_thickness) + (2 * mount_gap_thickness)

# Arm Dimensions
arm_length = 50.0
arm_thickness = 4.0
arm_height_start = 4.0
arm_height_end = 20.0  # Increases towards the clip side
chamfer_size = 1.0

# Truss/Triangle Cutout Dimensions
truss_wall_thickness = 3.0

# Clip/Hook Dimensions (the C-shaped parts)
clip_rod_dia = 8.0  # Estimated diameter of the rod it clips onto
clip_thickness = 5.0
clip_width = 8.0
clip_opening_gap = 5.0 # Opening to snap onto the rod
vertical_spacing = 30.0 # Distance between the two clips

# --- Helper Functions ---

def create_gopro_tabs():
    """Creates the standard 3-tab GoPro interface."""
    
    # Create a single tab profile
    tab = (
        cq.Workplane("XY")
        .circle(mount_radius)
        .extrude(mount_tab_thickness)
    )
    
    # Create the hole
    tab = tab.faces(">Z").workplane().hole(mount_hole_dia)
    
    # Create the rectangular base for the tab to merge into the main body
    # It needs to be tangent to the bottom of the circle
    base_rect = (
        cq.Workplane("XY")
        .center(0, -mount_radius/2)
        .rect(mount_radius*2, mount_radius)
        .extrude(mount_tab_thickness)
    )
    
    single_tab = tab.union(base_rect)
    
    # Arrange 3 tabs with gaps
    tabs = single_tab
    
    # Second tab
    t2 = single_tab.translate((0, 0, mount_tab_thickness + mount_gap_thickness))
    tabs = tabs.union(t2)
    
    # Third tab
    t3 = single_tab.translate((0, 0, (mount_tab_thickness + mount_gap_thickness) * 2))
    tabs = tabs.union(t3)
    
    # Center the assembly
    total_height = (3 * mount_tab_thickness) + (2 * mount_gap_thickness)
    tabs = tabs.translate((0, 0, -total_height/2 + mount_tab_thickness/2))
    
    # Rotate to correct orientation (Holes along Y axis in final assembly context)
    # The current orientation has holes along Z. 
    # Let's align it so the tabs stick up.
    tabs = tabs.rotate((0,0,0), (1,0,0), 90)
    
    return tabs

def create_c_clip():
    """Creates a single C-shaped clip."""
    outer_r = (clip_rod_dia / 2) + 2.5 # Wall thickness approx 2.5
    inner_r = clip_rod_dia / 2
    
    clip = (
        cq.Workplane("XY")
        .circle(outer_r)
        .extrude(clip_width)
    )
    
    # Cut the inner hole
    clip = clip.faces(">Z").workplane().hole(clip_rod_dia)
    
    # Cut the opening slot
    slot_cutout = (
        cq.Workplane("XY")
        .rect(outer_r * 2.5, clip_opening_gap)
        .extrude(clip_width)
    )
    
    # Rotate cutout to face the right direction (approx 45 degrees usually works well for snaps)
    # But looking at image, they seem to face somewhat inwards/angled.
    # Let's just cut straight "out" relative to the arm connection point.
    # Based on image, opening faces somewhat 'up' for the top one and 'down' for bottom one?
    # Actually, they look like standard snap hooks. Let's cut a slot.
    
    # Position the slot to cut the side
    slot_cutout = slot_cutout.translate((outer_r, 0, 0))
    clip = clip.cut(slot_cutout)
    
    return clip

# --- Main Construction ---

# 1. Build the main arm body (L-shape structure)
# We will draw the profile on the XZ plane and extrude Y
pts = [
    (0, 0),
    (arm_length, 0),
    (arm_length, -vertical_spacing/2 - 5), # Bottom vertical extent
    (arm_length - 5, -vertical_spacing/2 - 5),
    (arm_length - 5, 0), # Back up inner wall
    (0, 0) # Closing (we will loft or just make a complex shape)
]

# Let's construct it from primitives for better control over the triangular truss
# Main horizontal bar
arm = (
    cq.Workplane("XY")
    .box(arm_length, mount_base_width, arm_thickness)
    .translate((arm_length/2, 0, 0))
)

# The vertical post at the end
vertical_post_height = vertical_spacing + 15 # rough total height
vertical_post = (
    cq.Workplane("YZ")
    .box(mount_base_width, vertical_post_height, arm_thickness)
    .rotate((0,0,0), (0,1,0), 90) # Orient correctly
    .translate((arm_length - arm_thickness/2, 0, -vertical_post_height/2 + arm_thickness/2 + vertical_spacing/2))
)

# The triangular reinforcement (truss)
# Vertices for the triangle on XZ plane
v1 = (15, -arm_thickness/2) # Start of angle on horizontal arm
v2 = (arm_length - arm_thickness, -arm_thickness/2) # Corner
v3 = (arm_length - arm_thickness, -vertical_spacing/2) # Point down the vertical post

truss = (
    cq.Workplane("XZ")
    .polyline([v1, v2, v3, v1])
    .close()
    .extrude(mount_base_width/2, both=True) # Extrude centered
)

# Combine structure
body = arm.union(vertical_post).union(truss)

# Create the cutout in the truss
# Offset inwards
cutout_v1 = (v1[0] + 5, v1[1] - 3)
cutout_v2 = (v2[0] - 3, v2[1] - 3)
cutout_v3 = (v3[0] - 3, v3[1] + 5)

truss_cutout = (
    cq.Workplane("XZ")
    .polyline([cutout_v1, cutout_v2, cutout_v3, cutout_v1])
    .close()
    .extrude(mount_base_width/2 + 1, both=True) # Cut through
)

body = body.cut(truss_cutout)

# 2. Add GoPro Mount
tabs = create_gopro_tabs()
# Position tabs at the start of the arm (0,0,0), slightly raised
tabs = tabs.rotate((0,0,0), (0,0,1), 90) # Align with arm direction
tabs = tabs.translate((0, 0, arm_thickness/2 + mount_radius/2)) 
# Shift slightly forward to overhang edge like in picture
tabs = tabs.translate((-mount_radius + 2, 0, 0))

# Create a small base block for the tabs to sit on smoothly
tab_base = (
    cq.Workplane("XY")
    .box(mount_radius*2, mount_base_width, arm_thickness)
    .translate((0, 0, 0))
)

body = body.union(tabs).union(tab_base)

# 3. Add Clips
# Top Clip
top_clip = create_c_clip()
# Rotate so cylinder axis is Y
top_clip = top_clip.rotate((0,0,0), (1,0,0), 90)
# Rotate opening
top_clip = top_clip.rotate((0,0,0), (0,1,0), -45) 
# Position
top_pos_z = vertical_spacing/2 
top_clip = top_clip.translate((arm_length, 0, top_pos_z))

# Bottom Clip
bottom_clip = create_c_clip()
bottom_clip = bottom_clip.rotate((0,0,0), (1,0,0), 90)
# Rotate opening opposite way
bottom_clip = bottom_clip.rotate((0,0,0), (0,1,0), -135)
# Position
bottom_pos_z = -vertical_spacing/2
bottom_clip = bottom_clip.translate((arm_length, 0, bottom_pos_z))


# Union everything
result = body.union(top_clip).union(bottom_clip)

# Final cleanups / Chamfers
# Apply chamfers to sharp edges for strength and aesthetics (optional but good practice)
try:
    result = result.edges("|Y").filter_by(lambda e: e.boundingBox().min.x > 5 and e.boundingBox().min.x < arm_length-5).chamfer(0.5)
except:
    pass # Skip if selection is tricky geometrically

# Ensure the "result" variable is available
result = result