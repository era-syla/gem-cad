import cadquery as cq

# Dimensions
length = 100.0
width = 40.0
height = 40.0
notch_width = 15.0   # Width of the cutout/step
notch_depth = 20.0   # Depth of the cutout from the top

# Derived dimension
shelf_height = height - notch_depth

# Create the L-shaped profile on the YZ plane and extrude along X
# The profile defines the cross-section with a step removed from the top-left
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                      # Bottom-left corner
        (width, 0),                  # Bottom-right corner
        (width, height),             # Top-right corner
        (notch_width, height),       # Top edge of the vertical wall
        (notch_width, shelf_height), # Inner corner of the step
        (0, shelf_height)            # Top edge of the lower shelf
    ])
    .close()
    .extrude(length)
)