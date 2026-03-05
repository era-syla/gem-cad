import cadquery as cq

# Parameters for the model
plate_width = 50.0
plate_height = 95.0
plate_thickness = 4.0
fillet_radius = 8.0

# Parameters for the top slot
slot_width = 24.0
slot_height = 10.0
# Distance from the center of the plate to the center of the slot
slot_center_y_offset = 35.0 

# Parameters for the back block protrusion
back_block_width = 42.0
back_block_height = 65.0
back_block_depth = 6.0
back_block_y_offset = -8.0

# 1. Create the main body plate
# We create a box centered at the origin
main_body = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Apply fillets to the four corners of the plate
# We select edges parallel to the Z axis
main_body = main_body.edges("|Z").fillet(fillet_radius)

# 3. Cut the rectangular slot near the top
# We select the top face (positive Z), create a workplane, move to position, and cut
main_body = (
    main_body.faces(">Z")
    .workplane()
    .center(0, slot_center_y_offset)
    .rect(slot_width, slot_height)
    .cutBlind(-plate_thickness)
)

# 4. Add the mounting block on the back
# We select the bottom face (negative Z), create a workplane, and extrude outwards
# Note: Extruding from a face typically goes along the normal (away from the solid)
main_body = (
    main_body.faces("<Z")
    .workplane()
    .center(0, back_block_y_offset)
    .rect(back_block_width, back_block_height)
    .extrude(back_block_depth)
)

# 5. (Optional) Logo placeholder
# The complex organic Browning logo cannot be procedurally generated 
# without external vector data. We can add a simple text placeholder instead.
# To keep the geometry clean as per the prompt's request for "this model", 
# we leave the surface plain, but the code structure allows adding it here.
# main_body = main_body.faces(">Z").workplane().text("LOGO", 10, -0.5)

result = main_body