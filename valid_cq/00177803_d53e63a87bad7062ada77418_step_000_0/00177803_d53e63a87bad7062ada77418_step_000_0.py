import cadquery as cq

# Dimensions
plate_length = 100.0
plate_height = 50.0
plate_thickness = 5.0
pin_diameter = 2.5
pin_length = 5.0
pin_offset_from_bottom = 8.0

# Create the main rectangular body
# Oriented with length along X, thickness along Y, height along Z
# This makes the main large faces parallel to the XZ plane
result = cq.Workplane("XY").box(plate_length, plate_thickness, plate_height)

# Add the pin feature on the left face (min X face)
# The pin is centered on the thickness (Y axis) and offset from the bottom (Z axis)
z_shift = -plate_height / 2 + pin_offset_from_bottom

result = (
    result
    .faces("<X")          # Select the left face
    .workplane()          # Create a working plane on this face
    .center(0, z_shift)   # Shift center: 0 in local x (thickness), z_shift in local y (height)
    .circle(pin_diameter / 2)
    .extrude(pin_length)  # Extrude outwards along the normal
)