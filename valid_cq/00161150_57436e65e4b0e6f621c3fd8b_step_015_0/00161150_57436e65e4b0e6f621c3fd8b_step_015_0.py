import cadquery as cq

# Parametric dimensions
plate_length = 30.0
plate_width = 12.0
plate_thickness = 2.0
gap = 10.0
count = 3

# Calculate the pitch (center-to-center distance)
pitch = plate_length + gap

# Create the 3D model
# Uses a rectangular array (rarray) to position 3 rectangles along the X-axis
# and extrudes them simultaneously to create separate solid bodies.
result = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=pitch, 
        ySpacing=1,      # Not used since yCount is 1
        xCount=count, 
        yCount=1, 
        center=True      # Centers the array at the origin
    )
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)