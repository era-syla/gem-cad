import cadquery as cq

# -- Parametric Dimensions --
plate_width = 120.0
plate_height = 150.0
plate_thickness = 6.0

pin_diameter = 5.0
pin_length = 8.0
pin_horizontal_spacing = 50.0  # Distance between the left and right pin pairs
pin_vertical_spacing = 20.0    # Vertical distance between pins in a pair
pin_offset_from_bottom = 25.0  # Distance from bottom edge to the center of the lowest pins

# -- Coordinate Calculations --
# The plate is centered at (0,0), so the bottom edge is at y = -plate_height/2
y_lower = -plate_height / 2 + pin_offset_from_bottom
y_upper = y_lower + pin_vertical_spacing

x_left = -pin_horizontal_spacing / 2
x_right = pin_horizontal_spacing / 2

# Define the centers for the four pins
pin_centers = [
    (x_left, y_lower),
    (x_left, y_upper),
    (x_right, y_lower),
    (x_right, y_upper)
]

# -- Model Generation --
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)  # Create base plate centered at origin
    .faces(">Z")                                      # Select the top face (Z direction)
    .workplane()                                      # Create a workplane on the selected face
    .pushPoints(pin_centers)                          # Move to pin locations
    .circle(pin_diameter / 2)                         # Sketch circles for pins
    .extrude(pin_length)                              # Extrude pins outwards
)