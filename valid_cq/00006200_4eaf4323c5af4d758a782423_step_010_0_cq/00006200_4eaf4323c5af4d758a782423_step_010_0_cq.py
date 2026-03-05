import cadquery as cq

# Define parametric dimensions
# These dimensions are estimates based on the visual proportions of the image.
# The object appears to be a tall, thin rectangular plate.
height = 100.0  # Total height of the plate
width = 30.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate
# We center it on X and Y to keep the origin in the middle of the base or centroid
result = (
    cq.Workplane("XY")
    .box(width, thickness, height)
)

# Alternatively, if the orientation needs to match the image exactly (standing up facing mostly forward):
# The image shows a face that looks like the "front" face.
# Let's assume the large face is on the XZ plane.
# width (X), height (Z), thickness (Y)
result = cq.Workplane("XY").box(width, thickness, height)