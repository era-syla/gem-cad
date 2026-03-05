import cadquery as cq

# Parametric dimensions
length = 100.0   # Center-to-center distance between holes
width = 20.0     # Width of the link
thickness = 10.0 # Thickness of the link
hole_dia = 10.0  # Diameter of the holes at the ends

# Create the basic shape
# We start with a sketch on the XY plane
# 1. Create a rectangle for the main body
# 2. Fillet the corners to create the rounded ends, or use a "slot" shape logic
# 3. Cut the holes

result = (
    cq.Workplane("XY")
    # Draw the main slot shape. The slot2D function creates a stadium/slot shape 
    # defined by the length (center-to-center) and diameter (width).
    .slot2D(length, width)
    # Extrude to create the 3D solid
    .extrude(thickness)
    # Select the top face to cut holes
    .faces(">Z")
    .workplane()
    # Create points at the centers of the two ends
    # The slot is centered at (0,0), so the ends are at (-length/2, 0) and (length/2, 0)
    .pushPoints([(-length/2, 0), (length/2, 0)])
    # Cut the holes
    .hole(hole_dia)
)