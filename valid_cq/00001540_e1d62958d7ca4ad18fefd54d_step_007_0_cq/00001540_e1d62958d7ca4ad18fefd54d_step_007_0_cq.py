import cadquery as cq

# Parametric dimensions
# Estimating dimensions based on the visual proportions
length = 100.0   # Length of the long side
width = 80.0     # Width of the other main side
height = 40.0    # Thickness of the block
chamfer_size = 30.0 # Size of the diagonal cut (chamfer) at the corner
hole_diameter = 8.0 # Diameter of the central hole

# Create the base shape
# We start with a rectangle and then cut a corner off to make the irregular pentagonal/trapezoidal shape
# Or simply draw the polygon points. Drawing points is often cleaner for this specific shape.

# Let's define the points of the base polygon (counter-clockwise)
# Assuming the origin (0,0) is at the "inner" corner (where the two long straight sides would meet if it were a rectangle)
# But looking at the image, it looks like a rectangle with one corner cut off (chamfered).
# Let's model it as a box with a chamfer.

# Step 1: Create a basic box
base_block = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# Step 2: Chamfer one corner to create the angled face
# We need to select the vertical edge at one of the corners. 
# Based on the image perspective, let's assume the main block is aligned with X and Y axes.
# The cut removes a triangular prism from one corner.
# Let's pick the corner at (+x, +y) for the chamfer to match the visual orientation somewhat, 
# or simpler: chamfer one of the vertical edges.

# Re-evaluating based on the specific shape:
# The shape is a 5-sided prism (pentagonal prism).
# Sides: 
# 1. Long side
# 2. Perpendicular short side
# 3. Angled side
# 4. Another short side
# 5. Another long side
# Actually, looking at the image, it's a "corner bracket" shape. 
# It looks like a square or rectangle with one corner cut off diagonally.

# Let's go with the "Box with Chamfer" approach as it's most robust.
# Let's align the corner to the origin to make hole placement easier.
# Points approach: (0,0) -> (L,0) -> (L, W-C) -> (L-C, W) -> (0, W) -> (0,0)
# Where L=Length, W=Width, C=Chamfer dimension.

L = 80.0
W = 80.0
C = 30.0 # The length of the cut on the sides
H = 30.0

# Define points for the base polygon
pts = [
    (0, 0),
    (L, 0),
    (L, W - C), # Start of diagonal cut
    (L - C, W), # End of diagonal cut
    (0, W),
    (0, 0)      # Close the loop
]

# Create the extrusion
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(H)
)

# Step 3: Create the hole
# The hole appears to be roughly in the center of the mass or slightly offset.
# Let's place it relative to the bounding box center or specific coordinates.
# Visually, it looks equidistant from the straight sides (L and W).
hole_x = L / 2.5
hole_y = W / 2.5

result = result.faces(">Z").workplane().pushPoints([(hole_x, hole_y)]).hole(hole_diameter)

# If we want the exact orientation as the image (rotated), we can rotate the final result,
# but usually, standard alignment is preferred. The code above generates the geometry correctly.