import cadquery as cq

# Define parametric variables
width = 100.0   # Distance across flats or overall width
thickness = 5.0 # Thickness of the plate

# Create the octagonal plate
# We can create a polygon with 8 sides.
# circumscribed=True implies 'width' is the outer diameter (point-to-point)
# circumscribed=False implies 'width' is the inner diameter (flat-to-flat)
# For an octagon, usually flat-to-flat is the main spec, but let's assume a reasonable radius.
# Using polygon method with 8 sides.
result = cq.Workplane("XY").polygon(nSides=8, diameter=width).extrude(thickness)
