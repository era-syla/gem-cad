import cadquery as cq

# --- Parameter Definitions ---
# T-Slot Profile Dimensions (approximating a 2020 profile)
profile_size = 20.0
slot_width = 6.0
slot_depth = 6.0
center_hole_d = 5.0

# Assembly Dimensions
tower_height_tall = 500.0
tower_height_med = 400.0  # Approximated
tower_height_short = 350.0 # Approximated
radius_to_towers = 150.0  # Distance from center to vertical beams
base_arm_length = radius_to_towers - profile_size/2
central_hex_radius = 80.0 # Approximate radius for the central mechanism
central_hex_height = 10.0 # Height of the flat plate

# --- Helper Function: Create 2020 T-Slot Profile ---
def create_2020_profile(length):
    # Basic square
    s = cq.Workplane("XY").box(profile_size, profile_size, length)
    
    # Create the slots (running along Z)
    # Slot shape profile
    slot_profile = (
        cq.Workplane("XY")
        .rect(slot_width, profile_size + 2) # Vertical slot
        .extrude(length)
    )
    slot_profile_rot = (
        cq.Workplane("XY")
        .rect(profile_size + 2, slot_width) # Horizontal slot
        .extrude(length)
    )
    
    # Center hole
    center_hole = (
        cq.Workplane("XY")
        .circle(center_hole_d / 2)
        .extrude(length)
    )
    
    # Cut material
    s = s.cut(slot_profile).cut(slot_profile_rot).cut(center_hole)
    
    # Create the specific T-undercuts (simplified as boxes for visual fidelity without extreme complexity)
    # Normally 2020 has internal voids, but for this visual assembly, the external cross slot is key.
    # To make it look more real, let's chamfer the outer edges slightly
    s = s.edges("|Z").fillet(1.0)
    
    return s

# --- Build Components ---

# 1. The Vertical Towers
# There are 3 towers at 120 degrees separation.
# Looking at image: One is tall, one medium, one short.

# Define positions (polar coordinates)
positions = [
    (radius_to_towers, 90),    # Tallest one
    (radius_to_towers, 210),   # Medium
    (radius_to_towers, 330)    # Short
]

heights = [tower_height_tall, tower_height_med, tower_height_short]

towers = []
for i, (r, angle) in enumerate(positions):
    h = heights[i]
    tower = create_2020_profile(h)
    # Move so base is at Z=0? No, image shows horizontal arms connecting somewhat up the tower.
    # Let's assume the horizontal arms are at some Z height, say 50mm from bottom.
    # Let's align the bottom of the towers to Z=0 for simplicity.
    
    # Rotate and translate
    # By default, profile is at origin. Move it to radius.
    # We need to calculate XY from polar.
    # But wait, CadQuery rotate/translate makes this easier.
    
    tower = tower.translate((r, 0, h/2)) # Move out to radius, and up so bottom is at 0
    tower = tower.rotate((0,0,0), (0,0,1), angle)
    towers.append(tower)

# 2. Horizontal Arms
# These connect the center to the towers.
# They look like the same 2020 profile.
# They meet at a central vertical hub.

# Central Hub (Vertical piece in the middle)
central_hub_height = 150.0 # Looks like it sticks up a bit
central_hub = create_2020_profile(central_hub_height)
central_hub = central_hub.translate((0, 0, central_hub_height/2)) # Base at 0

# Horizontal spokes
arms = []
arm_z_level = 80.0 # Height where the horizontal arms connect
arm_len = radius_to_towers - profile_size # Approximate length needed

for i, (r, angle) in enumerate(positions):
    arm = create_2020_profile(arm_len)
    
    # Rotate the profile so it lies horizontally. 
    # Original is along Z. Rotate 90 around Y to point along X.
    arm = arm.rotate((0,0,0), (0,1,0), 90)
    
    # Shift it so one end is near center, other near tower
    # Length is arm_len. Center of mass is at (0,0,0) before rotate? No, Z-extrude starts at Z=0.
    # After extrude(L): Z is 0 to L.
    # After rotate 90 Y: X is 0 to L.
    
    arm = arm.translate((profile_size/2, 0, 0)) # Offset slightly from absolute center
    
    # Lift to height
    arm = arm.translate((0, 0, arm_z_level))
    
    # Rotate around Z to point to tower
    arm = arm.rotate((0,0,0), (0,0,1), angle)
    
    arms.append(arm)


# 3. The Hexagonal Base Structure
# The image shows a complex arrangement at the bottom. 
# There seems to be a plate (hexagon/circle) and short extrusion segments forming a perimeter.
# It looks like a delta printer effector or base.
# Let's model the plate first.

base_plate = (
    cq.Workplane("XY")
    .polygon(6, central_hex_radius * 2) # Diameter argument usually
    .extrude(5.0)
    .translate((0,0, 20.0)) # Lifted slightly off ground
)

# Perimeter segments on the hexagon
# There are pairs of short profiles attached to the sides of the hexagon plate.
# Looking closely, they look like linear rail carriages or just short 2020 blocks.
# Let's assume they are short 2020 segments mounted tangentially.

side_length = central_hex_radius # Roughly for hexagon
segment_len = side_length * 0.8
hex_segments = []

for i in range(6):
    angle = i * 60 + 30 # Faces are at 30, 90, 150...
    
    # Create segment
    seg = create_2020_profile(segment_len)
    # Lay horizontal
    seg = seg.rotate((0,0,0), (0,1,0), 90)
    
    # Position
    # Distance to flat of hex is radius * cos(30)
    dist_to_flat = central_hex_radius * 0.866
    
    # We want these on the outside of the plate
    offset_dist = dist_to_flat + profile_size/2
    
    seg = seg.translate((-segment_len/2, 0, 0)) # Center length
    seg = seg.translate((0, -offset_dist, 20.0 + 2.5)) # Move out and up to plate level
    
    # Rotate into position around center
    seg = seg.rotate((0,0,0), (0,0,1), angle)
    
    # The image actually shows doubled segments (top and bottom of plate?) 
    # or maybe a specialized carriage. 
    # It looks like there are two distinct blocks per side in the image, parallel.
    # Let's duplicate it slightly offset in Z to mimic the complex look.
    seg_top = seg.translate((0,0, 15))
    seg_bot = seg.translate((0,0, -15))
    
    hex_segments.append(seg_top)
    hex_segments.append(seg_bot)

# --- Combine All Geometry ---

result = cq.Workplane("XY")

# Add Towers
for t in towers:
    result = result.union(t)

# Add Central Hub
result = result.union(central_hub)

# Add Horizontal Arms
for a in arms:
    result = result.union(a)

# Add Base Plate
result = result.union(base_plate)

# Add Hex Segments
for s in hex_segments:
    result = result.union(s)

# Center the whole assembly visually if needed, but keeping absolute coordinates is usually safer.
# The `result` variable now holds the compound solid.