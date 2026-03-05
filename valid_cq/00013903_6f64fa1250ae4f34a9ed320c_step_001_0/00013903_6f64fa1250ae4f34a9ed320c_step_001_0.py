import cadquery as cq

# --- Parameters ---
shaft_radius = 4.5
head_radius = 10.0
total_length = 150.0

# --- 1. Main Revolved Body (Shaft + Head + Tail steps) ---
# Define profile points in XY plane (X=axis, Y=radius)
profile_pts = [
    (0, 0),                 # Center start
    (0, 3.0),               # Nose flat
    (2.0, 5.0),             # Nose taper
    (5.0, 8.0),             # Head dome start
    (8.0, head_radius),     # Head full diameter
    (28.0, head_radius),    # Head straight section
    (28.0, head_radius-1.0),# Groove down
    (31.0, head_radius-1.0),# Groove bottom
    (31.0, head_radius),    # Groove up
    (34.0, head_radius),    # Land after groove
    (42.0, shaft_radius),   # Taper to shaft
    (115.0, shaft_radius),  # Shaft straight section
    (117.0, shaft_radius+2.0), # Rear collar step 1
    (122.0, shaft_radius+2.0), # Rear collar land
    (124.0, shaft_radius+4.0), # Rear collar step 2
    (130.0, shaft_radius+4.0), # Rear collar land
    (130.0, 0)              # Close loop
]

main_body = cq.Workplane("XY").polyline(profile_pts).close().revolve()

# --- 2. Rear Foot Plate ---
# Rectangular plate with chamfered corners
foot_width_z = 28.0
foot_height_y = 18.0
foot_thick_x = 6.0

foot = (
    cq.Workplane("YZ")
    .workplane(offset=130.0)
    .rect(foot_height_y, foot_width_z) # dim1=Y-axis, dim2=Z-axis in YZ plane
    .extrude(foot_thick_x)
)
# Chamfer edges parallel to extrusion (X-axis) to create the octagonal profile
foot = foot.edges("|X").chamfer(4.0)

# --- 3. Front Underslung Assembly (Spring/Damper detail) ---
# Located under the main head
sub_rad = 3.5
sub_x_start = 12.0
sub_y_offset = -12.5
sub_len = 20.0

# Cylinder core
sub_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=sub_x_start)
    .moveTo(0, sub_y_offset)
    .circle(sub_rad)
    .extrude(sub_len)
)

# Ribs/Rings on the sub cylinder
for i in range(5):
    rib_offset = sub_x_start + 3.0 + (i * 3.5)
    rib = (
        cq.Workplane("YZ")
        .workplane(offset=rib_offset)
        .moveTo(0, sub_y_offset)
        .circle(sub_rad + 0.8)
        .extrude(1.5)
    )
    sub_cyl = sub_cyl.union(rib)

# Front cap (rounded)
sub_cap = (
    cq.Workplane("YZ")
    .workplane(offset=sub_x_start)
    .moveTo(0, sub_y_offset)
    .circle(sub_rad)
    .extrude(-2.0)
    .edges("<X").fillet(1.5)
)
sub_cyl = sub_cyl.union(sub_cap)

# Connector block between main head and sub cylinder
connector = (
    cq.Workplane("XY")
    .moveTo(sub_x_start + 10.0, sub_y_offset/2.0)
    .rect(14.0, abs(sub_y_offset)) 
    .extrude(6.0)
    .translate((0, 0, -3.0)) # Center Z
)

# --- 4. Middle Mounting Bracket ---
# L-shaped lug roughly halfway down the shaft
bracket_x = 80.0
bracket_width = 12.0

# Collar ring
collar = (
    cq.Workplane("YZ")
    .workplane(offset=bracket_x)
    .circle(shaft_radius + 2.5)
    .extrude(bracket_width)
)

# Lower block
mount_block = (
    cq.Workplane("XY")
    .moveTo(bracket_x + bracket_width/2.0, -8.0)
    .rect(bracket_width, 10.0)
    .extrude(10.0)
    .translate((0, 0, -5.0))
)

# --- Final Boolean Union ---
result = (
    main_body
    .union(foot)
    .union(sub_cyl)
    .union(connector)
    .union(collar)
    .union(mount_block)
)