import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 60.0    # Width of the plate
thickness = 5.0 # Thickness of the plate
radius = 5.0    # Fillet radius for the corners

# Create the base plate with rounded corners
# We draw a rectangle, extrude it, and then fillet the vertical edges
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .edges("|Z") # Select edges parallel to the Z axis (the corners)
    .fillet(radius)
)