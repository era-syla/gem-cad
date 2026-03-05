import cadquery as cq

# Parametric dimensions for the model
length = 1200.0       # Length of the main board
height = 120.0        # Height of the board (width in the vertical direction)
thickness = 18.0      # Thickness of the board
pin_diameter = 8.0    # Diameter of the dowel pins
pin_length = 30.0     # Length of the pins protruding from the end
pin_spacing = 60.0    # Vertical distance between the centers of the two pins

# Create the main rectangular body
# The board is created centered on the origin
# X-axis: Length, Y-axis: Thickness, Z-axis: Height
board = cq.Workplane("XY").box(length, thickness, height)

# Create the pins on the right-hand face (+X direction)
result = (
    board
    .faces(">X")          # Select the face at the positive X end
    .workplane()          # Create a workplane on this face
    # Define points for the pins: (0, offset) moves along the local Y axis (Global Z/Height)
    .pushPoints([(0, pin_spacing / 2), (0, -pin_spacing / 2)])
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)