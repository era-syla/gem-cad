import cadquery as cq

# --- Base Plate ---
base = cq.Workplane("XY").box(180, 70, 25, centered=(True, True, False))

# Central channel
channel = cq.Workplane("XY", origin=(0, 0, 25)).box(180, 30, 15, centered=(True, True, False)).translate((0, 0, -15))
base = base.cut(channel)

# Side slots for mounting
slot1 = cq.Workplane("XY", origin=(0, 35, 8)).box(180, 15, 12, centered=(True, True, True))
slot2 = cq.Workplane("XY", origin=(0, -35, 8)).box(180, 15, 12, centered=(True, True, True))
base = base.cut(slot1).cut(slot2)

# --- Fixed Jaw ---
fixed_jaw = (
    cq.Workplane("XZ", origin=(0, 0, 25))
    .moveTo(60, 0)
    .lineTo(90, 0)
    .lineTo(90, 50)
    .lineTo(75, 50)
    .lineTo(75, 20)
    .lineTo(60, 20)
    .close()
    .extrude(35, both=True)
)
base = base.union(fixed_jaw)

# --- Front Support ---
front_support = (
    cq.Workplane("YZ", origin=(-90, 0, 25))
    .moveTo(-35, 0)
    .lineTo(-35, 15)
    .threePointArc((0, 50), (35, 15))
    .lineTo(35, 0)
    .close()
    .extrude(20)
)
# Hole for screw in front support
hole = cq.Workplane("YZ", origin=(-90, 0, 40)).circle(8).extrude(20)
front_support = front_support.cut(hole)
base = base.union(front_support)

# --- Moving Jaw ---
moving_jaw = (
    cq.Workplane("YZ", origin=(-35, 0, 25))
    .moveTo(-35, 0)
    .lineTo(-35, 15)
    .threePointArc((0, 50), (35, 15))
    .lineTo(35, 0)
    .close()
    .extrude(30)
)

# Step cut in moving jaw to match fixed jaw
step_cut = cq.Workplane("XY", origin=(-12.5, 0, 45)).box(15, 70, 40, centered=(True, True, False))
moving_jaw = moving_jaw.cut(step_cut)

# Guide block under moving jaw
guide = cq.Workplane("XY", origin=(-20, 0, 25)).box(30, 29.5, 14, centered=(True, True, False)).translate((0, 0, -14))
moving_jaw = moving_jaw.union(guide)

# --- Screw and Handle Mechanism ---
screw = cq.Workplane("YZ", origin=(-110, 0, 40)).circle(7).extrude(100)

collar = cq.Workplane("YZ", origin=(-95, 0, 40)).circle(10).extrude(5)
hub = cq.Workplane("YZ", origin=(-110, 0, 40)).circle(12).extrude(15)

handle = cq.Workplane("XZ", origin=(-102.5, 0, 40)).circle(3.5).extrude(45, both=True)
knob1 = cq.Workplane("XY", origin=(-102.5, 45, 40)).sphere(6)
knob2 = cq.Workplane("XY", origin=(-102.5, -45, 40)).sphere(6)

# --- Final Assembly ---
result = (
    base
    .union(moving_jaw)
    .union(screw)
    .union(collar)
    .union(hub)
    .union(handle)
    .union(knob1)
    .union(knob2)
)