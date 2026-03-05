import cadquery as cq

# Flexible shaft coupling / beam coupling
# Parameters
outer_diameter = 30
outer_radius = outer_diameter / 2
total_height = 40
bore_diameter = 8
bore_radius = bore_diameter / 2

# Build main cylinder
result = cq.Workplane("XY").cylinder(total_height, outer_radius)

# Central bore (through hole)
result = result.faces(">Z").workplane().circle(bore_radius).cutThruAll()

# Cut helical-like slots (beam coupling spiral cuts approximated as angled slots)
# The coupling has spiral cuts that create the flexible beam section
# Approximate with rectangular cuts at different angles

# Slot parameters
slot_width = 1.5
slot_depth = outer_radius - 2  # almost through to center

# Top section slot (vertical cut from side, near top)
# Cut 1 - at 0 degrees, near top
result = (result
    .faces(">Z").workplane(offset=-5)
    .transformed(rotate=cq.Vector(0, 0, 0))
    .rect(slot_depth * 2, slot_width)
    .cutBlind(-slot_width)
)

# Actually let's do the spiral cuts as thin slots cut from the outer surface
# These are the characteristic cuts of a beam coupling

# Create the main body first fresh
body = cq.Workplane("XY").cylinder(total_height, outer_radius)

# Central bore
body = body.faces(">Z").workplane().circle(bore_radius).cutThruAll()

# Helical slots - approximate as rectangular cuts at various heights and rotations
# A beam coupling typically has 3-4 spiral cuts

cut_angles = [0, 180, 60, 240, 120, 300]
cut_heights = [-14, -14, -7, -7, 0, 0]

for angle, height in zip(cut_angles, cut_heights):
    # Create a slot box that cuts through from one side
    slot_box = (cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, height), rotate=cq.Vector(0, 0, angle))
        .rect(outer_diameter + 2, slot_width)
        .extrude(2)
    )
    body = body.cut(slot_box)

# Clamping slots (vertical slots at top and bottom sections)
# Top clamping slot
top_slot = (cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, total_height/2 - 5), rotate=cq.Vector(0, 0, 0))
    .rect(outer_diameter + 2, 2)
    .extrude(8)
)
body = body.cut(top_slot)

# Bottom clamping slot  
bot_slot = (cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -total_height/2 + 1), rotate=cq.Vector(0, 0, 90))
    .rect(outer_diameter + 2, 2)
    .extrude(8)
)
body = body.cut(bot_slot)

# Add set screw holes (hex socket) in clamping sections
# Top set screw hole
top_screw = (cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, total_height/2 - 9, outer_radius - 3))
    .circle(2)
    .extrude(8)
)
body = body.cut(top_screw)

# Bottom set screw hole
bot_screw = (cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, -total_height/2 + 5, outer_radius - 3))
    .circle(2)
    .extrude(8)
)
body = body.cut(bot_screw)

# Add grooves on the flexible section
for z_offset in [-10, -6, -2, 2, 6, 10]:
    groove = (cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, z_offset))
        .circle(outer_radius + 0.1)
        .circle(outer_radius - 1.0)
        .extrude(1.0)
    )
    body = body.cut(groove)

result = body