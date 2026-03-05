import cadquery as cq

# Parameter definitions based on visual estimation of the image
plate_length = 200.0
plate_width = 80.0
plate_thickness = 4.0

pin_diameter = 4.0
pin_height = 4.0
edge_margin = 10.0

# Calculate coordinate offsets
x_offset = (plate_length / 2.0) - edge_margin
y_front = -(plate_width / 2.0) + edge_margin
y_back = (plate_width / 2.0) - edge_margin

# Define pin locations
# Front row has 2 pins at the corners
# Back row has 4 pins distributed along the edge (2 corners + 2 intermediate)
# Calculating spacing for the back row to be equidistant
back_row_span = 2 * x_offset
back_pin_spacing = back_row_span / 3.0

points = [
    # Front Row (Left, Right)
    (-x_offset, y_front),
    (x_offset, y_front),
    
    # Back Row (Left, Mid-Left, Mid-Right, Right)
    (-x_offset, y_back),
    (-x_offset + back_pin_spacing, y_back),
    (x_offset - back_pin_spacing, y_back),
    (x_offset, y_back)
]

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Add the pins to the top surface
result = (result.faces(">Z")
          .workplane()
          .pushPoints(points)
          .circle(pin_diameter / 2.0)
          .extrude(pin_height))