import cadquery as cq

# --- Parameters ---
# PCB Dimensions (approximate Arduino Uno dims)
pcb_width = 53.3
pcb_length = 68.6
pcb_thickness = 1.6
corner_fillet = 2.0

# Mounting Holes
hole_dia = 3.2
hole_offset = 2.5 # from edge

# USB Connector (Type B)
usb_width = 12.0
usb_height = 11.0
usb_depth = 16.0
usb_protrusion = 2.0 # Sticks out past PCB edge

# Power Jack
power_width = 9.0
power_height = 11.0
power_depth = 14.0
power_protrusion = 2.0

# Headers (Female)
header_width = 2.54
header_height = 8.5
header_pitch = 2.54

# IC (DIP Package)
ic_width = 7.6
ic_length = 35.0
ic_height = 3.5

# ISP Header (2x3 pins)
isp_pin_height = 6.0
isp_pin_width = 0.64
isp_pitch = 2.54

# Crystal
crystal_length = 11.5
crystal_width = 4.5
crystal_height = 3.5

# --- Helper Functions ---

def create_female_header(pins, spacing=2.54):
    """Creates a block representing a female pin header."""
    h_len = pins * spacing
    h_wid = 2.54
    h_hgt = 8.5
    
    header = cq.Workplane("XY").box(h_len, h_wid, h_hgt, centered=(True, True, False))
    return header

def create_dip_ic(length, width, height, pins_per_side):
    """Creates a DIP IC package."""
    # Main body
    body = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
    
    # Legs (simplified as blocks along the side)
    leg_block_w = 1.0
    leg_block_h = 2.0 # below body
    legs_l = cq.Workplane("XY").box(length - 2, leg_block_w, leg_block_h, centered=(True, True, False)) \
             .translate((0, -width/2 - leg_block_w/2, 0))
    legs_r = cq.Workplane("XY").box(length - 2, leg_block_w, leg_block_h, centered=(True, True, False)) \
             .translate((0, width/2 + leg_block_w/2, 0))
    
    full_ic = body.translate((0,0, leg_block_h)).union(legs_l).union(legs_r)
    return full_ic

def create_isp_header():
    """Creates a 2x3 pin header block."""
    base = cq.Workplane("XY").box(2.54*3, 2.54*2, 2.5, centered=(True, True, False))
    pins = []
    for x in [-2.54, 0, 2.54]:
        for y in [-1.27, 1.27]:
            p = cq.Workplane("XY").box(0.64, 0.64, 6.0 + 2.5, centered=(True, True, False)) \
                .translate((x, y, 0))
            if not pins:
                pins = p
            else:
                pins = pins.union(p)
    return base.union(pins)

# --- Build Process ---

# 1. PCB Base
# The shape is roughly rectangular with a notch near the USB/Power jack
# We'll start with a rectangle and cut holes.
pcb = cq.Workplane("XY").box(pcb_length, pcb_width, pcb_thickness, centered=(True, True, False))

# Cutouts and Notch (Uno specific shape)
# Creating a custom polygon for exact shape would be ideal, but modifying a box is simpler for approximation.
# Notch near USB
pcb = pcb.cut(cq.Workplane("XY")
              .rect(10, 15)
              .translate((-pcb_length/2 + 5, pcb_width/2 - 7.5, 0))
              .extrude(pcb_thickness))

# Round corners
pcb = pcb.edges("|Z").fillet(corner_fillet)

# Mounting Holes
holes = [
    (-pcb_length/2 + 14, -pcb_width/2 + 2.5),
    (-pcb_length/2 + 15.2, pcb_width/2 - 2.5 - 10), # Near USB
    (pcb_length/2 - 14, pcb_width/2 - 2.5),
    (pcb_length/2 - 2.5, -pcb_width/2 + 15.2)
]

for x, y in holes:
    pcb = pcb.cut(cq.Workplane("XY").circle(hole_dia/2).extrude(pcb_thickness).translate((x, y, 0)))


# 2. Components

# USB Connector (Type B) - Top left
usb_box = cq.Workplane("XY").box(usb_depth, usb_width, usb_height, centered=(True, True, False))
# Add inner detail
usb_hole = cq.Workplane("XY").rect(usb_depth, usb_width - 4).extrude(usb_height - 4).translate((2, 0, 2))
usb_conn = usb_box.cut(usb_hole)
usb_pos = (-pcb_length/2 + usb_depth/2 - usb_protrusion, pcb_width/2 - usb_width/2 - 5, pcb_thickness)
usb_conn = usb_conn.translate(usb_pos)

