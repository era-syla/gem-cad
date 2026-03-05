import cadquery as cq

# --- Dimensions & Parameters ---
# Overall ship dimensions
L = 160.0  # Length
W = 22.0   # Beam (Width)
H = 14.0   # Hull Height

# Hull profile parameters
bow_x = -L / 2
stern_x = L / 2
deck_w = W / 2
water_w = W / 2 * 0.65  # Waterline is narrower

# --- 1. Hull Construction ---
# Create the hull by lofting a bottom waterline profile to a top deck profile

# Bottom profile (Waterline)
# 5 points: Bow tip, Mid-fwd Left, Stern Left, Stern Right, Mid-fwd Right
pts_bottom = [
    (bow_x + 5, 0),
    (bow_x + 40, water_w),
    (stern_x, water_w),
    (stern_x, -water_w),
    (bow_x + 40, -water_w)
]

# Top profile (Deck)
pts_top = [
    (bow_x, 0),
    (bow_x + 35, deck_w),
    (stern_x + 2, deck_w),
    (stern_x + 2, -deck_w),
    (bow_x + 35, -deck_w)
]

hull = (cq.Workplane("XY")
        .polyline(pts_bottom).close()
        .workplane(offset=H)
        .polyline(pts_top).close()
        .loft(combine=True))

# Create a stepped down flight deck at the stern
flight_deck_cut = (cq.Workplane("XY")
                   .workplane(offset=H - 3)
                   .moveTo(stern_x - 25, 0)
                   .rect(35, W + 5)
                   .extrude(10))

hull = hull.cut(flight_deck_cut)

# --- 2. Main Superstructure Base ---
# A large block sitting on the mid-deck
ss_len = 80
ss_width = W * 0.8
ss_height = 8
ss_center_x = 0

ss_base = (cq.Workplane("XY")
           .workplane(offset=H)
           .moveTo(ss_center_x, 0)
           .rect(ss_len, ss_width)
           .extrude(ss_height)
           .edges("|Z").fillet(2)        # Rounded vertical corners
           .edges(">Z").chamfer(1.5)     # Stealthy chamfer on top
           )

# --- 3. Forward Bridge & Mast ---
# Located on the forward part of the superstructure
bridge_x = ss_center_x - 20
bridge_dim = 16
bridge_h = 10

bridge = (cq.Workplane("XY")
          .workplane(offset=H + ss_height)
          .moveTo(bridge_x, 0)
          .rect(bridge_dim + 4, bridge_dim)
          .extrude(bridge_h, taper=15)  # Pyramidal taper
          )

# Main Mast
mast_h = 25
mast = (cq.Workplane("XY")
        .workplane(offset=H + ss_height + bridge_h)
        .moveTo(bridge_x, 0)
        .circle(3)
        .workplane(offset=mast_h)
        .circle(0.5)
        .loft()
        )

# Mast Crossbars (Yardarms)
yardarm = (cq.Workplane("XY")
           .workplane(offset=H + ss_height + bridge_h + mast_h * 0.6)
           .moveTo(bridge_x, 0)
           .box(2, 18, 1)
           )

# Secondary radar platform on bridge
bridge_radar = (cq.Workplane("XY")
                .workplane(offset=H + ss_height + bridge_h * 0.5)
                .moveTo(bridge_x + 4, 0)
                .box(6, 6, 4)
                )

# --- 4. Aft Funnel & Radar Tower ---
# Located on the aft part of the superstructure
aft_x = ss_center_x + 20
aft_dim_l = 22
aft_dim_w = 18
aft_h = 12

aft_tower = (cq.Workplane("XY")
             .workplane(offset=H + ss_height)
             .moveTo(aft_x, 0)
             .rect(aft_dim_l, aft_dim_w)
             .extrude(aft_h, taper=10)
             )

# Funnel exhausts
funnels = (cq.Workplane("XY")
           .workplane(offset=H + ss_height + aft_h)
           .moveTo(aft_x, 0)
           .rect(8, 10)
           .extrude(4)
           )

# Aft Radar Dome
aft_dome = (cq.Workplane("XY")
            .workplane(offset=H + ss_height + aft_h)
            .moveTo(aft_x + 6, 0)
            .sphere(3.5)
            )

# Aft Sensor Mast
aft_mast = (cq.Workplane("XY")
            .workplane(offset=H + ss_height + aft_h)
            .moveTo(aft_x - 6, 5)
            .circle(1.5)
            .extrude(12)
            )

# --- 5. Weapons & Details ---

# Main Gun Turret (Forward)
gun_x = bow_x + 30
turret_base = (cq.Workplane("XY")
               .workplane(offset=H)
               .moveTo(gun_x, 0)
               .circle(4.5)
               .extrude(3.5)
               .faces(">Z").workplane()
               .box(5, 4, 2.5) # Turret housing
               )

gun_barrel = (cq.Workplane("XY")
              .workplane(offset=H + 2)
              .moveTo(gun_x, 0)
              .transformed(rotate=(0, -5, 0)) # Elevation angle
              .box(14, 1.2, 1.2, centered=(False, True, True)) # Point forward
              )

# Side Sponsons (Mid-ship protrusions)
sponson_w = W + 6
sponson_x = ss_center_x
sponsons = (cq.Workplane("XY")
            .workplane(offset=H - 2)
            .moveTo(sponson_x, 0)
            .rect(15, sponson_w)
            .extrude(3)
            )

# CIWS / Small guns on sponsons
ciws_left = (cq.Workplane("XY")
             .workplane(offset=H + 1)
             .moveTo(sponson_x, sponson_w / 2 - 2)
             .cylinder(3, 2)
             .faces(">Z").workplane().sphere(1.5)
             )

ciws_right = (cq.Workplane("XY")
              .workplane(offset=H + 1)
              .moveTo(sponson_x, -sponson_w / 2 + 2)
              .cylinder(3, 2)
              .faces(">Z").workplane().sphere(1.5)
              )

# VLS Cells (Vertical Launch System) - simplified as a grid plate
vls_plate = (cq.Workplane("XY")
             .workplane(offset=H)
             .moveTo(gun_x + 15, 0)
             .rect(10, 12)
             .extrude(0.5)
             )

# --- 6. Assembly ---
result = (hull
          .union(ss_base)
          .union(bridge)
          .union(mast)
          .union(yardarm)
          .union(bridge_radar)
          .union(aft_tower)
          .union(funnels)
          .union(aft_dome)
          .union(aft_mast)
          .union(turret_base)
          .union(gun_barrel)
          .union(sponsons)
          .union(ciws_left)
          .union(ciws_right)
          .union(vls_plate)
          )