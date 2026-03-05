import cadquery as cq

# --- Parametric Dimensions ---
# Main enclosure dimensions
box_length = 80.0
box_height = 50.0
box_width = 15.0
wall_thickness = 1.5

# Connector Cutouts (Top Face)
# Small cutout (Left)
cutout1_w = 6.0
cutout1_h = 6.0
cutout1_pos_x = -box_length/2 + 15.0

# Large cutout (Middle-Left)
cutout2_w = 10.0
cutout2_h = 8.0
cutout2_pos_x = -box_length/2 + 30.0

# Cylindrical Boss/Connector (Top Face)
boss_dia = 5.0
boss_height = 6.0
boss_pos_x = -box_length/2 + 45.0
# Add some rings/grooves to the boss to match the image
groove_depth = 0.5
groove_width = 0.5
num_grooves = 3

# Side Slit/Connector (Left Face)
slit_width = 2.0
slit_height = 25.0
slit_depth = 2.0

# Separate Plate (floating in the image)
plate_length = 20.0
plate_height = 8.0
plate_thickness = 1.0
plate_offset_x = 40.0 # Distance away from the main body
plate_offset_y = 30.0 # Height relative to center

# --- Modeling ---

# 1. Create the Main Body
# Using a simple box as the base
main_body = cq.Workplane("XY").box(box_length, box_width, box_height)

# 2. Add Top Features (Connectors/Cutouts)
# We work on the top face (positive Z)
top_face = main_body.faces(">Z").workplane()

# Cutout 1
main_body = top_face.center(cutout1_pos_x, 0).rect(cutout1_w, cutout1_w).cutBlind(-5.0)

# Reset and move to Cutout 2 position
# Note: center() is relative to the previous workplane origin, so we reset or calculate carefully.
# It's often safer to re-select the face to reset the local origin.
top_face = main_body.faces(">Z").workplane()
main_body = top_face.center(cutout2_pos_x, 0).rect(cutout2_w, cutout2_w).cutBlind(-5.0)

# 3. Add the Cylindrical Boss
top_face = main_body.faces(">Z").workplane()
boss = top_face.center(boss_pos_x, 0).circle(boss_dia/2).extrude(boss_height)

# Add grooves to the boss
for i in range(num_grooves):
    z_pos = box_height/2 + boss_height - (i + 1) * (groove_width + 1.0)
    # Create a cutting tool for the groove
    groove_cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(boss_pos_x, 0)
        .circle(boss_dia/2)
        .circle(boss_dia/2 - groove_depth)
        .extrude(groove_width)
    )
    boss = boss.cut(groove_cutter)

main_body = main_body.union(boss)

# 4. Add Side Feature (Slit on the left face)
# Select the left face (-X)
left_face = main_body.faces("<X").workplane()
# Create a rectangular pocket
main_body = left_face.rect(slit_depth, slit_height).cutBlind(-2.0)
# Add small holes/contacts inside the slit to simulate pins
pin_dia = 0.8
pin_spacing = 2.0
num_pins = 8
start_z = -slit_height/2 + 3.0

# We need to orient correctly on the left face for the pins
left_face_pins = main_body.faces("<X").workplane(centerOption="CenterOfMass")
for i in range(num_pins):
    # Adjust Y in local coords (which is Z in global)
    y_loc = -slit_height/2 + (i * pin_spacing) + (slit_height - ((num_pins-1)*pin_spacing))/2 
    main_body = left_face_pins.center(0, 0).moveTo(0, y_loc).circle(pin_dia/2).cutBlind(-2.5)


# 5. Create the Floating Plate
floating_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_thickness, plate_height)
    .translate((box_length/2 + plate_offset_x, 0, plate_offset_y))
)

# 6. Combine everything
result = main_body.union(floating_plate)