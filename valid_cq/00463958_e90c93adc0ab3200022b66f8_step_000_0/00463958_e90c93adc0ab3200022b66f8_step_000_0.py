import cadquery as cq

# --- Parameters ---
# Overall dimensions of the plate
plate_width = 300.0
plate_height = 80.0
plate_thickness = 4.0

# Margins defining the central cutout
# The bottom margin is larger to accommodate the mounting holes
margin_top = 10.0
margin_bottom = 20.0
margin_side = 15.0

# Mounting hole parameters
hole_diameter = 4.0
hole_offset_from_bottom = 10.0
hole_offset_from_side = 10.0

# --- Calculations ---
# Calculate cutout dimensions
cutout_width = plate_width - (2 * margin_side)
cutout_height = plate_height - (margin_top + margin_bottom)

# Calculate the vertical center of the cutout relative to the plate center
# Plate Y range is [-plate_height/2, plate_height/2]
# Cutout Top Y = plate_height/2 - margin_top
# Cutout Bottom Y = -plate_height/2 + margin_bottom
cutout_center_y = ((plate_height / 2 - margin_top) + (-plate_height / 2 + margin_bottom)) / 2

# Calculate hole positions relative to plate center
hole_y = -plate_height / 2 + hole_offset_from_bottom
hole_x_dist = plate_width / 2 - hole_offset_from_side

# --- Modeling ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the central rectangular window
result = (
    result.faces(">Z")
    .workplane()
    .center(0, cutout_center_y)
    .rect(cutout_width, cutout_height)
    .cutBlind(-plate_thickness)
)

# 3. Create the three mounting holes (Left, Center, Right)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_x_dist, hole_y), # Left hole
        (0, hole_y),            # Center hole
        (hole_x_dist, hole_y)   # Right hole
    ])
    .circle(hole_diameter / 2)
    .cutBlind(-plate_thickness)
)