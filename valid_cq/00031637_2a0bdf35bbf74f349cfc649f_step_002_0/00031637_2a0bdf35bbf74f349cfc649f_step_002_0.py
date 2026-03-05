import cadquery as cq

# Define parametric dimensions for the model
length = 60.0       # Total length of the block (X-axis)
width = 40.0        # Total width/depth of the block (Y-axis)
height = 30.0       # Total height of the block (Z-axis)
step_length = 20.0  # Length of the lower step section
step_height = 15.0  # Height of the lower step section

# Create the 3D model
# We draw the L-shaped profile on the XZ plane (front view) 
# and extrude it along the Y axis (width).
result = (
    cq.Workplane("XZ")
    .lineTo(0, height)                       # Draw vertical line up
    .lineTo(length - step_length, height)    # Draw top horizontal line
    .lineTo(length - step_length, step_height) # Draw vertical line down to step
    .lineTo(length, step_height)             # Draw horizontal step line
    .lineTo(length, 0)                       # Draw vertical line down to bottom
    .close()                                 # Close the profile back to (0,0)
    .extrude(width)                          # Extrude to create the solid
)