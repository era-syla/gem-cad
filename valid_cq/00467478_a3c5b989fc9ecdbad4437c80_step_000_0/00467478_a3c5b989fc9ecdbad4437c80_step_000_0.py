import cadquery as cq

# Parametric dimensions
plate_length = 120.0
plate_width = 50.0
plate_thickness = 4.0
cylinder_diameter = 25.0
cylinder_height = 20.0
slot_length = 40.0
slot_width = 5.0

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # 1. Create the base rectangular plate
    .box(plate_length, plate_width, plate_thickness)
    
    # 2. Create the cylindrical boss on the bottom face
    .faces("<Z").workplane()
    .circle(cylinder_diameter / 2.0)
    .extrude(cylinder_height)
    
    # 3. Cut the slot through the center, from the top face
    .faces(">Z").workplane()
    .slot2D(slot_length, slot_width)
    .cutBlind(-(plate_thickness + cylinder_height))
)