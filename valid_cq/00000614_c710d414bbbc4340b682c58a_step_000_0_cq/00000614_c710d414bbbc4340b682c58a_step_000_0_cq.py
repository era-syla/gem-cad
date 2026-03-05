import cadquery as cq

def create_arduino_uno():
    # --- Parameters ---
    # PCB Dimensions (Standard Arduino Uno R3 dimensions)
    pcb_length = 68.6
    pcb_width = 53.4
    pcb_thickness = 1.6
    
    # Corner Fillets and Cutouts
    corner_fillet = 2.5
    cutout_offset_x = 0  # relative to the irregular shape logic
    
    # Mounting Holes (Standard spacing)
    # Positions relative to bottom-left corner (USB side, Power jack side)
    # Hole 1: Near USB
    h1_x, h1_y = 14.0, 2.5
    # Hole 2: Near Power Jack
    h2_x, h2_y = 66.0, 7.6
    # Hole 3: Bottom right
    h3_x, h3_y = 66.0, 35.6
    # Hole 4: Bottom left
    h4_x, h4_y = 15.2, 50.8
    hole_dia = 3.2

    # USB Connector (Type B)
    usb_l, usb_w, usb_h = 16.0, 12.0, 11.0
    usb_x, usb_y = -6.0, 36.0 # Approx relative to center
    
    # Power Jack (Barrel Jack)
    jack_l, jack_w, jack_h = 14.0, 9.0, 11.0
    jack_x, jack_y = 23.0, 38.0 
    
    # Headers (Generic blocks for visual representation)
    header_w = 2.54
    header_h = 8.5
    
    # Digital High (8-pin + 10-pin block approximation)
    dig_high_l = 45.0
    dig_high_x, dig_high_y = 15.0, 24.0
    
    # Digital Low / Analog (6-pin + 8-pin + 8-pin + 6-pin approx)
    # Let's split them into two main banks for the bottom
    # Bank 1 (Power + Analog)
    bank1_l = 35.0
    bank1_x, bank1_y = -8.0, -24.0
    
    # Bank 2 (Digital 0-7)
    bank2_l = 22.0
    bank2_x, bank2_y = 24.0, -24.0
    
    # IC (ATmega328P DIP package)
    ic_l, ic_w, ic_h = 35.0, 8.0, 4.0
    ic_x, ic_y = 10.0, -5.0
    
    # ISP Header (2x3 pins)
    isp_l, isp_w, isp_h = 5.08, 7.62, 6.0
    isp_x, isp_y = 30.0, 0.0

    # --- Geometry Construction ---

    # 1. PCB Base
    # The Arduino Uno shape is irregular. It's essentially a rectangle with a notch near the USB.
    # Let's start with a base rectangle centered.
    pcb = cq.Workplane("XY").box(pcb_length, pcb_width, pcb_thickness)
    
    # Create the characteristic notch/shape adjustments
    # The USB overhangs, and there's a cutout near the mounting hole.
    # We will refine the shape by defining the outline points for a simpler approximation
    # or just keep it rectangular with fillets for simplicity, but let's try to match the profile.
    
    # Let's redefine PCB as a sketch extrusion to get the shape right
    # Coordinate system: Origin at center of the bounding box roughly
    
    # Drawing the outline path
    # Starting from bottom-left, going counter-clockwise
    pts = [
        (-pcb_length/2, -pcb_width/2), # Bottom Left
        (pcb_length/2, -pcb_width/2),  # Bottom Right
        (pcb_length/2, pcb_width/2 - 5),   # Top Right (start of notch)
        (pcb_length/2 - 2, pcb_width/2), # Notch diagonal
        (-pcb_length/2 + 10, pcb_width/2), # Top edge
        (-pcb_length/2, pcb_width/2 - 10), # Cut corner near USB
    ]
    
    pcb = (cq.Workplane("XY")
           .polyline(pts)
           .close()
           .extrude(pcb_thickness)
           .edges("|Z").fillet(1.0) # Smooth corners slightly
          )

    # 2. Mounting Holes
    # We need to translate the hole coordinates from "bottom-left relative" to "center relative"
    # Center approx at (pcb_length/2, pcb_width/2) relative to bottom-left
    ox, oy = -pcb_length/2, -pcb_width/2
    
    holes = (cq.Workplane("XY")
             .pushPoints([
                 (ox + h1_x, oy + h1_y),
                 (ox + h2_x, oy + h2_y),
                 (ox + h3_x, oy + h3_y),
                 (ox + h4_x, oy + h4_y)
             ])
             .circle(hole_dia/2)
             .extrude(pcb_thickness + 2) # cut through
            )
    
    pcb = pcb.cut(holes)

    # 3. Components
    
    # USB Connector (Silver box)
    usb = (cq.Workplane("XY")
           .workplane(offset=pcb_thickness/2)
           .center(ox + 9.0, oy + 40.0) # Position adjustment
           .box(usb_l, usb_w, usb_h, centered=(True, True, False))
           .edges("|Z").fillet(1.0)
          )
    
    # Power Jack (Black box)
    jack = (cq.Workplane("XY")
            .workplane(offset=pcb_thickness/2)
            .center(ox + 60.0, oy + 45.0) # Position adjustment
            .box(jack_l, jack_w, jack_h, centered=(True, True, False))
           )

    # Female Headers (Top row - Digital)
    # We create a long block and cut holes to simulate sockets
    header_top = (cq.Workplane("XY")
                  .workplane(offset=pcb_thickness/2)
                  .center(ox + 45.0, oy + 50.0)
                  .box(45, header_w, header_h, centered=(True, True, False))
                 )
    
    # Cut square holes in header
    hx_pts = [(i*2.54 - 45/2 + 2, 0) for i in range(16)]
    header_cuts = (cq.Workplane("XY")
                   .workplane(offset=pcb_thickness/2 + header_h)
                   .center(ox + 45.0, oy + 50.0)
                   .pushPoints(hx_pts)
                   .rect(1.5, 1.5)
                   .extrude(-2.0)
                  )
    header_top = header_top.cut(header_cuts)

    # Female Headers (Bottom row - Power + Analog)
    header_bot1 = (cq.Workplane("XY")
                   .workplane(offset=pcb_thickness/2)
                   .center(ox + 35.0, oy + 2.5)
                   .box(40, header_w, header_h, centered=(True, True, False))
                  )
    
    # Female Headers (Bottom row - Digital low)
    header_bot2 = (cq.Workplane("XY")
                   .workplane(offset=pcb_thickness/2)
                   .center(ox + 62.0, oy + 2.5)
                   .box(20, header_w, header_h, centered=(True, True, False))
                  )
    
    # Main IC (DIP Package)
    ic_body = (cq.Workplane("XY")
               .workplane(offset=pcb_thickness/2)
               .center(ox + 45.0, oy + 18.0)
               .box(ic_l, ic_w, ic_h, centered=(True, True, False))
              )
    
    # IC Socket underneath (slightly larger/flatter)
    ic_socket = (cq.Workplane("XY")
               .workplane(offset=pcb_thickness/2)
               .center(ox + 45.0, oy + 18.0)
               .box(ic_l + 2, ic_w + 2, 1.5, centered=(True, True, False))
              )

    # ISP Header (2x3 pins)
    isp_pins = (cq.Workplane("XY")
                .workplane(offset=pcb_thickness/2)
                .center(ox + 65.0, oy + 25.0)
                .rect(isp_l, isp_w)
                .extrude(6.0)
               )

    # Crystal Oscillator (Oval shape)
    crystal = (cq.Workplane("XY")
               .workplane(offset=pcb_thickness/2)
               .center(ox + 25.0, oy + 30.0)
               .box(10, 4, 3, centered=(True, True, False))
               .edges("|Z").fillet(1.9)
              )
    
    # Reset Button (Small cylinder + box)
    reset_base = (cq.Workplane("XY")
                  .workplane(offset=pcb_thickness/2)
                  .center(ox + 6.0, oy + 48.0)
                  .box(6, 6, 3, centered=(True, True, False))
                 )
    reset_btn = (cq.Workplane("XY")
                  .workplane(offset=pcb_thickness/2 + 3)
                  .center(ox + 6.0, oy + 48.0)
                  .circle(1.5)
                  .extrude(1.0)
                 )

    # Combine everything
    result = pcb.union(usb).union(jack).union(header_top).union(header_bot1).union(header_bot2)
    result = result.union(ic_socket).union(ic_body).union(isp_pins).union(crystal)
    result = result.union(reset_base).union(reset_btn)
    
    # Rotate to match the isometric-like view in the prompt approximately for better viewing
    result = result.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -45)

    return result

result = create_arduino_uno()