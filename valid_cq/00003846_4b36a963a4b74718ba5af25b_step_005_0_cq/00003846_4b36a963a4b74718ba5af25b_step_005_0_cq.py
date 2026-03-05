import cadquery as cq

# Parametric dimensions
# Based on visual estimation, let's assume reasonable units (mm)
length_center_to_center = 40.0  # Distance between the centers of the two holes
width = 20.0                    # Width of the link
thickness = 8.0                 # Thickness of the plate
hole_diameter = 8.0             # Inner diameter of the holes
chamfer_size = 0.5              # Small chamfer around the holes

# The total length is center-to-center + one width (radius on top + radius on bottom)
radius = width / 2.0

# Create the main shape
# We use a sketch approach: a rectangle with full semicircles on top and bottom
# or a hull of two circles.
# Or simply a box with fillets.

# Approach: Sketch a stadium shape (slot) and extrude.
result = (
    cq.Workplane("XY")
    .slot2D(length_center_to_center, width)
    .extrude(thickness)
)

# Create the two holes
# We select the top face, and create two holes at the appropriate locations
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-length_center_to_center / 2.0, 0), (length_center_to_center / 2.0, 0)])
    .hole(hole_diameter)
)

# Add chamfers to the hole edges
# We select the circular edges corresponding to the holes on the top face
result = (
    result.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0)) # Selects the inner hole edges
    .chamfer(chamfer_size)
)

# Optional: Add chamfers to the bottom hole edges as well for symmetry, 
# though only top is clearly visible.
result = (
    result.faces("<Z")
    .edges(cq.selectors.RadiusNthSelector(0))
    .chamfer(chamfer_size)
)