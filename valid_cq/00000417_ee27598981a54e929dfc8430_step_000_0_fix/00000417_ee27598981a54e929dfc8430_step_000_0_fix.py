import cadquery as cq

# Main block dimensions
main_w = 80
main_d = 60
main_h = 50

# Create the main rectangular body
body = cq.Workplane("XY").box(main_w, main_d, main_h)

# Add cross-shaped extensions on top (left and right wings)
# Left wing extension
left_wing = cq.Workplane("XY").box(20, main_d, main_h).translate((-50, 0, 0))
# Right wing extension  
right_wing = cq.Workplane("XY").box(20, main_d, main_h).translate((50, 0, 0))

# Front extension
front_wing = cq.Workplane("XY").box(main_w + 40, 20, main_h).translate((0, -40, 0))
# Back extension
back_wing = cq.Workplane("XY").box(main_w + 40, 20, main_h).translate((0, 40, 0))

# Union all wings to body
body = body.union(left_wing).union(right_wing).union(front_wing).union(back_wing)

# Cut a notch/slot from the top center
notch = cq.Workplane("XY").box(30, 25, 15).translate((0, 10, main_h/2 - 7.5 + 7.5))
body = body.cut(notch)

# Add mounting tabs/feet at bottom corners
tab_size = 8
tab_h = 4
tab_positions = [
    (-main_w/2 - 10 + tab_size/2, -main_d/2 - 10 + tab_size/2),
    (main_w/2 + 10 - tab_size/2, -main_d/2 - 10 + tab_size/2),
    (-main_w/2 - 10 + tab_size/2, main_d/2 + 10 - tab_size/2),
    (main_w/2 + 10 - tab_size/2, main_d/2 + 10 - tab_size/2),
]

# Actually let's simplify the approach - create a cleaner model

# Start fresh with a cleaner interpretation
# The image shows a block with cross-shaped top profile and a rectangular cutout on top

# Base dimensions
bw = 80  # base width
bd = 60  # base depth  
bh = 50  # base height

# Create cross shape in XY plane, then extrude
cross = (cq.Workplane("XY")
         .rect(bw, bd)
         .extrude(bh))

# Add side wings (extending left and right)
wing_w = 20
wing_d = bd
wing_h = bh

left = (cq.Workplane("XY")
        .transformed(offset=cq.Vector(-(bw/2 + wing_w/2), 0, 0))
        .rect(wing_w, wing_d)
        .extrude(wing_h))

right = (cq.Workplane("XY")
         .transformed(offset=cq.Vector(bw/2 + wing_w/2, 0, 0))
         .rect(wing_w, wing_d)
         .extrude(wing_h))

# Add front and back wings
wing_w2 = bw + 2*wing_w
wing_d2 = 15
front = (cq.Workplane("XY")
         .transformed(offset=cq.Vector(0, -(bd/2 + wing_d2/2), 0))
         .rect(wing_w2, wing_d2)
         .extrude(wing_h))

back = (cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, bd/2 + wing_d2/2, 0))
        .rect(wing_w2, wing_d2)
        .extrude(wing_h))

combined = cross.union(left).union(right).union(front).union(back)

# Cut a rectangular notch from the top
notch_w = 35
notch_d = 20
notch_h = 15

notch = (cq.Workplane("XY")
         .transformed(offset=cq.Vector(0, 5, bh - notch_h))
         .rect(notch_w, notch_d)
         .extrude(notch_h + 1))

combined = combined.cut(notch)

# Add small mounting feet at bottom
foot_w = 10
foot_d = 10
foot_h = 3

foot_positions = [
    (-(bw/2 + wing_w - foot_w/2), -(bd/2 + wing_d2 - foot_d/2), -foot_h),
    ((bw/2 + wing_w - foot_w/2), -(bd/2 + wing_d2 - foot_d/2), -foot_h),
    (-(bw/2 + wing_w - foot_w/2), (bd/2 + wing_d2 - foot_d/2), -foot_h),
    ((bw/2 + wing_w - foot_w/2), (bd/2 + wing_d2 - foot_d/2), -foot_h),
]

for pos in foot_positions:
    foot = (cq.Workplane("XY")
            .transformed(offset=cq.Vector(pos[0], pos[1], pos[2]))
            .rect(foot_w, foot_d)
            .extrude(foot_h))
    combined = combined.union(foot)

result = combined