import cadquery as cq

# --- Parametric Dimensions ---
# Main enclosure dimensions
box_width = 90.0
box_depth = 130.0
box_height = 35.0

# LED indicator dimensions
led_diameter = 4.0
led_spacing = 8.0
led_depth = 1.0  # Shallow cut for visual representation
# Position relative to the center of the front face
led_y_pos = -10.0 
led_x_start = -30.0

# Rectangular port/switch dimensions
port_width = 4.0
port_height = 8.0
port_depth = 1.0
port_x_pos = 35.0
port_y_pos = -10.0

# --- Modeling ---

# 1. Create the main body (Block)
# box() creates a centered box by default
main_body = cq.Workplane("XY").box(box_width, box_depth, box_height)

# 2. Create the front features
# We select the face with minimum Y coordinate to be the "front"
# On this face workplane:
#   - Local X corresponds to Global X (Width)
#   - Local Y corresponds to Global Z (Height)
#   - (0,0) is the center of the face

# Define points for the three LEDs
led_centers = [
    (led_x_start, led_y_pos),
    (led_x_start + led_spacing, led_y_pos),
    (led_x_start + 2 * led_spacing, led_y_pos)
]

# Apply features to the main body
result = (
    main_body
    # Select front face
    .faces("<Y").workplane()
    
    # Create LED holes
    .pushPoints(led_centers)
    .circle(led_diameter / 2.0)
    .cutBlind(-led_depth)
    
    # Create Rectangular port (requires a new workplane reference on the same face 
    # or continuing from the cut object, but resetting the workplane center is safer)
    .faces("<Y").workplane()
    .center(port_x_pos, port_y_pos)
    .rect(port_width, port_height)
    .cutBlind(-port_depth)
)