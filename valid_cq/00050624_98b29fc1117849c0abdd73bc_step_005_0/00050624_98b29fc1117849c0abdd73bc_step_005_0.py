import cadquery as cq

# Dimensions
length = 150.0
width = 100.0
thickness = 10.0
hole_size = 10.0
hole_spacing = 50.0  # Distance between the centers of the two holes

# Create the model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)  # Create base plate centered at origin
    .faces(">Z")                    # Select the top face
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])  # Define locations for holes
    .rect(hole_size, hole_size)     # Sketch square profile at points
    .cutThruAll()                   # Cut through the plate
)