import cadquery as cq

# Parameters
length = 400.0       # Total length of the angle bar
width = 40.0         # Width of one leg (outer dimension)
thickness = 3.0      # Thickness of the material
hole_diameter = 6.0  # Diameter of the holes
hole_spacing = 20.0  # Center-to-center distance between holes
hole_offset = 10.0   # Distance from the start/end to the first hole center
side_offset = width / 2.0 # Distance from the corner edge to the hole center line

# 1. Create the base L-profile
# We'll sketch the L-shape and extrude it
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, width)
    .lineTo(0, width)
    .close()
)

angle_bar = profile.extrude(length)

# 2. Define hole locations
# We need holes along the length on both flanges.
# Calculate number of holes based on length and spacing
num_holes = int((length - 2 * hole_offset) / hole_spacing) + 1

# Generate a list of (x, y) coordinates for the holes along the extrusion axis
# Since we extruded along Z, the "length" is Z.
# For the X-leg (horizontal in profile sketch), holes are on the X-Z plane (actually offset by thickness/2 or similar if picking faces)
# For the Y-leg (vertical in profile sketch), holes are on the Y-Z plane.

# Let's select the faces and cut holes.

# Side 1: The face on the X-Z plane (bottom flange in sketch, but extruded up)
# We select the face with normal -Y (the outer face at y=0)
# Or select face with normal +Y (inner face) -- let's use outer faces for clarity.
# Wait, looking at the profile: (0,0) to (width,0). This is a face on Y=0 plane.
pts_side1 = []
for i in range(num_holes):
    # X coordinate is centered on the flange: width/2
    # Y coordinate is height along the extrusion: hole_offset + i*spacing
    x_pos = width / 2.0
    y_pos = hole_offset + i * hole_spacing
    pts_side1.append((x_pos, y_pos))

# Side 2: The face on the Y-Z plane (side flange in sketch)
# Looking at profile: (0,0) to (0,width). This is a face on X=0 plane.
pts_side2 = []
for i in range(num_holes):
    # X coordinate is centered on the flange: width/2
    # Y coordinate is height along the extrusion: hole_offset + i*spacing
    x_pos = width / 2.0
    y_pos = hole_offset + i * hole_spacing
    pts_side2.append((x_pos, y_pos))

# 3. Cut the holes
# Select the face on the X=0 plane (The "vertical" leg in the profile)
result = (
    angle_bar
    .faces("<X")
    .workplane()
    .pushPoints(pts_side2)
    .hole(hole_diameter)
)

# Select the face on the Y=0 plane (The "horizontal" leg in the profile)
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(pts_side1)
    .hole(hole_diameter)
)

# Fillet the inner corner for realism (optional but typical for bent metal)
try:
    result = result.edges(cq.selectors.NearestToPointSelector((thickness, thickness, 0))).fillet(thickness/2.0)
except:
    pass # Skip if selection fails due to geometry complexity, though typical for this shape

# Export or display is handled by the environment, 'result' is the final variable.