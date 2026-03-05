import cadquery as cq

# Parametric dimensions
plate_width = 100.0
plate_height = 110.0
plate_thickness = 4.0

pin_diameter = 3.5
pin_height = 6.0
pin_x_spacing = 28.0
pin_y_spacing = 12.0
pin_y_offset = -32.0  # Vertical offset from the center of the plate

# Create the base plate
base_plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Define the positions for the 4 pins
pin_locations = [
    (-pin_x_spacing / 2, pin_y_offset - pin_y_spacing / 2),
    (-pin_x_spacing / 2, pin_y_offset + pin_y_spacing / 2),
    (pin_x_spacing / 2, pin_y_offset - pin_y_spacing / 2),
    (pin_x_spacing / 2, pin_y_offset + pin_y_spacing / 2)
]

# Extrude the pins from the front face
result = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(pin_locations)
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)