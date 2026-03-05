import cadquery as cq

# Parametric dimensions
# These values are estimated from the visual proportions of the image
length = 100.0       # Total length of the slot
width = 20.0         # Total width of the slot (outer diameter of the semicircles)
thickness = 2.0      # Wall thickness of the loop
height = 8.0         # Height of the extrusion

# Derived dimensions
radius_outer = width / 2.0
radius_inner = radius_outer - thickness
center_distance = length - width  # Distance between the centers of the two arcs

# Create the sketch
# We will create the outer slot shape and cut the inner slot shape from it
# Alternatively, we can sketch two profiles and extrude, or sweep a profile.
# The simplest robust way in CadQuery is to draw the 2D profile of the wall and extrude.

# Method: Create a sketch on the XY plane.
# The sketch will consist of two slot shapes (racetracks) subtracted from each other.

result = (
    cq.Workplane("XY")
    .sketch()
    # Outer profile
    .slot(length, width, angle=0, mode='a') 
    # Inner profile (subtracted)
    .slot(length - 2*thickness, width - 2*thickness, angle=0, mode='s')
    .finalize()
    .extrude(height)
)
