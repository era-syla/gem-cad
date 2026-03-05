import cadquery as cq

# --- Parametric Dimensions ---
# Base Plate
plate_width = 30.0
plate_thickness = 10.0
plate_height = 60.0

# Large Cylinder (Front)
cyl_od = 28.0
cyl_id = 26.0  # Thin wall
cyl_length = 25.0
cyl_vertical_offset = 10.0  # Shift upwards from center

# Top Pin
pin_diameter = 6.0
pin_height = 30.0
# Groove detail on pin
groove_from_top = 4.0
groove_width = 1.0
groove_depth = 0.5

# --- Modeling ---

# 1. Create the Base Plate
# Centered at origin, thickness along Y, height along Z
result = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)

# 2. Add Large Cylinder to Front Face
# Select the front face (>Y), move center up, draw circle, and extrude
result = (
    result.faces(">Y").workplane()
    .center(0, cyl_vertical_offset)
    .circle(cyl_od / 2.0)
    .extrude(cyl_length)
)

# 3. Create Hole in Large Cylinder
# Select the face at the end of the cylinder, draw inner circle, cut back
result = (
    result.faces(">Y").workplane()
    .circle(cyl_id / 2.0)
    .cutBlind(-cyl_length)
)

# 4. Add Top Pin
# Select top face (>Z), center is automatic, draw circle, extrude
result = (
    result.faces(">Z").workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)

# 5. Create Groove Detail on Pin
# Calculate the absolute Z height for the groove
# Plate top is at plate_height/2
pin_top_z = (plate_height / 2.0) + pin_height
groove_z_center = pin_top_z - groove_from_top

# Create a ring-shaped cutter tool to subtract the groove
cutter = (
    cq.Workplane("XY")
    .workplane(offset=groove_z_center - (groove_width / 2.0))
    .circle(pin_diameter * 2.0)            # Outer radius (clearance)
    .circle((pin_diameter / 2.0) - groove_depth) # Inner radius (cut depth)
    .extrude(groove_width)
)

# Apply the cut to create the groove
result = result.cut(cutter)