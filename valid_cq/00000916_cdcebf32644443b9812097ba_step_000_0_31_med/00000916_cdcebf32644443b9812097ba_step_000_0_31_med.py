import cadquery as cq

# --- Parameters ---
body_l, body_w, body_h = 24.0, 14.0, 14.0
intake_offset = -3.0
intake_r = 6.0
intake_h = 8.0
bore_r = 4.0
barrel_r = 4.5

# --- Main Block ---
base = cq.Workplane("XY").box(body_l, body_w, body_h)

# --- Top Intake Stack ---
intake = (cq.Workplane("XY").workplane(offset=body_h/2)
          .center(intake_offset, 0)
          .circle(intake_r)
          .extrude(intake_h))
intake_lip = (cq.Workplane("XY").workplane(offset=body_h/2 + intake_h - 1.5)
              .center(intake_offset, 0)
              .circle(intake_r + 1.2)
              .extrude(1.5))
base = base.union(intake).union(intake_lip)

# --- Bottom Boss ---
bottom_boss = (cq.Workplane("XY").workplane(offset=-body_h/2)
               .center(intake_offset, 0)
               .circle(intake_r - 0.5)
               .extrude(-6.0))
base = base.union(bottom_boss)

# --- Venturi Cut ---
venturi_pts = [
    (0, -body_h/2 - 6.0),
    (bore_r, -body_h/2 - 6.0),
    (bore_r, body_h/2 + intake_h - 4.0),
    (intake_r + 0.2, body_h/2 + intake_h),
    (0, body_h/2 + intake_h)
]
venturi_cut = (cq.Workplane("XZ", origin=(intake_offset, 0, 0))
               .polyline(venturi_pts).close()
               .revolve(360, (0, 0, 0), (0, 1, 0)))
base = base.cut(venturi_cut)

# --- Left Side Throttle Barrel & Lever ---
left_x = -body_l/2
lever_thickness = 1.2

barrel_l = (cq.Workplane("YZ").workplane(offset=left_x)
            .circle(barrel_r)
            .extrude(-3.0))
base = base.union(barrel_l)

# Lever Arm
lever = (cq.Workplane("YZ").workplane(offset=left_x - 3.0)
         .moveTo(4, 4)
         .lineTo(-4, 4)
         .lineTo(-4, -2)
         .lineTo(-9, -12)
         .lineTo(-9, -19)
         .lineTo(-3, -19)
         .lineTo(4, -5)
         .close()
         .extrude(-lever_thickness))
# Lever hole
lever = lever.faces("<X").workplane().center(-6, -15.5).hole(2.5)
base = base.union(lever)

# Nut
nut = (cq.Workplane("YZ").workplane(offset=left_x - 3.0 - lever_thickness)
       .polygon(6, 7.0)
       .extrude(-3.0))
base = base.union(nut)

# Screw Head
screw = (cq.Workplane("YZ").workplane(offset=left_x - 3.0 - lever_thickness - 3.0)
         .circle(2.5)
         .extrude(-1.5))
slot = (cq.Workplane("YZ").workplane(offset=left_x - 3.0 - lever_thickness - 4.5)
        .rect(6, 1)
        .extrude(0.6))
screw = screw.cut(slot)
base = base.union(screw)

# --- Right Side (Needle Valve) ---
right_x = body_l/2

# Large adjustment dial
large_disc = (cq.Workplane("YZ").workplane(offset=right_x)
              .polygon(24, 15.0)
              .extrude(2.0))
base = base.union(large_disc)

# Barrel extension
barrel_r_side = (cq.Workplane("YZ").workplane(offset=right_x + 2.0)
                 .circle(3.5)
                 .extrude(5.0))
base = base.union(barrel_r_side)

# Needle Shaft
needle_shaft = (cq.Workplane("YZ").workplane(offset=right_x + 7.0)
                .circle(1.5)
                .extrude(8.0))
base = base.union(needle_shaft)

# Needle Knob base
knob_base = (cq.Workplane("YZ").workplane(offset=right_x + 15.0)
             .circle(2.5)
             .extrude(1.5))
base = base.union(knob_base)

# Needle Knob (Knurled simulation)
knurled_knob = (cq.Workplane("YZ").workplane(offset=right_x + 16.5)
                .polygon(16, 9.0)
                .extrude(4.0))
base = base.union(knurled_knob)

# Needle Knob Tip
knob_tip = (cq.Workplane("YZ").workplane(offset=right_x + 20.5)
            .circle(2.0)
            .extrude(2.0))
base = base.union(knob_tip)

# --- Idle Screw (Top Front Left) ---
idle_boss = (cq.Workplane("XY").workplane(offset=body_h/2)
             .center(-body_l/2 + 3.5, body_w/2 - 2.5)
             .circle(2.5)
             .extrude(2.5))
idle_screw = (cq.Workplane("XY").workplane(offset=body_h/2 + 2.5)
              .center(-body_l/2 + 3.5, body_w/2 - 2.5)
              .circle(1.8)
              .extrude(2.0))
idle_slot = (cq.Workplane("XY").workplane(offset=body_h/2 + 4.5)
             .center(-body_l/2 + 3.5, body_w/2 - 2.5)
             .rect(4, 0.8)
             .extrude(-0.6))
base = base.union(idle_boss).union(idle_screw).cut(idle_slot)

result = base