import cadquery as cq

# Define parameters for the rectangular plate
length = 200.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the 3D model
# We start with a workplane (usually XY)
# We draw a rectangle centered at the origin
# We extrude it by the thickness
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
)

# If this were part of a larger script, you might want to export it or show it
# but the prompt specifically asks for the 'result' variable.