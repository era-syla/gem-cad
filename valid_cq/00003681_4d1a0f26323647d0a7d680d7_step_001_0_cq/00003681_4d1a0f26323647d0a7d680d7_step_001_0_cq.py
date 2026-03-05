import cadquery as cq

# Parametric dimensions
width = 100.0   # Length of the plate
height = 50.0   # Height of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate
# We center it on X and Y, but not Z, to make positioning intuitive
result = cq.Workplane("XY").box(width, thickness, height)

# Alternatively, if "XY" implies flat on the ground and we want it vertical like the image:
# result = cq.Workplane("XY").box(width, height, thickness)
# But the image shows a vertical orientation, often represented as length along X and height along Z.
# Let's adjust the workplane to match the visual orientation better.
# A box created on "XY" typically extrudes in Z.
# To match the image:
#   - Long edge horizontal (X)
#   - Short edge vertical (Z)
#   - Thin edge depth (Y)

result = cq.Workplane("XY").box(width, thickness, height)