import cadquery as cq

# Parametric dimensions
length = 100.0       # Distance between hole centers
width = 20.0         # Width of the link
thickness = 5.0      # Thickness of the material
hole_diameter = 10.0 # Diameter of the mounting holes

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Create the base 2D "stadium" or slot shape
    # slot2D length is the center-to-center distance
    .slot2D(length, width)
    # Extrude to create the 3D solid
    .extrude(thickness)
    # Select the top face to create the holes
    .faces(">Z")
    .workplane()
    # Define the center points for the holes
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    # Cut the holes through the part
    .hole(hole_diameter)
)