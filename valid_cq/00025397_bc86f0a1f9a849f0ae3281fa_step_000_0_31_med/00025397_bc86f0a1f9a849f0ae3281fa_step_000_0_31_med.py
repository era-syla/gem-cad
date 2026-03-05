import cadquery as cq

# Parameters for the machine vise model
L = 160
W = 60
H = 20
slot_W = 26
slot_D = 12

jaw_H = 35
left_L = 25
right_L = 30

screw_Z = H + 15
screw_R = 6

hub_R = 9
hub_L = 14
collar_R = 7
collar_L = 6

handle_R = 2.5
handle_L = 65
knob_R = 4.5

# 1. Base (U-channel)
base = cq.Workplane("XY").box(L, W, H).translate((L/2, 0, H/2))
base = base.faces(">Z").workplane().center(0, 0).rect(L+10, slot_W).extrude(-slot_D, combine="cut")

# 2. Left Block (Arched fixed support)
left_block = cq.Workplane("XY").box(left_L, W, jaw_H).translate((left_L/2, 0, H + jaw_H/2))
left_block = left_block.edges(">Z and |X").fillet(29)

# Oil hole on top of the left block
oil_hole = cq.Workplane("XY").workplane(offset=H+jaw_H).center(left_L/2, 0).circle(1.5).extrude(-10)
left_block = left_block.cut(oil_hole)

# 3. Right Block (Fixed jaw)
right_block = cq.Workplane("XY").box(right_L, W, jaw_H).translate((L - right_L/2, 0, H + jaw_H/2))
# Jaw plate cutout step
jaw_cut = cq.Workplane("XY").box(8, W+2, 15).translate((L - right_L + 4, 0, H + jaw_H - 7.5))
right_block = right_block.cut(jaw_cut)
# Chamfer the back face
right_block = right_block.edges(">X and >Z").chamfer(15)

# 4. Screw Core
screw = cq.Workplane("YZ").workplane(offset=-20).center(0, screw_Z).circle(screw_R).extrude(160)

# Create threaded appearance using grooved cutouts
pts = [(i * 3, 0) for i in range(33)]
grooves = cq.Workplane("XY").workplane(offset=screw_Z).center(28, 0).pushPoints(pts).box(1.5, 14, 14)
screw = screw.cut(grooves)

# 5. Front Hub and Collar
hub = cq.Workplane("YZ").workplane(offset=-20).center(0, screw_Z).circle(hub_R).extrude(hub_L)
collar = cq.Workplane("YZ").workplane(offset=-6).center(0, screw_Z).circle(collar_R).extrude(collar_L)

# 6. Handle
handle = cq.Workplane("XZ").workplane(offset=0).center(-13, screw_Z).circle(handle_R).extrude(handle_L/2, both=True)

# 7. Knobs
knob1 = cq.Workplane("XZ").workplane(offset=handle_L/2).center(-13, screw_Z).sphere(knob_R)
knob2 = cq.Workplane("XZ").workplane(offset=-handle_L/2).center(-13, screw_Z).sphere(knob_R)

# Combine all components into the final result
result = (
    base
    .union(left_block)
    .union(right_block)
    .union(screw)
    .union(hub)
    .union(collar)
    .union(handle)
    .union(knob1)
    .union(knob2)
)