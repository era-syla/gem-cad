import cadquery as cq

# --- Parametric Dimensions ---

# Main mounting plate
plate_width = 150.0
plate_height = 80.0
plate_thickness = 10.0
corner_radius = 8.0

# Mounting slots (oblongs)
slot_width = 6.0
slot_length = 12.0
slot_inset_x = 10.0
slot_inset_y = 15.0

# Rear V-slot extrusion profile (simulated)
extrusion_size = 20.0
extrusion_length = 50.0 # Length sticking out back
extrusion_offset_z = -extrusion_length 

# Top adjustment plate
adj_plate_width = 50.0
adj_plate_height = 40.0
adj_plate_thickness = 3.0
adj_plate_y_offset = 15.0 # Relative to center of main plate

# Wheel/Bearing assembly (bottom)
wheel_diameter = 24.0
wheel_thickness = 8.0
wheel_spacer_dia = 12.0
wheel_spacer_height = 4.0
wheel_bolt_head_dia = 5.0
wheel_y_offset = -20.0

# Top tensioner/eccentric spacer assembly
eccentric_dia = 12.0
eccentric_height = 10.0
eccentric_bolt_dia = 5.0

# Small screws/bolts
screw_head_dia = 4.0
screw_head_height = 2.0
screw_spacing = 8.0

# --- Geometry Construction ---

# 1. Main Mounting Plate
# Create a base rectangle with rounded corners
main_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add Mounting Slots
# We need 4 slots near the corners
slot_locations = [
    (plate_width/2 - slot_inset_x, plate_height/2 - slot_inset_y),
    (plate_width/2 - slot_inset_x, -plate_height/2 + slot_inset_y),
    (-plate_width/2 + slot_inset_x, plate_height/2 - slot_inset_y),
    (-plate_width/2 + slot_inset_x, -plate_height/2 + slot_inset_y),
]

main_plate = (
    main_plate.faces(">Z")
    .workplane()
    .pushPoints(slot_locations)
    .slot2D(slot_length, slot_width, 90) # Vertical slots
    .cutThruAll()
)

# 3. Rear Extrusion (Simulated Connection)
# Attached to the back
extrusion = (
    cq.Workplane("XY")
    .rect(extrusion_size, extrusion_size * 2) # Often a 2040 profile
    .extrude(extrusion_length)
    .translate((0, 0, -extrusion_length - plate_thickness/2))
)

# Combine plate and extrusion
result = main_plate.union(extrusion)

# 4. Top Adjustment Plate (The rectangular plate on top)
adj_plate = (
    cq.Workplane("XY")
    .box(adj_plate_width, adj_plate_height, adj_plate_thickness)
    .translate((0, adj_plate_y_offset, plate_thickness/2 + adj_plate_thickness/2))
)

# Add slots and holes to adjustment plate
adj_plate = (
    adj_plate.faces(">Z").workplane()
    # Center hole for eccentric nut
    .circle(eccentric_dia/2 + 1) 
    # Side slots
    .pushPoints([(-15, 0), (15, 0)])
    .slot2D(10, 4, 90)
    .cutThruAll()
)

result = result.union(adj_plate)

# 5. Top Roller/Eccentric Nut Assembly
eccentric_nut = (
    cq.Workplane("XY")
    .circle(eccentric_dia/2)
    .extrude(eccentric_height)
    .translate((0, adj_plate_y_offset, plate_thickness/2 + adj_plate_thickness))
)

top_bolt = (
    cq.Workplane("XY")
    .circle(eccentric_bolt_dia/2)
    .extrude(eccentric_height + 2)
    .translate((0, adj_plate_y_offset, plate_thickness/2 + adj_plate_thickness))
)

result = result.union(eccentric_nut).union(top_bolt)

# 6. Bottom Wheel Assembly
# Create the main wheel
wheel = (
    cq.Workplane("XY")
    .circle(wheel_diameter/2)
    .extrude(wheel_thickness)
    # Bevel the edge to look like a v-wheel
    .faces(">Z").edges()
    .chamfer(2.0)
    .translate((0, wheel_y_offset, plate_thickness/2))
)

# Spacer/hub
wheel_hub = (
    cq.Workplane("XY")
    .circle(wheel_spacer_dia/2)
    .extrude(wheel_thickness + wheel_spacer_height)
    .translate((0, wheel_y_offset, plate_thickness/2))
)

# Center bolt
wheel_bolt = (
    cq.Workplane("XY")
    .circle(wheel_bolt_head_dia/2)
    .extrude(2.0)
    .translate((0, wheel_y_offset, plate_thickness/2 + wheel_thickness + wheel_spacer_height))
)
# Tiny nub on bolt
wheel_bolt_nub = (
    cq.Workplane("XY")
    .circle(1.5)
    .extrude(3.0)
    .translate((0, wheel_y_offset, plate_thickness/2 + wheel_thickness + wheel_spacer_height))
)

result = result.union(wheel).union(wheel_hub).union(wheel_bolt).union(wheel_bolt_nub)


# 7. Small Screw Heads (Bottom row)
# The image shows a row of small screws/rivets near the bottom edge
screw_y = -plate_height/2 + 10
screw_start_x = -20
screw_locs = []
for i in range(4):
    screw_locs.append((screw_start_x - i*screw_spacing, screw_y))
    # Mirror on the other side roughly
    screw_locs.append((20 + i*screw_spacing, screw_y))

screws = (
    cq.Workplane("XY")
    .pushPoints(screw_locs)
    .circle(screw_head_dia/2)
    .extrude(screw_head_height)
    .translate((0, 0, plate_thickness/2))
)

result = result.union(screws)

# 8. Cutout for the wheel in the main plate (implied functionality)
# Often these plates have a recess or hole for the wheel mounting
wheel_hole = (
    cq.Workplane("XY")
    .circle(5.0) # Bolt hole
    .extrude(plate_thickness * 2)
    .translate((0, wheel_y_offset, -plate_thickness))
)
result = result.cut(wheel_hole)

# Recess on the back of the plate for the extrusion rail fitment (optional detail)
recess = (
    cq.Workplane("XY")
    .rect(plate_width + 10, 22) # Slightly larger than 20mm extrusion
    .extrude(2.0)
    .translate((0, 0, -plate_thickness/2))
)
result = result.cut(recess)

# Export or display
# cq.exporters.export(result, "mounting_plate.step")