# Power Jack - Top Right
# Main body
pwr_body = cq.Workplane("XY").box(power_depth, power_width, power_height, centered=(True, True, False))
# Cylindrical socket part
pwr_cyl = cq.Workplane("YZ").circle(power_width/2).extrude(power_depth).translate((0, 0, power_height/2))
pwr_cyl = pwr_cyl.rotate((0,0,1), (0,0,0), -90).translate((power_depth/2, 0, 0))
# Combine
power_jack = pwr_body.union(pwr_cyl)
# Add hole
jack_hole = cq.Workplane("YZ").circle(3.0).extrude(5).translate((0,0,power_height/2))
jack_hole = jack_hole.rotate((0,0,1), (0,0,0), -90).translate((-power_depth/2, 0, 0))
power_jack = power_jack.cut(jack_hole)

pwr_pos = (-pcb_length/2 + power_depth/2 - power_protrusion, -pcb_width/2 + power_width/2 + 2, pcb_thickness)
power_jack = power_jack.translate(pwr_pos)


# Headers (Digital/Analog)
# Top Row (Digital)
header_digital_1 = create_female_header(8).translate((pcb_length/2 - (8*2.54)/2 - 2, pcb_width/2 - 2.54, pcb_thickness))
header_digital_2 = create_female_header(10).translate((-5, pcb_width/2 - 2.54, pcb_thickness)) # approximate pos

# Bottom Row (Power + Analog)
header_power = create_female_header(8).translate((-10, -pcb_width/2 + 2.54, pcb_thickness))
header_analog = create_female_header(6).translate((pcb_length/2 - (6*2.54)/2 - 2, -pcb_width/2 + 2.54, pcb_thickness))


# Main IC (ATmega328P DIP)
ic_x = 10
ic_y = -5
ic_dip = create_dip_ic(ic_length, ic_width, ic_height, 14).translate((ic_x, ic_y, pcb_thickness))

# ISP Header (ICSP) - Near the end of the board
isp_header = create_isp_header().translate((pcb_length/2 - 5, 0, pcb_thickness))

# Reset Button (Small tactile switch)
reset_btn = cq.Workplane("XY").box(6, 6, 3, centered=(True, True, False))
btn_cylinder = cq.Workplane("XY").circle(1.5).extrude(3.5).translate((0,0,0))
reset_switch = reset_btn.union(btn_cylinder).translate((-pcb_length/2 + 7, pcb_width/2 - 7, pcb_thickness))

# Crystal Oscillator
crystal_body = cq.Workplane("XY").box(crystal_length, crystal_width, crystal_height, centered=(True, True, False))
# Rounded ends
cyl1 = cq.Workplane("XY").circle(crystal_width/2).extrude(crystal_height).translate((-crystal_length/2, 0, 0))
cyl2 = cq.Workplane("XY").circle(crystal_width/2).extrude(crystal_height).translate((crystal_length/2, 0, 0))
crystal = crystal_body.union(cyl1).union(cyl2).translate((-8, -15, pcb_thickness)) # Approx location

# Voltage Regulator (SOT-223 approx)
regulator = cq.Workplane("XY").box(6.5, 3.5, 1.6, centered=(True, True, False))
reg_tab = cq.Workplane("XY").box(3.0, 3.0, 1.6, centered=(True, True, False)).translate((0, 3.25, 0))
vreg = regulator.union(reg_tab).translate((-20, -12, pcb_thickness))

# Small ISP near USB (ATmega16U2 header)
isp_usb = create_isp_header().rotate((0,0,1), (0,0,0), 90).translate((-pcb_length/2 + 15, pcb_width/2 - 20, pcb_thickness))


# --- Assembly ---

result = pcb \
    .union(usb_conn) \
    .union(power_jack) \
    .union(header_digital_1) \
    .union(header_digital_2) \
    .union(header_power) \
    .union(header_analog) \
    .union(ic_dip) \
    .union(isp_header) \
    .union(reset_switch) \
    .union(crystal) \
    .union(vreg) \
    .union(isp_usb)