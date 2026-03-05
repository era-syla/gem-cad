import cadquery as cq
import math

# Tire parameters
outer_radius = 50
inner_radius = 28
tire_width = 35
tread_height = 4
rim_radius = 22
rim_width = 28

# Create the basic tire torus shape by revolving a profile
# Cross-section of tire in 2D
def make_tire_profile():
    # Tire cross section - roughly circular/oval profile
    r_mid = (outer_radius + inner_radius) / 2  # ~39
    r_cross = (outer_radius - inner_radius) / 2  # ~11
    w_half = tire_width / 2  # ~17.5
    
    pts = []
    steps = 32
    for i in range(steps + 1):
        angle = math.pi * i / steps  # 0 to pi
        # Parametric cross section
        x = r_cross * math.cos(math.pi - angle)
        y = w_half * math.sin(math.pi - angle) * 0.85
        pts.append((r_mid + x, y))
    
    return pts

# Build tire body by revolving
profile_pts = make_tire_profile()

tire_profile = (
    cq.Workplane("XZ")
    .spline(profile_pts)
    .close()
)

# Create tire torus using revolve
# Use a simpler approach: revolve a 2D profile around Y axis
r_mid = (outer_radius + inner_radius) / 2
r_cross = (outer_radius - inner_radius) / 2
w_half = tire_width / 2

# Build profile in XY plane, revolve around Y axis
pts = []
steps = 24
for i in range(steps + 1):
    angle = 2 * math.pi * i / steps
    x = r_mid + r_cross * math.cos(angle)
    y = w_half * 0.85 * math.sin(angle)
    pts.append((x, y))

tire_body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Create rim
rim = (
    cq.Workplane("XY")
    .cylinder(rim_width, rim_radius)
)

# Add rim flange
rim_flange = (
    cq.Workplane("XY")
    .cylinder(4, rim_radius + 4)
)

# Combine tire and rim
result = tire_body.union(rim)

# Add tread blocks
# Tread blocks arranged in rows around the tire
num_blocks_circumference = 18
num_rows = 3

tread_result = result

for row in range(num_rows):
    # Row offset angle
    row_offset = (row * 360 / num_blocks_circumference / num_rows)
    # Row lateral position
    if row == 0:
        lat_offset = 0
        block_width = 10
        block_len = 8
    elif row == 1:
        lat_offset = 11
        block_width = 8
        block_len = 7
    else:
        lat_offset = -11
        block_width = 8
        block_len = 7
    
    for i in range(num_blocks_circumference):
        angle_deg = i * 360 / num_blocks_circumference + row_offset
        angle_rad = math.radians(angle_deg)
        
        # Position on tire surface
        bx = (outer_radius + tread_height/2) * math.cos(angle_rad)
        bz = (outer_radius + tread_height/2) * math.sin(angle_rad)
        by = lat_offset
        
        block = (
            cq.Workplane("XY")
            .box(block_len, block_width, tread_height)
            .rotate((0, 0, 0), (0, 0, 1), angle_deg)
            .translate((bx, by, bz))
        )
        
        tread_result = tread_result.union(block)

# Hollow out the inside of the tire (wheel well)
hollow = (
    cq.Workplane("XY")
    .cylinder(tire_width + 2, inner_radius)
)

result = tread_result.cut(hollow)

# Add back the rim
result = result.union(rim)