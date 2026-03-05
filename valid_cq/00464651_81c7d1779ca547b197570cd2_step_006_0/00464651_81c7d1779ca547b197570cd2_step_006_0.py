import cadquery as cq

# Parametric dimensions for the component (Transistor-like package)
body_width = 4.5      # X dimension
body_thickness = 2.5  # Y dimension
body_height = 6.0     # Z dimension

pin_length = 12.0
pin_size = 0.5        # Square cross-section side length
pin_pitch = 1.27      # Distance between pin centers

# Create the main body block
# The box is centered at the origin
main_body = cq.Workplane("XY").box(body_width, body_thickness, body_height)

# Create the pins
# 1. Select the bottom face of the body (lowest Z face)
# 2. Create a workplane on that face (normal points downwards)
# 3. Define the center points for the three pins
# 4. Draw the square profiles
# 5. Extrude the profiles to create the legs
result = (
    main_body
    .faces("<Z")
    .workplane()
    .pushPoints([
        (-pin_pitch, 0),  # Left pin
        (0, 0),           # Center pin
        (pin_pitch, 0)    # Right pin
    ])
    .rect(pin_size, pin_size)
    .extrude(pin_length)
)