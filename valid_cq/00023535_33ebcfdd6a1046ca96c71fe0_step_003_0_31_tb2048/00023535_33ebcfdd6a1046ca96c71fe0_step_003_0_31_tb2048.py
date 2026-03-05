import cadquery as cq

# Base Plate
base_plate = cq.Workplane("XY").box(150, 60, 20).translate((0, 0, 10))

# Slot in base
slot = cq.Workplane("XY").moveTo(-2.5, 0).box(105, 20, 20).translate((0, 0, 15))
base_plate = base_plate.cut(slot)

# Rear Jaw
rear_jaw = cq.Workplane("XY").moveTo(62.5, 0).box(25, 60, 35).translate((0, 0, 37.5))

# Front Support
front_support = cq.Workplane("XY").moveTo(-65, 0).box(20, 60, 25).translate((0, 0, 32.5))
front_support = front_support.edges("|X and >Z").chamfer(12)

# Small oil hole in front support
hole = cq.Workplane("XY").workplane(offset=45).moveTo(-65, 0).circle(2).extrude(-10)
front_support = front_support.cut(hole)

# Sliding Jaw
sliding_jaw = cq.Workplane("XY").moveTo(2.5, 0).box(25, 60, 35).translate((0, 0, 37.5))
sliding_jaw = sliding_jaw.edges("|X and >Z").chamfer(12)

# Jaw Plates
fixed_plate = cq.Workplane("XY").moveTo(47.5, 0).box(5, 60, 25).translate((0, 0, 42.5))
sliding_plate = cq.Workplane("XY").moveTo(17.5, 0).box(5, 60, 25).translate((0, 0, 42.5))

# Screw
screw = cq.Workplane("YZ").workplane(offset=-80).moveTo(0, 32).circle(6).extrude(90)

# Handle Hub
hub = cq.Workplane("YZ").workplane(offset=-90).moveTo(0, 32).circle(10).extrude(15)

# Handle Rod
handle_rod = cq.Workplane("XZ").workplane(offset=-40).moveTo(-82.5, 32).circle(3).extrude(80)

# Knobs
knob1 = cq.Workplane("XY").moveTo(-82.5, -40).sphere(5).translate((0, 0, 32))
knob2 = cq.Workplane("XY").moveTo(-82.5, 40).sphere(5).translate((0, 0, 32))

# Combine all components into the final result
result = (
    base_plate
    .union(rear_jaw)
    .union(front_support)
    .union(sliding_jaw)
    .union(fixed_plate)
    .union(sliding_plate)
    .union(screw)
    .union(hub)
    .union(handle_rod)
    .union(knob1)
    .union(knob2)
)