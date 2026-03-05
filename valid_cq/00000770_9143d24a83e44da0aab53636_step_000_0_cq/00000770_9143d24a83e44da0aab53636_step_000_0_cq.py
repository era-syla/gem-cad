import cadquery as cq

# --- Parametric Dimensions ---
# Base Plate
plate_length = 100.0
plate_width = 50.0
plate_thickness = 10.0

# Pin (Cylinder)
pin_diameter = 15.0
pin_length = 40.0
pin_chamfer = 1.0

# Mounting Holes (Countersunk)
hole_pattern_x_spacing = 40.0
hole_pattern_y_spacing = 30.0
hole_diameter = 5.0
csk_diameter = 10.0
csk_angle = 82  # Standard countersink angle

# Additional Single Hole on Face
single_hole_offset_x = -35.0 # From center
single_hole_offset_y = -10.0 # From center

# Side Hole (Set screw or similar)
side_hole_diameter = 3.0

# --- Geometry Construction ---

# 1. Create the Base Plate
# We start with a simple box centered on XY plane
base_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add the Pin (Cylinder) on the back
# Select the back face (Z- direction relative to default box orientation)
# We assume the box was created centered, so the back face is at z = -plate_thickness/2
pin = (
    base_plate.faces("<Z")
    .workplane()
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# Apply a chamfer to the end of the pin
result_with_pin = pin.faces("<Z").edges().chamfer(pin_chamfer)

# 3. Add the 4-hole pattern
# These look like countersunk holes.
# We will position them relative to the center of the front face.
result_with_4_holes = (
    result_with_pin.faces(">Z")
    .workplane()
    .rect(hole_pattern_x_spacing, hole_pattern_y_spacing, forConstruction=True)
    .vertices()
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 4. Add the 5th single hole on the face
# Based on the image, there is an extra hole to the left.
result_with_5_holes = (
    result_with_4_holes.faces(">Z")
    .workplane()
    .center(single_hole_offset_x, single_hole_offset_y)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 5. Add the small side hole
# This hole is on the thin side face (left side in the image, -X direction).
# It appears to be a simple through hole or blind hole into the plate thickness.
# We'll make it a through hole into the nearest cavity or a specific depth.
side_hole_depth = 15.0 # Arbitrary depth enough to be visible
result = (
    result_with_5_holes.faces("<X")
    .workplane()
    # Move somewhat down in Y based on visual appearance, or keep centered if intended
    .center(0, -5.0) 
    .hole(side_hole_diameter, side_hole_depth)
)

# Return the final result
if __name__ == "__main__":
    show_object(result)