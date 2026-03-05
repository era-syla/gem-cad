import cadquery as cq

# --- Parametric Variables ---

# Main dimensions
base_length = 80.0
base_width = 40.0
base_thickness = 5.0

# Front vertical plate
front_plate_width = 70.0  # Wider than the base
front_plate_height = 20.0
front_plate_thickness = 5.0

# Rear block
rear_block_length = 30.0
rear_block_width = 20.0
rear_block_height = 15.0  # Height above base

# Central groove/rail section
rail_width = 6.0
rail_height = 3.0  # Height above base
rail_gap = 6.0     # Gap between rails

# Side mounting tabs (ears)
ear_length = 15.0
ear_width = 20.0
ear_offset_from_front = 40.0 # Approximate position

# Holes
mount_hole_dia = 4.0
slot_length = 8.0
slot_width = 4.0
front_hole_dia = 5.0
rear_block_hole_dia = 5.0

# Small details
stop_block_size = 5.0  # Small cubes near the front
triangular_rib_size = 10.0

# --- Geometry Construction ---

# 1. Base Plate (The central flat part)
# We will build this centered on Y for symmetry
base = cq.Workplane("XY").box(base_length, base_width, base_thickness, centered=(True, True, False))

# 2. Add the Rear Block
# Positioned at the back (-X direction)
rear_block = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(-base_length/2 + rear_block_length/2, 0)
    .box(rear_block_length, rear_block_width, rear_block_height, centered=(True, True, False))
)

# 3. Add the Front Vertical Plate
# Positioned at the front (+X direction)
# It extends below and above the base slightly, based on the image visual
front_plate = (
    cq.Workplane("XY")
    .center(base_length/2 - front_plate_thickness/2, 0)
    .box(front_plate_thickness, front_plate_width, front_plate_height + base_thickness, centered=(True, True, False))
    .translate((0, 0, -5)) # Shift down so it's flush with bottom or slightly lower
)

# 4. Create the main shape by union
main_body = base.union(rear_block).union(front_plate)

# 5. Add Side Ears (Mounting Tabs) with Slots
# Left Ear
left_ear = (
    cq.Workplane("XY")
    .center(-base_length/2 + ear_length/2, base_width/2 + ear_width/2 - 5) # Overlap slightly
    .box(ear_length, ear_width, base_thickness, centered=(True, True, False))
)
# Right Ear (Mirror or create new)
right_ear = (
    cq.Workplane("XY")
    .center(-base_length/2 + ear_length/2, -base_width/2 - ear_width/2 + 5)
    .box(ear_length, ear_width, base_thickness, centered=(True, True, False))
)

main_body = main_body.union(left_ear).union(right_ear)


# 6. Cut the Central features
# There's a deep channel in the middle of the base, but rails sticking up.
# Let's cut the central channel first.
channel_width = rail_gap
channel_depth = base_thickness # Through cut? Or partial? Looks partial or through. Let's do partial deep.

# Actually, looking closer, it looks like two rails are ADDED on top of the base.
# Let's add the rails.
rail_length = base_length - rear_block_length - front_plate_thickness
rail_geo = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center((base_length/2 - front_plate_thickness) - rail_length/2, 0)
    .rect(rail_length, rail_width*2 + rail_gap) # Overall footprint
    .extrude(rail_height)
)

# Now cut the slot between the rails
rail_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center((base_length/2 - front_plate_thickness) - rail_length/2, 0)
    .rect(rail_length + 2, rail_gap) # slightly longer for clean cut
    .extrude(rail_height + 1)
)

rails = rail_geo.cut(rail_cut)
main_body = main_body.union(rails)

# 7. Add Triangular Ribs
# There are small triangular supports near the front plate on the sides of the central body
rib_pts = [(0, 0), (triangular_rib_size, 0), (0, triangular_rib_size)]
right_rib = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(base_length/2 - front_plate_thickness - 0.1, base_width/2 - 5)
    .polyline(rib_pts).close()
    .extrude(5) # Thickness of rib
    .rotate((0,0,0), (1,0,0), -90) # Orient correctly
    .rotate((0,0,0), (0,0,1), -90)
    .translate((0, -5, 0)) # Adjust position
)

left_rib = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(base_length/2 - front_plate_thickness - 0.1, -base_width/2 + 5)
    .polyline(rib_pts).close()
    .extrude(5)
    .rotate((0,0,0), (1,0,0), -90)
    .rotate((0,0,0), (0,0,1), -90)
    .translate((0, 5 + 5, 0)) # Adjust position (thickness is 5)
)

# 8. Add Small Stop Blocks
# Located near the front plate, inside the main width
stop_block_right = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(base_length/2 - front_plate_thickness - stop_block_size/2 - 2, base_width/2 - stop_block_size/2 - 2)
    .box(stop_block_size, stop_block_size, stop_block_size, centered=(True, True, False))
)
stop_block_left = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(base_length/2 - front_plate_thickness - stop_block_size/2 - 2, -(base_width/2 - stop_block_size/2 - 2))
    .box(stop_block_size, stop_block_size, stop_block_size, centered=(True, True, False))
)

main_body = main_body.union(stop_block_right).union(stop_block_left)


# 9. Cuts and Holes

# Rear Block Hole (Horizontal)
main_body = (
    main_body.faces(">X").workplane()
    .center(0, rear_block_height/2 + base_thickness/2 ) # Adjust Z height relative to face center
    .hole(rear_block_hole_dia, depth=rear_block_length/2) # Partial depth
)

# Front Plate Holes
main_body = (
    main_body.faces(">X").workplane()
    .pushPoints([(0, front_plate_width/2 - 10), (0, -front_plate_width/2 + 10)])
    .hole(front_hole_dia)
)

# Front Plate Center Cutout (U-shape)
# This creates the gap in the middle of the front plate
u_cut_width = rail_gap + 2 * rail_width
u_cut_height = front_plate_height / 2
main_body = (
    main_body.faces(">X").workplane()
    .center(0, front_plate_height/2 + base_thickness - u_cut_height/2) # Approx vertical center
    .rect(u_cut_width, u_cut_height * 2) # Exaggerate height to cut through top
    .cutBlind(-front_plate_thickness - 1)
)

# Slots in side ears
# Left Ear Slot
main_body = (
    main_body.faces(">Z").workplane()
    .center(-base_length/2 + ear_length/2, base_width/2 + ear_width/2 - 5)
    .slot2D(slot_length, slot_width, 90)
    .cutThruAll()
)

# Right Ear Slot
main_body = (
    main_body.faces(">Z").workplane()
    .center(-base_length/2 + ear_length/2, -base_width/2 - ear_width/2 + 5)
    .slot2D(slot_length, slot_width, 90)
    .cutThruAll()
)

# Small circular holes in the main base (visible near the small stop blocks)
main_body = (
    main_body.faces(">Z").workplane()
    .pushPoints([
        (base_length/2 - front_plate_thickness - 10, base_width/2 - 8),
        (base_length/2 - front_plate_thickness - 10, -base_width/2 + 8)
    ])
    .hole(4.0)
)

# Final result assignment
result = main_body