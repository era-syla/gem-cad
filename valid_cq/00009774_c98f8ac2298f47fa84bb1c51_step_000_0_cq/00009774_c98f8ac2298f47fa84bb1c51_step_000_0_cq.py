import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate (looks square in the image)
thickness = 10.0 # Thickness of the plate

# Create the 3D model
# We start with a workplane on the XY plane
# Draw a rectangle centered at the origin
# Extrude it by the thickness
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# Alternatively using the sketch and extrude method for clarity:
# result = (
#     cq.Workplane("XY")
#     .rect(length, width)
#     .extrude(thickness)
# )