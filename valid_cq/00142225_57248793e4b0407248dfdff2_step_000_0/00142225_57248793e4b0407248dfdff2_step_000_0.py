import cadquery as cq
import math

# --- Parameters (in mm) ---
length = 2400.0
width = 1500.0
main_profile = 50.0   # 50x50mm square tubing for main frame
grid_profile = 30.0   # 30x30mm tubing for floor grid
rail_profile = 40.0   # 40x40mm tubing for upper rails
rail_height = 300.0   # Height of the side rails
tongue_length = 1100.0
side_ext_width = 200.0 # Width of the side extension/step

# --- Helper Function ---
def make_tube(l, w, h, x=0, y=0, z=0, rz=0):
    """Creates a solid box representing a tube, rotated around Z and translated."""
    return (cq.Workplane("XY")
            .box(l, w, h)
            .rotate((0,0,0), (0,0,1), rz)
            .translate((x, y, z)))

# --- 1. Main Chassis Frame ---
# Side beams (Longitudinal)
# Located at the outer edges of the width
side_l = make_tube(length, main_profile, main_profile, 0, width/2 - main_profile/2, 0)
side_r = make_tube(length, main_profile, main_profile, 0, -(width/2 - main_profile/2), 0)

# End beams (Transverse)
# Connecting the side beams at front and back
end_f = make_tube(main_profile, width - 2*main_profile, main_profile, length/2 - main_profile/2, 0, 0)
end_b = make_tube(main_profile, width - 2*main_profile, main_profile, -length/2 + main_profile/2, 0, 0)

frame = side_l.union(side_r).union(end_f).union(end_b)

# --- 2. Floor Grid ---
# Internal grid of smaller tubing
# Longitudinal dividers
num_long_divs = 3
spacing_long = (width - 2*main_profile) / (num_long_divs + 1)
grid_long_geo = cq.Workplane("XY")

for i in range(num_long_divs):
    y_pos = -(width/2 - main_profile) + (i + 1) * spacing_long
    # Create beam centered at y_pos
    beam = make_tube(length - 2*main_profile, grid_profile, grid_profile, 0, y_pos, 0)
    grid_long_geo = grid_long_geo.union(beam)

# Transverse dividers
num_trans_divs = 6
spacing_trans = (length - 2*main_profile) / (num_trans_divs + 1)
grid_trans_geo = cq.Workplane("XY")

for i in range(num_trans_divs):
    x_pos = -(length/2 - main_profile) + (i + 1) * spacing_trans
    # Spanning full inner width
    beam = make_tube(grid_profile, width - 2*main_profile, grid_profile, x_pos, 0, 0)
    grid_trans_geo = grid_trans_geo.union(beam)

frame = frame.union(grid_long_geo).union(grid_trans_geo)

# --- 3. Upper Railing Structure ---
# Vertical Posts
post_z = main_profile/2 + rail_height/2
post_locs = [
    (length/2 - main_profile/2, width/2 - main_profile/2),    # Front Left
    (length/2 - main_profile/2, -(width/2 - main_profile/2)), # Front Right
    (-length/2 + main_profile/2, width/2 - main_profile/2),   # Rear Left
    (-length/2 + main_profile/2, -(width/2 - main_profile/2)),# Rear Right
    (0, width/2 - main_profile/2),                            # Mid Left
    (0, -(width/2 - main_profile/2))                          # Mid Right
]

posts = cq.Workplane("XY")
for x, y in post_locs:
    p = make_tube(rail_profile, rail_profile, rail_height, x, y, post_z)
    posts = posts.union(p)

# Horizontal Rails
# Top rails sit flush with top of posts
rail_z = main_profile/2 + rail_height - rail_profile/2
top_rail_l = make_tube(length, rail_profile, rail_profile, 0, width/2 - main_profile/2, rail_z)
top_rail_r = make_tube(length, rail_profile, rail_profile, 0, -(width/2 - main_profile/2), rail_z)
top_rail_f = make_tube(rail_profile, width - 2*main_profile, rail_profile, length/2 - main_profile/2, 0, rail_z)

railing = posts.union(top_rail_l).union(top_rail_r).union(top_rail_f)

# --- 4. Tongue (A-Frame) ---
# Geometry calculation for V-shape
t_start_x = length/2
t_start_y_offset = width/2 - main_profile # Attach near corners
t_tip_x = length/2 + tongue_length
t_tip_y = 0

dx = t_tip_x - t_start_x
dy = t_tip_y - t_start_y_offset # Negative
beam_len = math.sqrt(dx**2 + dy**2)
angle = math.degrees(math.atan2(dy, dx))

# Left Arm (Y+)
arm_l = make_tube(beam_len, main_profile, main_profile, 
                  t_start_x + dx/2, t_start_y_offset + dy/2, 0, angle)

# Right Arm (Y-)
# Symmetric angle
arm_r = make_tube(beam_len, main_profile, main_profile, 
                  t_start_x + dx/2, -(t_start_y_offset + dy/2), 0, -angle)

# Hitch Plate at tip
hitch = (cq.Workplane("XY")
         .box(150, 150, 10)
         .translate((t_tip_x, 0, main_profile/2 + 5)))

tongue = arm_l.union(arm_r).union(hitch)

# --- 5. Side Extension (Side Rack) ---
# Located on one side (Y+), spanning rear half
ext_len = length * 0.45
ext_x = -length * 0.2
ext_y = width/2 + side_ext_width
ext_z = rail_z

# Outer rail of extension
ext_rail = make_tube(ext_len, rail_profile, rail_profile, ext_x, ext_y, ext_z)
# Connecting struts
strut_1 = make_tube(rail_profile, side_ext_width, rail_profile, 
                    ext_x - ext_len/2 + rail_profile/2, width/2 + side_ext_width/2, ext_z)
strut_2 = make_tube(rail_profile, side_ext_width, rail_profile, 
                    ext_x + ext_len/2 - rail_profile/2, width/2 + side_ext_width/2, ext_z)

side_extension = ext_rail.union(strut_1).union(strut_2)

# --- 6. Axle Hangers ---
# Triangular brackets under the frame
hanger_shape = (cq.Workplane("XZ")
                .moveTo(0,0)
                .lineTo(30, -80)
                .lineTo(-30, -80)
                .close()
                .extrude(10) # Thickness
                .translate((0, -5, -main_profile/2)))

hangers = cq.Workplane("XY")
hanger_x_base = -length * 0.1
# Create 2 hangers per side
for x_off in [-40, 40]:
    # Left side
    h1 = hanger_shape.translate((hanger_x_base + x_off, width/2 - main_profile/2, 0))
    # Right side
    h2 = hanger_shape.translate((hanger_x_base + x_off, -(width/2 - main_profile/2), 0))
    hangers = hangers.union(h1).union(h2)

# --- Final Assembly ---
result = frame.union(railing).union(tongue).union(side_extension).union(hangers)