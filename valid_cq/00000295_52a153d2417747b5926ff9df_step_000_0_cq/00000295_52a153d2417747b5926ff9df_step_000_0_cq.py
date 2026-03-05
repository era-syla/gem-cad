import cadquery as cq

# Define parameters for the model
plate_length = 100.0   # Length of the main rectangular body
plate_width = 80.0     # Width of the main rectangular body
plate_thickness = 5.0  # Thickness of the plate

tab_length = 10.0      # How far the tabs stick out
tab_width = 30.0       # The width of the tabs along the plate's edge

# Create the main body
# We start with a base rectangle centered on the XY plane
main_body = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the tabs
# The tabs are located on the left and right sides (along the Y-axis width, positioned on X)
# We can create a single long box that represents both tabs if it spans the entire length + 2*tab_length
# and intersect/union it, or just union two separate boxes.

# Method 1: Create a second box representing the tabs and union it.
# The tabs box will be longer in the X dimension (plate_length + 2*tab_length)
# and narrower in the Y dimension (tab_width).
tabs = cq.Workplane("XY").box(plate_length + 2 * tab_length, tab_width, plate_thickness)

# Combine the main body and the tabs
result = main_body.union(tabs)

# Export or visualize the result
# show_object(result)