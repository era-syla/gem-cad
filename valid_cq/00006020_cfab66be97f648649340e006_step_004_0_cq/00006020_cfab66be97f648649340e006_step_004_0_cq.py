import cadquery as cq

# --- Parameter Definitions ---

# Base Plate
plate_width = 80.0
plate_height = 80.0
plate_thickness = 3.0
corner_hole_dist = 5.0
mounting_hole_diam = 4.0

# Top Right Connector (Header)
tr_header_base_width = 8.0
tr_header_base_length = 20.0
tr_header_base_height = 5.0
tr_header_pos_x = plate_width/2 - 12.0
tr_header_pos_y = plate_height/2 - 15.0
pin_size = 1.0
pin_length = 10.0
tr_pin_rows = 2
tr_pin_cols = 5
tr_pin_pitch = 2.54

# Left Connector (Header)
l_header_base_width = 8.0
l_header_base_length = 25.0
l_header_base_height = 5.0
l_header_pos_x = -plate_width/2 + 12.0
l_header_pos_y = 5.0
l_pin_rows = 2
l_pin_cols = 7
l_pin_pitch = 2.54

# Terminal Blocks (Right side)
term_block_size = 10.0
term_block_height = 10.0
term_block_count = 3
term_block_pitch = 10.0
term_block_pos_x = plate_width/2 - 12.0
term_block_start_y = 10.0 # Relative to center

# Central IC Chip
ic_size = 16.0
ic_height = 3.0
ic_pos_x = 0.0
ic_pos_y = 10.0

# Angled Components (bottom corners)
angled_comp_length = 20.0
angled_comp_width = 8.0
angled_comp_height = 6.0
angled_angle = 45.0

# Large Bottom Component (Tongue)
btm_comp_width = 30.0
btm_comp_length = 40.0
btm_comp_thickness = 4.0
btm_comp_pos_y = -20.0
btm_sub_tab_width = 10.0
btm_sub_tab_len = 5.0
btm_sub_tab_thick = 3.0

# --- Geometry Construction ---

# 1. Base Plate
plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
)

# 2. Mounting Holes
# We select the top face, then locate points near corners
holes = (
    plate.faces(">Z").workplane()
    .rect(plate_width - 2*corner_hole_dist, plate_height - 2*corner_hole_dist, forConstruction=True)
    .vertices()
    .hole(mounting_hole_diam)
)
result = holes

# 3. Top Right Header
# Base
tr_base = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(tr_header_pos_x, tr_header_pos_y)
    .box(tr_header_base_width, tr_header_base_length, tr_header_base_height, centered=(True, True, False))
)
result = result.union(tr_base)

# Pins
tr_pins = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2 + tr_header_base_height)
    .center(tr_header_pos_x, tr_header_pos_y)
    # Create grid of points
    .rarray(tr_pin_pitch, tr_pin_pitch, tr_pin_rows, tr_pin_cols)
    .rect(pin_size, pin_size)
    .extrude(pin_length)
)
result = result.union(tr_pins)


# 4. Left Header
# Base
l_base = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(l_header_pos_x, l_header_pos_y)
    .box(l_header_base_width, l_header_base_length, l_header_base_height, centered=(True, True, False))
)
result = result.union(l_base)

# Pins
l_pins = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2 + l_header_base_height)
    .center(l_header_pos_x, l_header_pos_y)
    .rarray(l_pin_pitch, l_pin_pitch, l_pin_rows, l_pin_cols)
    .rect(pin_size, pin_size)
    .extrude(pin_length)
)
result = result.union(l_pins)


# 5. Terminal Blocks (Right side, below TR header)
# Create a single block then iterate
for i in range(term_block_count):
    y_pos = term_block_start_y - (i * term_block_pitch)
    
    term = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness/2)
        .center(term_block_pos_x, y_pos)
        .box(term_block_size, term_block_size, term_block_height, centered=(True, True, False))
    )
    
    # Add screw detail
    screw = (
        term.faces(">Z").workplane()
        .circle(3.0)
        .cutBlind(-1.0) # Recess
        .faces("<Z[1]").workplane() # Select bottom of recess
        .rect(0.8, 4.0).extrude(0.5) # Cross
        .rect(4.0, 0.8).extrude(0.5)
    )
    # Add wire hole detail on side
    wire_hole = (
        term.faces(">X").workplane()
        .center(0, -term_block_height/4)
        .circle(2.0)
        .cutBlind(-5.0)
    )
    
    result = result.union(wire_hole)

# 6. Central IC Chip
ic = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(ic_pos_x, ic_pos_y)
    .box(ic_size, ic_size, ic_height, centered=(True, True, False))
)
result = result.union(ic)


# 7. Angled Components
# Right angled component
right_angled = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(15, -15)
    .transformed(rotate=(0, 0, -45))
    .box(angled_comp_length, angled_comp_width, angled_comp_height, centered=(True, True, False))
)
result = result.union(right_angled)

# Left angled component
left_angled = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(-15, -25)
    .transformed(rotate=(0, 0, 30)) # Slight different angle based on image visual
    .box(angled_comp_length, angled_comp_width, angled_comp_height, centered=(True, True, False))
)
result = result.union(left_angled)


# 8. Large Bottom Extension (Tongue)
# Main tongue
tongue = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(0, btm_comp_pos_y)
    .box(btm_comp_width, btm_comp_length, btm_comp_thickness, centered=(True, False, False)) # Extrude +Z
    .rotate((0,0,0), (1,0,0), -90) # Rotate to stick out perpendicular to plate
    .translate((0, -25, btm_comp_length/2 + plate_thickness/2)) # Adjust position to stick OUT
)

# Re-approaching Tongue construction to make it easier relative to the plate face
# Create a plane on the face of the plate
tongue_geo = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(0, -25) # Position near bottom center
    .box(btm_comp_width, btm_comp_length, btm_comp_thickness, centered=(True, False, False))
)
# Rotate it so it sticks out normally
tongue_geo = tongue_geo.rotate((0,-25,0), (1,0,0), -90).translate((0, -btm_comp_thickness, 0))

# Small tab under the tongue
tab = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .center(0, -25 - btm_comp_thickness) # align with bottom of tongue
    .box(btm_sub_tab_width, btm_sub_tab_len, btm_sub_tab_thick, centered=(True, False, False))
     .rotate((0,-25-btm_comp_thickness,0), (1,0,0), -90)
     .translate((0, -btm_sub_tab_thick, btm_comp_length - btm_sub_tab_len)) # Move to tip
)

result = result.union(tongue_geo).union(tab)