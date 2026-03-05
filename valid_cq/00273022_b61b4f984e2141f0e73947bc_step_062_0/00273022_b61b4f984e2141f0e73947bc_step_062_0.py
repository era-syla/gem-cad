import cadquery as cq
import math

# --- Parameters ---
# Dimensions based on visual estimation of the provided image
# Assuming roughly M6 scale properties
shaft_diameter = 6.0
shaft_length = 30.0
head_diameter = 12.0
head_height = 8.0
hex_across_flats = 5.0
hex_depth = 4.0
knurl_count = 30        # Number of ridges on the head
knurl_depth = 0.5       # Depth of the knurl cut
knurl_width = 0.8       # Width of the knurl cut

# --- Calculations ---
# Calculate the circumscribed diameter of the hexagon from the across-flats dimension
# Formula: d = s / (sqrt(3)/2)
hex_circum_diameter = hex_across_flats / (math.sqrt(3) / 2)

# --- Modeling ---

# 1. Create the Head Cylinder
# We start with the origin at the center of the top face of the screw head
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(-head_height)

# 2. Create the Shaft
# Select the bottom face of the head and extrude the shaft
result = (
    result.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Add Chamfers
# Chamfer the top edge of the head (before cutting features to ensure clean edge selection)
result = result.faces(">Z").edges().chamfer(0.5)
# Chamfer the tip of the shaft
result = result.faces("<Z").edges().chamfer(0.5)

# 4. Create the Hex Socket
# Cut a hexagonal recess into the top face
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
)

# 5. Create the Knurling / Ridges
# Cut vertical grooves around the perimeter of the head
# We use a polar array to position a rectangular cutter around the edge
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(head_diameter / 2.0, 0, 360, knurl_count)
    # The rectangle is defined in local coordinates at each polar point.
    # X is radial, Y is tangential.
    # We make the radial width (X) enough to cross the boundary depth-wise.
    # We make the tangential height (Y) the desired groove width.
    .rect(knurl_depth * 2, knurl_width)
    .cutBlind(-head_height)
)

# The variable 'result' now contains the final solid geometry