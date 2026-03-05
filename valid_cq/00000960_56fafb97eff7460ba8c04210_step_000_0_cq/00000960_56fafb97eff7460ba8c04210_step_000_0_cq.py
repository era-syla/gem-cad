import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length in the X direction
width = 80.0     # Total width in the Y direction
thickness = 2.0  # Thickness of the plate

# Cutout dimensions
cutout_length = 40.0
cutout_width = 30.0

# Create the base plate using a sketch approach
# We start with a rectangle and cut out a corner to form the L-shape/T-shape variation
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .moveTo(length / 2, width / 2)  # Move to the top-right corner
    .rect(cutout_length * 2, cutout_width * 2)  # Create a rectangle centered at the corner to cut
    .cutThruAll()
)

# Alternative method: constructing the points explicitly for a polygon extrusion
# This can be more robust for specific non-symmetrical shapes
# Let's interpret the shape as an L-shape with a specific block removed from a corner.
# Or constructing it as two rectangles unioned together.

# Let's re-create it to be exactly like the visual: a T-shape where one side is missing, 
# effectively an L-shape, or a rectangle with a notch.
# Looking closely at the image, it's a large rectangle with a rectangular notch in the top right.

# Re-defining using a more direct parametric sketch approach
result = (
    cq.Workplane("XY")
    .sketch()
    .push([
        (0, 0), # Center
    ])
    .rect(length, width) # Base rectangle
    .push([
        (length/2, width/2) # Top right corner
    ])
    .rect(cutout_length*2, cutout_width*2, mode='s') # Subtract corner
    .finalize()
    .extrude(thickness)
)