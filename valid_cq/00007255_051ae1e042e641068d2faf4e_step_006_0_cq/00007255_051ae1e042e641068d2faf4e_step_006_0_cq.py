import cadquery as cq

# Parametric dimensions
width = 100.0   # Width of the plate
height = 80.0   # Height of the plate
thickness = 5.0 # Thickness of the plate

# Create the solid geometry
# We create a simple box centered in X and Y, but with Z starting from 0 (or centered, depending on preference)
# Based on the image, it's just a rectangular prism.
result = cq.Workplane("XY").box(width, height, thickness)

# Optional: To match the orientation in the image (standing up), we could rotate it
# or define it on the XZ plane. The image shows a perspective view.
# Let's define it on the Front plane (XZ) to make it "stand up" like a wall.
result = cq.Workplane("XZ").box(width, height, thickness)