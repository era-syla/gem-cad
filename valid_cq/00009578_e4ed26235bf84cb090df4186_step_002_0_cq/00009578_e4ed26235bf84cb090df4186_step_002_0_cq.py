import cadquery as cq

# -- Parametric Dimensions --
length = 50.0   # Total length of the block (depth)
width = 50.0    # Total width of the base
height = 50.0   # Total height of the block
base_height = 30.0 # Height of the vertical base section before the taper starts

# Derived dimensions
taper_height = height - base_height
top_width = 30.0 # Width of the flat top surface

# -- Modeling --

# 1. Create the base box
# We create a box centered on X and Y, sitting on the Z plane
result = cq.Workplane("XY").box(width, length, height, centered=(True, True, False))

# 2. Apply chamfers to create the tapered top
# We select the top edges that run along the 'length' (Y) axis.
# The chamfer distance needs to be calculated to reduce the width from 'width' to 'top_width'.
chamfer_width_distance = (width - top_width) / 2.0
chamfer_height_distance = taper_height

# We select edges that are at the top (Z max) and parallel to the Y axis
result = result.edges(f"|Y and >Z").chamfer(chamfer_width_distance, chamfer_height_distance)

# Alternatively, a more robust way without assuming edge direction perfectly is to sketch the profile
# Let's verify the first approach. It's cleaner for simple shapes.
# However, `chamfer(length, length2)` applies asymmetric chamfers.
# CadQuery's chamfer usually takes one argument for 45 deg or two for asymmetric.
# If two arguments are provided, the order matters relative to the face references.
# Let's try a sketch-based extrusion approach which is often more predictable for specific profiles.

# -- Robust Sketch Approach --

# Define the points for the front profile (looking down the Y axis)
pts = [
    (width/2, 0),             # Bottom right
    (width/2, base_height),   # Top of vertical wall right
    (top_width/2, height),    # Top right corner
    (-top_width/2, height),   # Top left corner
    (-width/2, base_height),  # Top of vertical wall left
    (-width/2, 0)             # Bottom left
]

# Create the profile and extrude it
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(length)
    # Center the extrusion on Y axis to match typical "centered" behavior, 
    # though standard extrude goes in +Normal direction. 
    # Let's translate it back by half length to center it.
    .translate((0, -length/2, 0))
)