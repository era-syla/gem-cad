import cadquery as cq

# --- Parameters ---
pcb_width = 70.0
pcb_height = 70.0
pcb_thick = 1.6
hole_dist = 31.0  # Distance from center to corner holes
hole_dia = 3.2

# --- 1. PCB Base ---
# Create the main board
pcb = (cq.Workplane("XY")
       .box(pcb_width, pcb_height, pcb_thick)
       .faces(">Z").workplane()
       )

# Add Corner Holes
pcb = (pcb.rect(hole_dist * 2, hole_dist * 2, forConstruction=True)
       .vertices()
       .hole(hole_dia)
       )

# Add Bottom Cutout
# Cutout is on the bottom edge (-Y), slightly offset to the right (+X)
notch_w = 20.0
notch_d = 8.0
notch_center_x = 10.0

pcb = (pcb.faces("<Y").workplane()
       .center(notch_center_x, 0)
       .rect(notch_w, notch_d * 2)
       .cutBlind(pcb_thick * 3)
       )

# --- 2. Components ---

# A. Lens Mount (Back Side)
# Located Top-Left quadrant
lm_x, lm_y = -15.0, 15.0
lm_z_start = -pcb_thick / 2

# Square Base Block
lens_base = (cq.Workplane("XY")
             .center(lm_x, lm_y)
             .workplane(offset=lm_z_start - 9)  # Center of 18mm high block
             .box(30, 30, 18)
             )

# Cylindrical Barrel
lens_barrel = (cq.Workplane("XY")
               .center(lm_x, lm_y)
               .workplane(offset=lm_z_start - 18)  # Surface of block
               .circle(13.0)
               .extrude(-18.0)  # Extrude away from board
               )

# Bore hole in barrel
lens_barrel_hole = (cq.Workplane("XY")
                    .center(lm_x, lm_y)
                    .workplane(offset=lm_z_start - 18)
                    .circle(11.0)
                    .extrude(-20.0)
                    )
lens_barrel = lens_barrel.cut(lens_barrel_hole)

# Locking screw boss
screw_pos_z = lm_z_start - 18 - 8
screw_boss = (cq.Workplane("XY")
              .center(lm_x, lm_y)
              .workplane(offset=screw_pos_z)
              .transformed(rotate=(90, 0, 0))
              .workplane(offset=12.5)  # On barrel surface
              .circle(3)
              .extrude(4)
              )

screw_head = (cq.Workplane("XY")
              .center(lm_x, lm_y)
              .workplane(offset=screw_pos_z)
              .transformed(rotate=(90, 0, 0))
              .workplane(offset=16.5)
              .circle(3.5)
              .extrude(2)
              )

# B. Large Header (Front Right Top)
hdr_x = 22.0
hdr_y = 10.0
hdr_w = 9.0
hdr_l = 25.0
hdr_h = 11.0

header_body = (cq.Workplane("XY")
               .workplane(offset=pcb_thick / 2)
               .center(hdr_x, hdr_y)
               .box(hdr_w, hdr_l, hdr_h, centered=(True, True, False))
               )

# Hollow shell
header_body = (header_body.faces(">Z").workplane()
               .rect(hdr_w - 2, hdr_l - 2)
               .cutBlind(-(hdr_h - 2))
               )

# Keying slot
header_body = (header_body.faces(">X").workplane()
               .center(0, hdr_h / 2)
               .rect(3, hdr_h)
               .cutBlind(-2)
               )

# Pins for Header
pin_pts = []
for r in range(5):  # 5 rows
    for c in range(2):  # 2 cols
        px = hdr_x - 1.27 + (c * 2.54)
        py = hdr_y - 5.08 + (r * 2.54)
        pin_pts.append((px, py))

header_pins = (cq.Workplane("XY")
               .workplane(offset=pcb_thick / 2)
               .pushPoints(pin_pts)
               .rect(0.64, 0.64)
               .extrude(hdr_h - 2)
               )

# C. Right Angle Header (Front Right Bottom)
ra_x = 22.0
ra_y = -20.0
ra_rows = 3
ra_cols = 2

ra_base = (cq.Workplane("XY")
           .workplane(offset=pcb_thick / 2)
           .center(ra_x, ra_y)
           .box(5.08, 7.62, 2.5, centered=(True, True, False))
           )

ra_pin_objs = []
for r in range(ra_rows):
    for c in range(ra_cols):
        # Vertical pin part
        px = ra_x - 1.27 + c * 2.54
        py = ra_y - 2.54 + r * 2.54
        v = (cq.Workplane("XY")
             .workplane(offset=pcb_thick / 2)
             .center(px, py)
             .rect(0.64, 0.64)
             .extrude(6.0)
             )
        ra_pin_objs.append(v)
        # Horizontal pin part
        h = (cq.Workplane("YZ")
             .workplane(offset=px)
             .center(py, pcb_thick / 2 + 6.0 - 0.32)
             .rect(0.64, 0.64)
             .extrude(5.0)  # Extrude +X
             )
        ra_pin_objs.append(h)

# D. Small Connector (Front Left)
sm_x = -25.0
sm_y = -5.0
sm_conn = (cq.Workplane("XY")
           .workplane(offset=pcb_thick / 2)
           .center(sm_x, sm_y)
           .box(7, 9, 5, centered=(True, True, False))
           )

# Connector detail
sm_conn = (sm_conn.faces(">X").workplane()
           .center(0, 2.5)
           .rect(4, 4)
           .cutBlind(-2)
           )

# E. Tactile Switch (Front Top Left)
sw_x = -15.0
sw_y = 5.0
sw_body = (cq.Workplane("XY")
           .workplane(offset=pcb_thick / 2)
           .center(sw_x, sw_y)
           .box(6, 6, 3.5, centered=(True, True, False))
           )
sw_btn = (cq.Workplane("XY")
          .workplane(offset=pcb_thick / 2 + 3.5)
          .center(sw_x, sw_y)
          .circle(1.5)
          .extrude(2.0)
          )

# --- Combine All Parts ---
result = pcb
# Union Main Components
result = result.union(lens_base).union(lens_barrel).union(screw_boss).union(screw_head)
result = result.union(header_body).union(header_pins)
result = result.union(ra_base).union(sm_conn).union(sw_body).union(sw_btn)

# Union Arrayed Pins
for p in ra_pin_objs:
    result = result.union(p)