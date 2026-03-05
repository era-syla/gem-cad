import cadquery as cq

# -- Parameters --
arm_length = 110.0      # Total length of the stadium-shaped body
arm_width = 24.0        # Width of the body (and diameter of rounded ends)
arm_thickness = 10.0    # Thickness of the body plate
shaft_diam = 16.0       # Diameter of the large cylindrical handle
shaft_length = 60.0     # Length of the large cylindrical handle
pin_diam = 8.0          # Diameter of the small pins on the back
pin_length = 5.0        # Length of the small pins on the back

# -- Derived Calculations --
# Calculate the distance from the origin to the center of the end radii.
# slot2D is centered at (0,0), total length includes the radii.
# Center offset = (Total Length - Diameter) / 2
radius_center_offset = (arm_length - arm_width) / 2.0

# -- Modeling --

# 1. Main Body: Create the stadium (slot) shape and extrude
result = (
    cq.Workplane("XY")
    .slot2D(arm_length, arm_width)
    .extrude(arm_thickness)
)

# 2. Large Shaft: Extrude from the front face (>Z) at the right end
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(radius_center_offset, 0)])
    .circle(shaft_diam / 2.0)
    .extrude(shaft_length)
)

# 3. Small Pins: Extrude from the back face (<Z) at the left end and offset
# Visual analysis suggests two pins on the back: one at the end, one slightly inward.
back_pin_locations = [
    (-radius_center_offset, 0),                  # Pin at the far left center
    (-radius_center_offset + arm_width * 1.5, 0) # Second pin offset towards center
]

result = (
    result.faces("<Z")
    .workplane()
    .pushPoints(back_pin_locations)
    .circle(pin_diam / 2.0)
    .extrude(pin_length)
)