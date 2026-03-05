import cadquery as cq

# Parametric dimensions
length = 100.0       # Center-to-center distance
width = 40.0         # Width of the link (also the diameter of the rounded ends)
thickness = 5.0      # Thickness of the plate
hole_diameter = 15.0 # Diameter of the holes

# Create the link geometry
# We start with a 2D sketch on the XY plane.
# The 'slot' method creates the overall stadium shape.
# The dimensions for the slot are usually overall length and width, or center-to-center length.
# In CadQuery's sketch.slot: 
# - First argument is the length (tip-to-tip or center-to-center depending on definition, but usually overall X extent for a horizontal slot)
# - Second argument is width (diameter of the end arcs)
# Alternatively, we can construct it by hulling two circles.

# Using Workplane geometry construction:
# 1. Create a workplane.
# 2. Draw the outline: a rectangle with full circular fillets on the short sides, or a "slot" shape directly.
# 3. Extrude it.
# 4. Cut the holes.

result = (
    cq.Workplane("XY")
    # Method 1: Create a slot shape directly. 
    # The slot2D method creates a slot defined by length and diameter.
    # Note: CadQuery's slot2D length is the total length (end-to-end), not center-to-center.
    # So total_length = length + width
    .slot2D(length + width, width)
    .extrude(thickness)
    # Select the top face to cut holes
    .faces(">Z")
    .workplane()
    # Create two holes at the centers of the rounded ends
    # The centers are at (-length/2, 0) and (length/2, 0) relative to the center of the part
    .pushPoints([(-length / 2, 0), (length / 2, 0)])
    .hole(hole_diameter)
)