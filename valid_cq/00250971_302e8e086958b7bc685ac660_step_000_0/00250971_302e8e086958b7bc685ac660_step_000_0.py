import cadquery as cq

# --- Parameters ---
# Main body dimensions
case_width = 75.0
case_height = 150.0
case_thickness = 10.0
corner_radius = 8.0

# Camera slot dimensions (top left)
cam_slot_width = 24.0
cam_slot_height = 10.0
cam_pos_x = -16.0
cam_pos_y = 58.0

# Center pocket dimensions
pocket_width = 32.0
pocket_height = 85.0
pocket_depth = 2.0
pocket_pos_y = -10.0

# Side notch dimensions (left side)
notch_height = 30.0
notch_depth = 2.5
notch_pos_y = 25.0

# Side hole dimensions (left side)
hole_diameter = 2.5
hole_pos_y = -8.0

# --- Modeling ---

# 1. Base Body: Rectangular prism with filleted corners
result = (
    cq.Workplane("XY")
    .box(case_width, case_height, case_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Camera Cutout: Slot shape cut through the top left
result = (
    result.faces(">Z")
    .workplane()
    .center(cam_pos_x, cam_pos_y)
    .slot2D(cam_slot_width, cam_slot_height)
    .cutThruAll()
)

# 3. Center Pocket: Rectangular recess on the back
result = (
    result.faces(">Z")
    .workplane()
    .center(0, pocket_pos_y)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

# 4. Side Notch: Cutout on the left edge (viewed from back)
# Selecting the -X face. Local X is typically Global Y, Local Y is Global Z.
result = (
    result.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .center(notch_pos_y, 0)
    .rect(notch_height, case_thickness * 1.5)  # Height > thickness to ensure full edge cut
    .cutBlind(-notch_depth)
)

# 5. Side Hole: Small hole below the notch on the left edge
result = (
    result.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .center(hole_pos_y, 0)
    .circle(hole_diameter / 2.0)
    .cutBlind(-5.0)  # Cut 5mm into the case
)