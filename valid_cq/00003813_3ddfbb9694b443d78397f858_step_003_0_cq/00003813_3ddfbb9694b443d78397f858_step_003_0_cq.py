import cadquery as cq

# Parametric dimensions
height = 100.0         # Total height of the strut
bottom_width = 15.0    # Width at the bottom
bottom_thickness = 10.0 # Thickness at the bottom
top_width = 8.0        # Width at the top
top_thickness = 6.0    # Thickness at the top
hole_diameter = 8.0    # Diameter of the hole at the bottom

# Create the main lofted body
# We define the bottom profile and the top profile, then loft between them.
# The shape looks like a rounded rectangle (stadium shape) or an oval.

# Define the bottom cross-section
bottom_sketch = (
    cq.Sketch()
    .rect(bottom_width, bottom_thickness)
    .vertices()
    .fillet(bottom_thickness / 2.0 - 0.01) # Full round ends approximation
)

# Define the top cross-section
top_sketch = (
    cq.Sketch()
    .rect(top_width, top_thickness)
    .vertices()
    .fillet(top_thickness / 2.0 - 0.01) # Full round ends approximation
)

# Create the solid by lofting
result = (
    cq.Workplane("XY")
    .placeSketch(bottom_sketch, top_sketch.moved(cq.Location(cq.Vector(0, 0, height))))
    .loft()
)

# Add the hole at the bottom
# The hole goes through the wider face (Y-axis direction in this orientation relative to width)
# Looking at the image, the hole is near the base.
hole_center_height = bottom_width / 2.0 # Centered relative to the bottom round part usually

# Create the hole
result = (
    result
    .faces("<Y") # Select the 'front' face (or back depending on orientation)
    .workplane()
    .center(0, -height/2 + hole_center_height) # Move to the correct height relative to the workplane origin
    .hole(hole_diameter)
)

# Optional: Add the top rounded cap feature if the loft flat top isn't sufficient.
# The image shows a fully rounded top. The loft creates a flat top. 
# We need to round the top edge fully.

result = result.edges(">Z").fillet((top_thickness/2.0) - 0.1)

# The bottom also looks fully rounded.
result = result.edges("<Z").fillet((bottom_thickness/2.0) - 0.1)
