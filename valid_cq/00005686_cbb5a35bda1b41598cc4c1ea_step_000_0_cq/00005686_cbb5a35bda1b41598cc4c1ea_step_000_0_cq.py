import cadquery as cq

# Define parameters for the rectangular bar
length = 100.0  # Length of the bar
width = 5.0     # Width of the cross-section
height = 5.0    # Height of the cross-section

# Create the 3D model
# Start with a sketch on the XY plane, creating a rectangle centered on the origin
# Then extrude it to the specified length
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(length)
)

# Alternatively, using the box method for a simple primitive:
# result = cq.Workplane("XY").box(length, width, height)

# Export or visualize the result
# show_object(result)