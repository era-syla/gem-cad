import cadquery as cq

# Parametric dimensions
height = 100.0  # Height of the plate
width = 100.0   # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create the 3D model
# We create a box centered on X and Y, sitting on the Z plane (or centered on Z)
# Based on the image, it looks like a simple rectangular prism.
result = cq.Workplane("XY").box(width, height, thickness)

# If the intention is to have it "standing up" like in the image relative to a specific view,
# the orientation doesn't strictly matter for the geometry itself, but we can orient it 
# to match the typical "Front" view.
# The code above creates a flat plate. To make it stand up like a wall:
# result = cq.Workplane("XZ").box(width, thickness, height) 
# However, a simple box is the most robust interpretation.

# Let's stick to the simplest interpretation: a box.
# If specific orientation is needed to match the visual "standing up":
# Let's create it on the XZ plane and extrude along Y.
result = cq.Workplane("XY").box(width, thickness, height)