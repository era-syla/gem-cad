import cadquery as cq

# --- Parameters ---

# Cross Beam (X-Axis)
beam_length = 800.0
beam_width = 50.0
beam_height = 50.0
beam_wall_thk = 4.0

# Cradle / Pipe Support (Y-Axis)
cradle_length = 600.0
cradle_width = 100.0
cradle_block_height = 50.0
cradle_cut_radius = 42.0

# Connection Side Plates
conn_plate_length = 140.0
conn_plate_height = 40.0
conn_plate_thk = 5.0
conn_hole_spacing = 80.0
conn_hole_dia = 8.0

# Lifting Lugs
lug_width = 40.0
lug_height = 45.0  # Height above the beam
lug_thk = 5.0
lug_hole_dia = 10.0
lug_pair_gap = 20.0     # Gap between two lugs in a pair
lug_pair_spacing = 80.0 # Distance between the two pairs on one arm
lug_offset = 180.0      # Distance from center to the first pair

# --- 1. Create Cross Beam (Square Tube) ---
# Created along X axis, centered on Y
beam_outer = cq.Workplane("XY").box(beam_length, beam_width, beam_height)
beam_inner = cq.Workplane("XY").box(beam_length, beam_width - 2*beam_wall_thk, beam_height - 2*beam_wall_thk)
cross_beam = beam_outer.cut(beam_inner)

# --- 2. Create Cradle (Pipe Support) ---
# Sits on top of the cross beam. 
# Z position calculation: Beam top is at beam_height/2.
# Cradle block center Z is beam_height/2 + cradle_block_height/2.
cradle_z_center = beam_height/2 + cradle_block_height/2

cradle_base = (
    cq.Workplane("XY")
    .workplane(offset=cradle_z_center)
    .box(cradle_width, cradle_length, cradle_block_height)
)

# Create cylindrical cut along Y axis
# The geometric top of the cradle block is at Z = beam_height/2 + cradle_block_height
top_z = beam_height/2 + cradle_block_height
groove = (
    cq.Workplane("XZ")
    .workplane(offset=-cradle_length/2 - 10)
    .moveTo(0, top_z)
    .circle(cradle_cut_radius)
    .extrude(cradle_length + 20)
)

cradle = cradle_base.cut(groove)

# --- 3. Connection Plates ---
# Located on the side faces of the cross beam (+/- Y faces), centered at X=0
plate_sketch = (
    cq.Workplane("XZ")
    .rect(conn_plate_length, conn_plate_height)
    .extrude(conn_plate_thk)
)

# Add holes
plate_with_holes = (
    plate_sketch.faces(">Y").workplane()
    .pushPoints([(-conn_hole_spacing/2, 0), (conn_hole_spacing/2, 0)])
    .hole(conn_hole_dia)
)

# Position plates on both sides of the beam
# The plate extrudes from 0 to +thk in Y.
# To place on +Y face (at y=beam_width/2), shift by beam_width/2
plate_pos = plate_with_holes.translate((0, beam_width/2, 0))
# To place on -Y face (at y=-beam_width/2), shift by -beam_width/2 - thk
plate_neg = plate_with_holes.translate((0, -beam_width/2 - conn_plate_thk, 0))

# --- 4. Mounting Lugs ---
# Defined on XZ plane, extruded along Y
def create_lug_geo():
    # Calculate geometric points
    rect_h = lug_height - lug_width/2
    pts = [
        (-lug_width/2, 0),
        (lug_width/2, 0),
        (lug_width/2, rect_h),
        (-lug_width/2, rect_h)
    ]
    
    # Draw profile: Rectangle bottom + Arc top
    lug_solid = (
        cq.Workplane("XZ")
        .moveTo(pts[0][0], pts[0][1])
        .lineTo(pts[1][0], pts[1][1])
        .lineTo(pts[2][0], pts[2][1])
        .threePointArc((0, lug_height), pts[3]) # Arc through top center to end
        .close()
        .extrude(lug_thk)
    )
    
    # Cut hole
    lug_solid = (
        lug_solid.faces(">Y").workplane()
        .moveTo(0, rect_h)
        .hole(lug_hole_dia)
    )
    return lug_solid

# Create one lug instance and move to top of beam
base_lug = create_lug_geo().translate((0, 0, beam_height/2))

# Helper to create a pair of lugs
def create_lug_pair(x_pos):
    # Two plates separated by 'lug_pair_gap', centered on Y axis
    l1 = base_lug.translate((x_pos, lug_pair_gap/2, 0))
    l2 = base_lug.translate((x_pos, -lug_pair_gap/2 - lug_thk, 0))
    return l1.union(l2)

# Generate all lug pairs
lug_locations = [
    lug_offset, 
    lug_offset + lug_pair_spacing,
    -lug_offset, 
    -(lug_offset + lug_pair_spacing)
]

lugs_assembly = cq.Workplane()
for x in lug_locations:
    lugs_assembly = lugs_assembly.union(create_lug_pair(x))

# --- 5. Final Assembly ---
result = (
    cross_beam
    .union(cradle)
    .union(plate_pos)
    .union(plate_neg)
    .union(lugs_assembly)
)