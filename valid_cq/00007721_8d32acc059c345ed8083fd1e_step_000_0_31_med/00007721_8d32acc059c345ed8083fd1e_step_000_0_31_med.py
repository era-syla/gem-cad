import cadquery as cq

# Parameters
mast_size = 20
mast_height = 400

shield_thickness = 3
shield_height = 200
shield_top_width = 250
shield_bottom_width = 80

arm_width = 15
arm_height = 15
arm_length = 250
hole_dia = 6
hole_spacing = 25

disc_radius = 80
disc_thickness = 3

hub_size = 60

# 1. Mast (Simulating an Aluminum Extrusion Profile)
mast = cq.Workplane("XY").box(mast_size, mast_size, mast_height)
groove_width = 6
groove_depth = 6

# Cut grooves on all 4 sides of the mast
for angle in [0, 90, 180, 270]:
    groove = (cq.Workplane("XY")
              .transformed(rotate=cq.Vector(0, 0, angle))
              .center(0, mast_size/2)
              .box(groove_width, groove_depth*2, mast_height))
    mast = mast.cut(groove)

mast = mast.translate((0, 0, mast_height/2 - hub_size/2))

# 2. Shield Plate
shield_pts = [
    (shield_bottom_width/2, 0),
    (shield_top_width/2, shield_height),
    (-shield_top_width/2, shield_height),
    (-shield_bottom_width/2, 0)
]
shield = (cq.Workplane("XZ")
          .polyline(shield_pts).close()
          .extrude(shield_thickness)
          .edges("|Y").fillet(15)
          .translate((0, mast_size/2, -20)))

# 3. Hub Base
hub = (cq.Workplane("XY")
       .box(hub_size, hub_size, hub_size)
       .edges("|Z").chamfer(15))

# 4. Bottom Disc
disc = (cq.Workplane("XY")
        .circle(disc_radius)
        .extrude(disc_thickness)
        .translate((0, 0, -hub_size/2 - disc_thickness)))

# 5. Extension Arm with Holes
arm_base = (cq.Workplane("XY")
            .box(arm_length, arm_width, arm_height)
            .translate((-arm_length/2 - hub_size/2, 0, 0)))

num_holes = int(arm_length / hole_spacing) - 1
for i in range(num_holes):
    x_pos = -hub_size/2 - hole_spacing * (i + 1)
    hole = (cq.Workplane("XY")
            .center(x_pos, 0)
            .circle(hole_dia/2)
            .extrude(arm_height*2, both=True))
    arm_base = arm_base.cut(hole)

arm = arm_base

# 6. Angled Brackets
bracket_len = 60
bracket_wid = 25
bracket_thk = 5

bracket_base = cq.Workplane("XY").box(bracket_wid, bracket_thk, bracket_len)
b1 = bracket_base.rotate((0,0,0), (0,1,0), -45).translate((30, hub_size/2 + bracket_thk/2, 10))
b2 = bracket_base.rotate((0,0,0), (0,1,0), 45).translate((-30, hub_size/2 + bracket_thk/2, 10))

# Combine all components into the final result
result = (mast
          .union(shield)
          .union(hub)
          .union(disc)
          .union(arm)
          .union(b1)
          .union(b2))