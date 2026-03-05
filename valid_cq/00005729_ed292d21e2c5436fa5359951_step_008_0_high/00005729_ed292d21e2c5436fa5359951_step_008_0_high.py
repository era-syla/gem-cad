import cadquery as cq

# --- Parameters ---
pcb_width = 76.0
pcb_height = 70.0
pcb_thick = 1.6

# --- PCB Board ---
# Create the main board plate
pcb = cq.Workplane("XY").box(pcb_width, pcb_height, pcb_thick)

# Add cutout notch on the bottom edge (offset slightly to the right)
notch_width = 15.0
notch_height = 8.0
notch_x_pos = 12.0
notch_cutout = (
    cq.Workplane("XY")
    .center(notch_x_pos, -pcb_height / 2)
    .box(notch_width, notch_height, pcb_thick * 2)
)
pcb = pcb.cut(notch_cutout)

# Add Mounting Holes at corners
hole_inset_x = 4.0
hole_inset_y = 4.0
hx = pcb_width / 2 - hole_inset_x
hy = pcb_height / 2 - hole_inset_y
hole_locations = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]

pcb = pcb.faces(">Z").workplane().pushPoints(hole_locations).hole(3.2)


# --- Component: BNC Connector (Top Left) ---
# Location parameters
bnc_x = -pcb_width / 2 + 16
bnc_y = pcb_height / 2 - 18
bnc_z = pcb_thick / 2

# Main metal body block
bnc_body = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(bnc_x, bnc_y)
    .box(16, 16, 16, centered=(True, True, False))
)

# Cylindrical Barrel (pointing to the left / -X direction)
bnc_barrel = (
    cq.Workplane("YZ")
    .workplane(offset=bnc_x - 8)  # Left face of body
    .center(bnc_y, bnc_z + 8)     # Center relative to body height
    .circle(5.5)
    .extrude(-18)                 # Extrude outwards to the left
)

# Flange/Detail on barrel
bnc_flange = (
    cq.Workplane("YZ")
    .workplane(offset=bnc_x - 8 - 14)
    .center(bnc_y, bnc_z + 8)
    .circle(6.5)
    .extrude(-2)
)

# Screw on top of the connector body
bnc_screw = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z + 16)
    .center(bnc_x + 3, bnc_y)
    .circle(2.0)
    .extrude(2.5)
)
bnc_screw_head = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z + 16 + 2.5)
    .center(bnc_x + 3, bnc_y)
    .circle(3.5)
    .extrude(1.5)
)

bnc_assy = bnc_body.union(bnc_barrel).union(bnc_flange).union(bnc_screw).union(bnc_screw_head)


# --- Component: Tactile Switch (Near BNC) ---
sw_x = bnc_x + 16
sw_y = bnc_y + 4
sw_base = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(sw_x, sw_y)
    .box(6.5, 6.5, 4.0, centered=(True, True, False))
)
sw_btn = (
    sw_base.faces(">Z")
    .workplane()
    .circle(1.8)
    .extrude(1.5)
)
switch = sw_base.union(sw_btn)


# --- Component: Small Interface Port (Left Edge) ---
port_x = -pcb_width / 2 + 10
port_y = -5
port_housing = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(port_x, port_y)
    .box(8, 11, 7, centered=(True, True, False))
)
# Create cavity for the port
port_cavity = (
    cq.Workplane("YZ")
    .workplane(offset=port_x - 4)
    .center(port_y, bnc_z + 3.5)
    .rect(6, 3)
    .extrude(6)
)
small_port = port_housing.cut(port_cavity)


# --- Component: Large Shrouded Header (Right Side) ---
hdr_x = pcb_width / 2 - 14
hdr_y = 12
hdr_w = 10.0
hdr_l = 28.0
hdr_h = 13.0

# Plastic Shroud
shroud = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(hdr_x, hdr_y)
    .box(hdr_w, hdr_l, hdr_h, centered=(True, True, False))
)
# Hollow out the shroud
shroud_cavity = (
    shroud.faces(">Z")
    .workplane()
    .rect(hdr_w - 2.5, hdr_l - 2.5)
    .cutBlind(-(hdr_h - 2))
)
# Cut side slot (polarization notch)
side_slot = (
    cq.Workplane("YZ")
    .workplane(offset=hdr_x)
    .center(hdr_y, bnc_z + hdr_h / 2)
    .rect(6, 4)
    .extrude(hdr_w / 2 + 1)
)
shroud_final = shroud_cavity.cut(side_slot)

# Add Pins array
pin_pts = []
for col in [-1.27, 1.27]:
    for row_idx in range(5): # 10 pin header (2x5)
        y_pos = (row_idx - 2) * 2.54
        pin_pts.append((col, y_pos))

pins = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(hdr_x, hdr_y)
    .pushPoints(pin_pts)
    .circle(0.32)
    .extrude(hdr_h - 3)
)

large_header = shroud_final.union(pins)


# --- Component: Right-Angle Pin Header (Bottom Right) ---
ra_x = pcb_width / 2 - 14
ra_y = -22
# Plastic Base
ra_base = (
    cq.Workplane("XY")
    .workplane(offset=bnc_z)
    .center(ra_x, ra_y)
    .box(5, 18, 2.5, centered=(True, True, False))
)

# Construct Right Angle Pins (L-shape)
ra_pins_comp = ra_base
for i in range(4): # 2x4 header
    y_pos = ra_y + (i - 1.5) * 2.54
    for x_offset in [-1.27, 1.27]:
        x_pos = ra_x + x_offset
        # Vertical segment
        p_vert = (
            cq.Workplane("XY")
            .workplane(offset=bnc_z)
            .center(x_pos, y_pos)
            .circle(0.32)
            .extrude(6.0)
        )
        # Horizontal segment (sticking out to the right)
        p_horz = (
            cq.Workplane("YZ")
            .workplane(offset=x_pos)
            .center(y_pos, bnc_z + 6.0 - 0.32)
            .circle(0.32)
            .extrude(6.0)
        )
        ra_pins_comp = ra_pins_comp.union(p_vert).union(p_horz)


# --- Final Assembly ---
result = (
    pcb
    .union(bnc_assy)
    .union(switch)
    .union(small_port)
    .union(large_header)
    .union(ra_pins_comp)
)