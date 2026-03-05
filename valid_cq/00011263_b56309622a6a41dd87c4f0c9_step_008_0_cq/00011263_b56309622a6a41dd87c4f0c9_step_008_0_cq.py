import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 80.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the 3D model
# We create a simple box centered on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)

# If centering on Z=0 is preferred (so it sits on the plane), we can translate it up
# or just draw it from a face. The default box centers it on all axes.
# To make it look like the image (sitting on a plane), we can adjust the center point.
# result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))