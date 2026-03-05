import cadquery as cq

# Parameters for the geometry
plate_width = 150.0
plate_height = 180.0
plate_thickness = 12.0

pin_diameter = 8.0
pin_height = 15.0
pin_spacing_horizontal = 60.0  # Distance between the left and right columns of pins
pin_spacing_vertical = 25.0    # Distance between the top and bottom pins in a pair
pin_bottom_margin = 35.0       # Distance from the bottom edge to the lower pins

# 1. Create the base plate
# The box is centered at the origin.
# Width is along X, Height along Y, Thickness along Z.
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Calculate positions for the four pins
# Since the box is centered, the bottom edge Y coordinate is -plate_height/2
y_pos_lower = (-plate_height / 2) + pin_bottom_margin
y_pos_upper = y_pos_lower + pin_spacing_vertical

x_pos_left = -pin_spacing_horizontal / 2
x_pos_right = pin_spacing_horizontal / 2

pin_locations = [
    (x_pos_left, y_pos_lower),   # Bottom-left
    (x_pos_left, y_pos_upper),   # Top-left
    (x_pos_right, y_pos_lower),  # Bottom-right
    (x_pos_right, y_pos_upper)   # Top-right
]

# 3. Create the pins on the face of the plate
# Select the top face (positive Z), place the points, draw circles, and extrude
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(pin_locations)
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)