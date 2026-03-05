import cadquery as cq

# Model parameters
length = 100.0       # Total length of the part
width = 60.0         # Total width of the part
base_height = 15.0   # Height of the thinner base section
step_height = 3.0    # Additional height of the stepped section
step_ratio = 0.6     # Proportion of the length covered by the step

# derived dimensions
step_length = length * step_ratio
# Calculate offset to align the step with the right edge (+X)
# Center of the base is (0,0). Right edge is at x = length/2.
# Center of the step rectangle needs to be positioned such that its right edge aligns with length/2.
step_center_offset_x = (length / 2) - (step_length / 2)

# Create the base block
result = cq.Workplane("XY").box(length, width, base_height)

# Add the raised step feature
result = (
    result
    .faces(">Z")                         # Select the top face
    .workplane()                         # Create a workplane on the top face
    .center(step_center_offset_x, 0)     # Move local origin to the center of the step
    .rect(step_length, width)            # Sketch the rectangle for the step
    .extrude(step_height)                # Extrude upwards to add material
)