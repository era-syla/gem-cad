import cadquery as cq
from math import radians, cos, sin

# --- Parametric Variables ---
# Base Structure (Twin Beams)
beam_width = 100
beam_height = 100
beam_length = 800
beam_gap = 50
beam_wall_thickness = 5  # Estimated for U-channel or hollow box

# Vertical Posts
post_size = 20
post_height_tall = 600
post_height_short = 450
post_offset_x = 300  # Distance from one end
post_spacing_y = beam_width + beam_gap + 20

# Control Box
box_size = 150
box_height_offset = 350
box_x_pos = 150

# Safety Guard / Railing
rail_radius = 100
rail_tube_r = 5
rail_height_offset = 550
rail_extension = 200

# Cylindrical Features (Sensors/Stops)
cyl_diam = 40
cyl_height = 50
cyl_pos_x = -150

# --- Helper Functions ---

def create_u_beam(length, width, height, thickness):
    """Creates a U-channel beam."""
    pts = [
        (0, 0),
        (width, 0),
        (width, height),
        (width - thickness, height),
        (width - thickness, thickness),
        (thickness, thickness),
        (thickness, height),
        (0, height)
    ]
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

# --- Geometry Construction ---

# 1. Base Beams (The twin parallel structures)
# Left Beam (Box profile for simplicity based on image, or U-channel facing down)
beam_left = cq.Workplane("XY").box(beam_length, beam_width, beam_height).translate((0, -(beam_width/2 + beam_gap/2), beam_height/2))
# Right Beam
beam_right = cq.Workplane("XY").box(beam_length, beam_width, beam_height).translate((0, (beam_width/2 + beam_gap/2), beam_height/2))

# Let's make them look a bit more like formed sheet metal or channels if possible, 
# but solid blocks are safer for robust generation unless specific detail is required. 
# Looking at the ends, the left one looks like an inverted U-channel.
beam_left = (
    cq.Workplane("YZ")
    .rect(beam_width, beam_height)
    .extrude(beam_length)
    .faces(">X").shell(-5) # Hollow it out
    .rotate((0,0,0), (0,1,0), 90) # Orient along X
    .translate((0, -(beam_width/2 + beam_gap/2), beam_height/2))
)

beam_right = (
    cq.Workplane("YZ")
    .rect(beam_width, beam_height)
    .extrude(beam_length)
    .faces(">X").shell(-5)
    .rotate((0,0,0), (0,1,0), 90)
    .translate((0, (beam_width/2 + beam_gap/2), beam_height/2))
)


# 2. Vertical Posts
# Tall Post (Right side in image)
post_tall = (
    cq.Workplane("XY")
    .rect(post_size, post_size)
    .extrude(post_height_tall)
    .translate((beam_length/2 - 50, (beam_width + beam_gap)/2 + post_size, post_height_tall/2))
)

# Shorter Post (Left side, holding the box)
post_short_x = beam_length/2 - 150
post_short = (
    cq.Workplane("XY")
    .rect(post_size, post_size)
    .extrude(post_height_short)
    .translate((post_short_x, -(beam_width + beam_gap)/2 - post_size, post_height_short/2))
)

# 3. Control Box
control_box = (
    cq.Workplane("XY")
    .box(box_size, box_size, box_size)
    .translate((post_short_x - box_size/2 - post_size, -(beam_width + beam_gap)/2 - post_size, box_height_offset))
)

# Support diagonal for the box
support_diag = (
    cq.Workplane("XY")
    .rect(post_size, post_size)
    .extrude(250)
    .rotate((0,1,0), (0,0,0), 45) # Tilt
    .translate((post_short_x - box_size - 50, -(beam_width + beam_gap)/2 - post_size, 100))
)

# 4. Connecting Horizontal Bars (between posts)
cross_bar_z = post_height_short - 20
cross_bar_len = (beam_width + beam_gap) + 2*post_size + 100 # Rough span
cross_bar = (
    cq.Workplane("YZ")
    .circle(post_size/2)
    .extrude(cross_bar_len)
    .translate((beam_length/2 - 50, -(cross_bar_len/2), cross_bar_z))
    .rotate((0,0,1), (0,0,0), 0)
)
# Actually the image shows a frame structure. Let's build a simpler U-frame connecting the posts.
# Connection from tall post to left
conn_bar_1 = (
    cq.Workplane("XY")
    .box(post_size, 300, post_size)
    .translate((beam_length/2 - 50, 0, post_height_tall - 100))
)


# 5. Safety Guard / Railing (Curved structure)
# Path for the railing
rail_path_pts = [
    (0, 0),
    (-150, 0),
    (-200, 50),
    (-200, 150),
    (-150, 200),
    (0, 200)
]
# This needs to be a sweep or constructed of tubes.
# Let's make a simplified assembly of cylinders and torus segments.

rail_start_x = post_short_x
rail_start_y = -(beam_width + beam_gap)/2 - post_size
rail_start_z = post_height_short + 50

# Main Hoop
hoop_radius = 120
hoop = (
    cq.Workplane("XY")
    .parametricCurve(lambda t: (
        hoop_radius * cos(t),
        hoop_radius * sin(t),
        0
    ))
    .sweep(cq.Workplane("XZ").circle(rail_tube_r))
    .translate((rail_start_x - 150, rail_start_y, rail_start_z))
)

# Straight sections connecting hoop to post
rail_connectors = (
    cq.Workplane("XY")
    .rect(200, 2*rail_tube_r)
    .extrude(2*rail_tube_r)
    .translate((rail_start_x - 100, rail_start_y + hoop_radius, rail_start_z))
    .union(
        cq.Workplane("XY")
        .rect(200, 2*rail_tube_r)
        .extrude(2*rail_tube_r)
        .translate((rail_start_x - 100, rail_start_y - hoop_radius, rail_start_z))
    )
)
# Vertical supports for rail
rail_supports = (
    cq.Workplane("XY")
    .rect(post_size, post_size)
    .extrude(150)
    .translate((rail_start_x, rail_start_y, rail_start_z - 75))
)

rail_assembly = hoop.union(rail_connectors).union(rail_supports)

# 6. Cylindrical Features on the Conveyor
cyl_1 = (
    cq.Workplane("XY")
    .circle(cyl_diam/2)
    .extrude(cyl_height)
    .translate((cyl_pos_x, 0, beam_height))
)
cyl_2 = (
    cq.Workplane("XY")
    .circle(cyl_diam/2)
    .extrude(cyl_height)
    .translate((cyl_pos_x + 100, 0, beam_height))
)

# Connecting plate between cylinders (the weird flap mechanism)
plate = (
    cq.Workplane("XY")
    .rect(150, 80)
    .extrude(5)
    .rotate((0,1,0), (0,0,0), -15) # Tilted
    .translate((cyl_pos_x + 50, 0, beam_height + cyl_height + 10))
)

# Top discs on cylinders
disc_1 = (
    cq.Workplane("XY")
    .circle(cyl_diam/2 + 5)
    .extrude(5)
    .translate((cyl_pos_x, 0, beam_height + cyl_height))
)
disc_2 = (
    cq.Workplane("XY")
    .circle(cyl_diam/2 + 5)
    .extrude(5)
    .translate((cyl_pos_x + 100, 0, beam_height + cyl_height))
)


# Combine all parts
result = (
    beam_left
    .union(beam_right)
    .union(post_tall)
    .union(post_short)
    .union(control_box)
    .union(support_diag)
    .union(conn_bar_1)
    .union(rail_assembly)
    .union(cyl_1)
    .union(cyl_2)
    .union(plate)
    .union(disc_1)
    .union(disc_2)
)