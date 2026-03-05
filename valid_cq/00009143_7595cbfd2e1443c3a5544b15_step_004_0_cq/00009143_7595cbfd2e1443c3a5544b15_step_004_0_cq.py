import cadquery as cq

# --- Parametric Dimensions ---

# Base Plate
plate_width = 40.0
plate_height = 30.0
plate_thickness = 2.0
mount_hole_dia = 3.5
mount_hole_pos = (-15, 10) # Relative to center

# Right Connector (Molex style)
conn_right_width = 12.0
conn_right_height = 18.0
conn_right_depth = 12.0
conn_right_wall = 1.2
conn_right_offset_x = 10.0 # From center
conn_right_offset_y = 5.0  # From center
pin_size = 0.8
pin_length = 8.0
pin_pitch = 4.0

# Left Connector (Terminal Block style)
conn_left_width = 10.0  # Actually depth in this orientation
conn_left_height = 12.0
conn_left_depth = 15.0 # Along the plate
conn_left_wall = 1.0
conn_left_offset_x = -10.0
conn_left_offset_y = -8.0 

# --- Modeling Steps ---

# 1. Base Plate
# Create the main rectangular board
base_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .moveTo(mount_hole_pos[0], mount_hole_pos[1])
    .hole(mount_hole_dia)
)

# 2. Right Connector (Header)
# Create the shroud
shroud_outer = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .moveTo(conn_right_offset_x, conn_right_offset_y)
    .rect(conn_right_width, conn_right_height)
    .extrude(conn_right_depth)
)

shroud_cutout = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .moveTo(conn_right_offset_x, conn_right_offset_y)
    .rect(conn_right_width - 2*conn_right_wall, conn_right_height - 2*conn_right_wall)
    .extrude(conn_right_depth)
)

# Create the polarization/lock slots on top and bottom of shroud
slot_width = 2.5
slot_depth = conn_right_depth
slot_height = 2.0 # How much it cuts into the wall

top_slot = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2 + conn_right_depth - slot_depth/2)
    .moveTo(conn_right_offset_x, conn_right_offset_y + conn_right_height/2)
    .box(slot_width, slot_height*2, slot_depth)
)

bottom_slot = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2 + conn_right_depth - slot_depth/2)
    .moveTo(conn_right_offset_x, conn_right_offset_y - conn_right_height/2)
    .box(slot_width, slot_height*2, slot_depth)
)

# Create the pins inside
pins = cq.Workplane("XY").workplane(offset=plate_thickness/2)
for i in range(3):
    y_pos = conn_right_offset_y + (i - 1) * pin_pitch
    pins = (
        pins.moveTo(conn_right_offset_x, y_pos)
        .rect(pin_size, pin_size)
        .extrude(pin_length)
    )

# Combine Right Connector parts
right_connector = shroud_outer.cut(shroud_cutout).cut(top_slot).cut(bottom_slot).union(pins)

# Add side notches on the back of the right connector (visual detail from image)
notch_h = 2.0
notch_w = 1.0
notches = cq.Workplane("XY").workplane(offset=plate_thickness/2)
for i in range(3):
    y_pos = conn_right_offset_y + (i - 1) * pin_pitch
    notch = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness/2)
        .moveTo(conn_right_offset_x - conn_right_width/2, y_pos)
        .rect(notch_w*2, notch_h)
        .extrude(conn_right_depth) # Cut through whole length to simplify, or adjust depth
    )
    right_connector = right_connector.cut(notch)


# 3. Left Connector (Terminal Block)
# This has a complex shape: a block with wire entries and screw holes, plus an angled back.

# Main block body
tb_body = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2)
    .moveTo(conn_left_offset_x, conn_left_offset_y)
    .rect(conn_left_depth, conn_left_height)
    .extrude(conn_left_width)
)

# Angled back section (chamfer-like subtraction)
# We will cut a wedge off the top-right corner (relative to the block's local coords)
wedge_cut = (
    cq.Workplane("YZ")
    .workplane(offset=conn_left_offset_x + conn_left_depth/2)
    .moveTo(conn_left_offset_y + conn_left_height/2, plate_thickness/2 + conn_left_width)
    .lineTo(conn_left_offset_y - conn_left_height/4, plate_thickness/2 + conn_left_width)
    .lineTo(conn_left_offset_y + conn_left_height/2, plate_thickness/2)
    .close()
    .extrude(-conn_left_depth * 0.6) # Extrude into the object
)
tb_body = tb_body.cut(wedge_cut)


# Wire entry holes (rectangular with chamfer, simplified to rect for now)
entry_w = 4.0
entry_h = 3.0
wire_entries = cq.Workplane("YZ").workplane(offset=conn_left_offset_x - conn_left_depth/2)

for i in range(2):
    z_pos = plate_thickness/2 + (i + 0.5) * (conn_left_width/2.2) 
    wire_entries = (
        wire_entries.moveTo(conn_left_offset_y, z_pos)
        .rect(entry_h, entry_w)
        .extrude(conn_left_depth * 0.8)
    )
    
# Screw access holes (circular, on the face parallel to the plate normal but on the side)
# The image shows holes on the 'side' face of the block (YZ plane normal)
screw_holes = cq.Workplane("XZ").workplane(offset= -conn_left_offset_y - conn_left_height/2)
for i in range(2):
    z_pos = plate_thickness/2 + (i + 0.5) * (conn_left_width/2.2) 
    screw_holes = (
        screw_holes.moveTo(conn_left_offset_x + conn_left_depth*0.3, z_pos)
        .circle(1.2)
        .extrude(conn_left_height)
    )

left_connector = tb_body.cut(wire_entries).cut(screw_holes)

# --- Final Assembly ---

result = base_plate.union(right_connector).union(left_connector)