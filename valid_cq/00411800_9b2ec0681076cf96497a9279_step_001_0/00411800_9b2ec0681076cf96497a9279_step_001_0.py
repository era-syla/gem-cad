import cadquery as cq

# --- Parameters ---
pcb_width = 85.0
pcb_depth = 56.0
pcb_thick = 1.6
hole_offset = 3.5
hole_dia = 2.7

# --- Base PCB ---
# Create the main board centered on the XY plane
pcb = cq.Workplane("XY").box(pcb_width, pcb_depth, pcb_thick)

# Add mounting holes
pts = [
    (pcb_width/2 - hole_offset, pcb_depth/2 - hole_offset),
    (pcb_width/2 - hole_offset, -pcb_depth/2 + hole_offset),
    (-pcb_width/2 + hole_offset, pcb_depth/2 - hole_offset),
    (-pcb_width/2 + hole_offset, -pcb_depth/2 + hole_offset)
]
pcb = pcb.faces(">Z").workplane().pushPoints(pts).hole(hole_dia)

# --- Surface Components ---

# 1. CPU (Central Square Chip)
cpu = (cq.Workplane("XY")
       .workplane(offset=pcb_thick/2)
       .rect(13, 13)
       .extrude(1.5))

# 2. Wireless Shield (Left side rectangular component)
# Positioned to the left of the CPU
shield_pos_x = -pcb_width/4 - 5
shield_pos_y = -5
shield = (cq.Workplane("XY")
          .workplane(offset=pcb_thick/2)
          .center(shield_pos_x, shield_pos_y)
          .rect(12, 16)
          .extrude(2.0))

# 3. Side Connector Housing (Left Edge)
# Protrudes from the left edge near the shield
side_conn = (cq.Workplane("XY")
             .workplane(offset=pcb_thick/2)
             .center(-pcb_width/2 + 1, -5)
             .rect(6, 10)
             .extrude(2.5))

# --- Top Edge Connectors (Back Edge in +Y) ---
# Coordinates are relative to center. Top edge is at y = pcb_depth/2

# 4. Micro USB Power (Left)
musb_x = -28
musb = (cq.Workplane("XY")
        .workplane(offset=pcb_thick/2)
        .center(musb_x, pcb_depth/2 - 2)
        .rect(8, 6)
        .extrude(3.0))
# Cut interior
musb = musb.faces(">Y").workplane().rect(6, 1.8).cutBlind(-4)

# 5. HDMI Port (Mid-Left)
hdmi_x = -10
hdmi = (cq.Workplane("XY")
        .workplane(offset=pcb_thick/2)
        .center(hdmi_x, pcb_depth/2 - 2)
        .rect(15, 10)
        .extrude(5.5))
# Cut interior
hdmi = hdmi.faces(">Y").workplane().rect(12.5, 3.5).cutBlind(-6)

# 6. Display/Camera Flex Connector (Vertical Slot between HDMI and Audio)
flex_x = 5
flex_conn = (cq.Workplane("XY")
             .workplane(offset=pcb_thick/2)
             .center(flex_x, pcb_depth/2 - 6)
             .rect(4, 12)
             .extrude(4.5))
# Slot cut
flex_conn = flex_conn.faces(">Z").workplane().rect(2, 10).cutBlind(-3.5)

# 7. Audio Jack (Mid-Right)
audio_x = 18
# Base block
audio_base = (cq.Workplane("XY")
              .workplane(offset=pcb_thick/2)
              .center(audio_x, pcb_depth/2 - 3.5)
              .rect(6.5, 7)
              .extrude(6.0))
# Cylindrical port
audio_cyl = (cq.Workplane("XY")
             .workplane(offset=pcb_thick/2 + 3.0)
             .center(audio_x, pcb_depth/2)
             .transformed(rotate=cq.Vector(90, 0, 0))
             .cylinder(3.0, 3.0)) # length, radius
audio = audio_base.union(audio_cyl)

# 8. Ethernet/USB Combo Block (Right)
eth_x = 36
eth_h = 15.0
eth_block = (cq.Workplane("XY")
             .workplane(offset=pcb_thick/2)
             .center(eth_x, pcb_depth/2 - 2)
             .rect(17, 21)
             .extrude(eth_h))
# Detail: Cutouts for ports on the back face
eth_block = (eth_block.faces(">Y").workplane()
             .center(0, 3.5).rect(13, 5).cutBlind(-2) # Top USB/Port
             .center(0, -5.5).rect(13, 9).cutBlind(-2)) # Bottom Ethernet

# --- Bottom Components ---

# 9. SD Card Slot (Underneath, Left side)
sd_slot = (cq.Workplane("XY")
           .workplane(offset=-pcb_thick/2)
           .center(-pcb_width/2 + 3, 0)
           .rect(16, 14)
           .extrude(-1.8))
# Cut slot opening on the side
sd_slot = (sd_slot.faces("<X").workplane()
           .rect(1.0, 10)
           .cutBlind(-15))

# --- Assembly ---
result = pcb
result = result.union(cpu)
result = result.union(shield)
result = result.union(side_conn)
result = result.union(musb)
result = result.union(hdmi)
result = result.union(flex_conn)
result = result.union(audio)
result = result.union(eth_block)
result = result.union(sd_slot)

# Optional: Fillet sharp edges on larger blocks for realism
# result = result.edges("|Z").fillet(0.5) 