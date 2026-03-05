import cadquery as cq

# Parameters
length = 100.0  # Length of the plate
width = 80.0    # Width of the plate
thickness = 5.0 # Thickness of the plate
chamfer_size = 5.0 # Size of the chamfer (45 degrees)

# Create the base rectangular block
# We center it to make operations symmetric
result = cq.Workplane("XY").box(length, width, thickness)

# Select the edges on the top face (Z-max) to apply the chamfer
# Based on the image, the top surface is smaller than the bottom, 
# or the edges are angled. 
# Looking at the image, it looks like a "pyramid" frustum with a very low height.
# This is equivalent to chamfering the top edges of a box, or lofting two rectangles.
# Let's assume it's a box with a large chamfer on the top face edges.
# Or, conversely, a box with a chamfer on the side edges.

# Let's look closer. The side faces are angled inward from bottom to top. 
# This means the top face is smaller than the bottom face.
# This can be achieved by chamfering the top edges.
# If thickness is 5 and chamfer is 5, it creates a sharp edge at the bottom if the chamfer goes all the way.
# The image shows a small vertical section at the bottom? No, it looks like a pure bevel on the sides.
# Actually, looking at the corner, the edge is sharp.
# Let's assume a generic plate with a 45-degree bevel on the sides.

# Let's try creating a box and chamfering the top edges.
# Select edges on the top face
result = result.edges("|Z").chamfer(chamfer_size) # This would chamfer vertical corners. Wrong.

# We need to chamfer the perimeter of the top face.
# Let's reset.
result = cq.Workplane("XY").box(length, width, thickness)
# Select edges that are on the top plane (Z > 0)
# Since the box is centered, Z runs from -thickness/2 to +thickness/2.
# We want the edges at Z=+thickness/2.
top_edges = result.faces(">Z").edges()

# If the chamfer size is almost the thickness or creates that angled look:
# From the image, the angle looks roughly 45 degrees.
# Let's apply a chamfer.
result = result.faces(">Z").edges().chamfer(thickness * 0.8) 
# Adjusting chamfer size to look like the image. 
# The image shows a significant slope. Let's make it equal to height for a 45 deg slope, 
# or slightly less to leave a top surface.

# Let's use specific dimensions for reproducibility.
# Let's assume it's a base rectangle of 100x100 and a top rectangle of 80x80 lofted?
# Chamfer is easier.

# Re-evaluating the image:
# The shape is a truncated pyramid with a rectangular base.
# Base box.
L = 100.0
W = 100.0
H = 10.0
chamfer_dist = 10.0 # If equal to height, it's 45 degrees.

# Let's make a parameterized version.
result = (
    cq.Workplane("XY")
    .box(L, W, H)
    .faces(">Z") # Select top face
    .edges()     # Select edges of the top face
    .chamfer(H * 0.8) # Apply chamfer. 0.8*H gives a nice bevel without making the top face disappear if W/L are large enough.
)

# Refined parameters to match the aspect ratio of the image better
# The image looks slightly rectangular, not perfectly square.
L_final = 60.0
W_final = 60.0
H_final = 5.0
Chamfer_final = 2.0

result = (
    cq.Workplane("XY")
    .box(L_final, W_final, H_final)
    .faces(">Z")
    .edges()
    .chamfer(Chamfer_final)
)