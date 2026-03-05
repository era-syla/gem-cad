import cadquery as cq

# Arduino Uno board model
# Main PCB board dimensions approximately 68.6mm x 53.4mm

# Main PCB board
pcb_length = 68.6
pcb_width = 53.4
pcb_thickness = 1.6

result = cq.Workplane("XY").box(pcb_length, pcb_width, pcb_thickness)

# Add USB connector (Type B) on the right side
usb_w = 12
usb_h = 11
usb_d = 16
usb = (cq.Workplane("XY")
       .box(usb_d, usb_w, usb_h)
       .translate((pcb_length/2 + usb_d/2 - 2, 10, pcb_thickness/2 + usb_h/2))
)
result = result.union(usb)

# Add power jack on right side
jack_w = 9
jack_h = 11
jack_d = 13
jack = (cq.Workplane("XY")
        .box(jack_d, jack_w, jack_h)
        .translate((pcb_length/2 + jack_d/2 - 2, -15, pcb_thickness/2 + jack_h/2))
)
result = result.union(jack)

# Add cylindrical part of power jack
jack_cyl = (cq.Workplane("YZ")
            .circle(4)
            .extrude(8)
            .translate((pcb_length/2 + jack_d - 2, -15, pcb_thickness/2 + jack_h/2))
)
result = result.union(jack_cyl)

# Digital pin headers (top row) - 14 pins
pin_header_length = 54
pin_header_width = 2.5
pin_header_height = 8.5
digital_header = (cq.Workplane("XY")
                  .box(pin_header_length, pin_header_width, pin_header_height)
                  .translate((-2, pcb_width/2 + pin_header_width/2, pcb_thickness/2 + pin_header_height/2))
)
result = result.union(digital_header)

# Analog pin headers (bottom row) - 6 pins
analog_header_length = 22
analog_header = (cq.Workplane("XY")
                 .box(analog_header_length, pin_header_width, pin_header_height)
                 .translate((-18, -pcb_width/2 - pin_header_width/2, pcb_thickness/2 + pin_header_height/2))
)
result = result.union(analog_header)

# Power pin headers
power_header_length = 14
power_header = (cq.Workplane("XY")
                .box(power_header_length, pin_header_width, pin_header_height)
                .translate((18, -pcb_width/2 - pin_header_width/2, pcb_thickness/2 + pin_header_height/2))
)
result = result.union(power_header)

# Add screw terminal blocks on top-left area
terminal_w = 30
terminal_h = 8
terminal_d = 8
terminal1 = (cq.Workplane("XY")
             .box(terminal_w, terminal_d, terminal_h)
             .translate((-15, 20, pcb_thickness/2 + terminal_h/2))
)
result = result.union(terminal1)

terminal2 = (cq.Workplane("XY")
             .box(terminal_w, terminal_d, terminal_h)
             .translate((-15, 10, pcb_thickness/2 + terminal_h/2))
)
result = result.union(terminal2)

# Add main microcontroller chip (ATmega328)
chip_l = 18
chip_w = 7
chip_h = 3
chip = (cq.Workplane("XY")
        .box(chip_l, chip_w, chip_h)
        .translate((5, 5, pcb_thickness/2 + chip_h/2))
)
result = result.union(chip)

# Add crystal oscillator
xtal_l = 5
xtal_w = 2
xtal_h = 3
xtal = (cq.Workplane("XY")
        .box(xtal_l, xtal_w, xtal_h)
        .translate((15, 5, pcb_thickness/2 + xtal_h/2))
)
result = result.union(xtal)

# Add small IC chip (ATmega16U2)
ic2_l = 7
ic2_w = 7
ic2_h = 2
ic2 = (cq.Workplane("XY")
       .box(ic2_l, ic2_w, ic2_h)
       .translate((25, -15, pcb_thickness/2 + ic2_h/2))
)
result = result.union(ic2)

# Mounting holes - 4 corners
hole_r = 1.6
for hx, hy in [(-pcb_length/2 + 5, -pcb_width/2 + 5),
               (-pcb_length/2 + 5, pcb_width/2 - 5),
               (pcb_length/2 - 5, pcb_width/2 - 5),
               (pcb_length/2 - 14, -pcb_width/2 + 5)]:
    hole = (cq.Workplane("XY")
            .circle(hole_r)
            .extrude(pcb_thickness + 2)
            .translate((hx, hy, -pcb_thickness/2 - 1))
    )
    result = result.cut(hole)