import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0       # Center-to-center distance between end holes
width = 10.0         # Width of the link
thickness = 5.0      # Thickness of the link
hole_diameter = 4.0  # Diameter of the holes at the ends
slot_length = 70.0   # Length of the central recess slot
slot_width = 4.0     # Width of the central recess slot
slot_depth = 2.0     # Depth of the central recess slot

# --- Modeling ---

# 1. Create the base "racetrack" shape (a rectangle with rounded ends)
# We can do this by sketching a slot and extruding it.
# The `slot` method in CadQuery creates this shape easily.
# The slot length usually refers to the overall length or center-to-center. 
# Here we'll construct it using a center-to-center length plus the radius on each side.
radius = width / 2.0
overall_length = length + 2 * radius

# Create the main body
result = (
    cq.Workplane("XY")
    .slot2D(length, width)  # Creates a 2D slot shape centered at origin with center-to-center length
    .extrude(thickness)
)

# 2. Cut the holes at both ends
# We select the top face, then push points at the hole locations (-length/2, 0) and (length/2, 0)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .hole(hole_diameter)
)

# 3. Cut the central recess slot
# This is a shallower slot running along the center.
# We sketch a smaller slot on the top face and make a cut.
result = (
    result.faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Return the final result
if "show_object" in locals():
    show_object(result)