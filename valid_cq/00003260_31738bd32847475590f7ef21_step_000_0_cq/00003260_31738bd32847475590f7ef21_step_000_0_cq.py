import cadquery as cq

# Define parametric dimensions
box_width = 100.0   # Width of the main rectangular body
box_depth = 60.0    # Depth of the main rectangular body
box_height = 40.0   # Height of the main rectangular body

pin_diameter = 5.0  # Diameter of the cylindrical pins
pin_length = 10.0   # Length of the cylindrical pins sticking out
pin_offset_x = 40.0 # Distance from center to pin in X direction
pin_offset_z = -15.0 # Distance from center to pin in Z direction (relative to face center)

# Create the main rectangular body
# Using centered=True creates the box centered at (0,0,0)
base = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Create the pins on the front face
# We select the front face (positive Y direction in default orientation if created on XY plane? 
# Actually, box creates faces aligned with axes.
# Let's target the face on the positive Y axis (Front)
result = (
    base
    .faces(">Y")            # Select the front face (positive Y)
    .workplane()            # Create a workplane on this face
    .pushPoints([           # Define the locations for the two pins
        (-pin_offset_x, pin_offset_z), 
        (pin_offset_x, pin_offset_z)
    ])
    .circle(pin_diameter / 2.0) # Draw circles for the pins
    .extrude(pin_length)    # Extrude the circles to form the pins
)

# Alternatively, if we want to be very specific about relative positioning:
# The box is centered.
# Width is X, Depth is Y, Height is Z.
# Let's assume the pins are on one of the faces defined by Width and Height (XZ plane), i.e., Front/Back.
# In standard CAD view, Front is usually XZ plane (looking down Y).
# Let's re-orient to match the visual "Front" being the face with pins.

# Redefining for a more intuitive orientation matching the image:
# Box width (X), Depth (Y), Height (Z).
# Image shows a face with pins. Let's assume that's the "Front" face in the Y- direction or similar.
# Let's stick to the previous logic but refine coordinates.

# Create main block
main_body = cq.Workplane("XY").box(box_width, box_depth, box_height)

# The pins are on one of the side faces. Let's put them on the +Y face.
# Center of +Y face is (0, box_depth/2, 0).
# Pins are near the bottom corners.
# X coordinates: +/- (box_width/2 - margin)
# Z coordinates: - (box_height/2 - margin)

pin_x_spacing = box_width * 0.8  # Distance between pins
pin_z_location = -box_height * 0.35 # Height relative to center

result = (
    main_body
    .faces(">Y") # Select the face in the positive Y direction
    .workplane()
    .pushPoints([
        (-pin_x_spacing/2, pin_z_location),
        (pin_x_spacing/2, pin_z_location)
    ])
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)