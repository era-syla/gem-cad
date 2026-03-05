import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the C-channel profile with lips
length = 150.0       # Total extrusion length
height = 50.0        # Overall height of the profile
width = 60.0         # Overall width (depth) of the profile
thickness = 3.0      # Material thickness
lip_length = 8.0     # Length of the small inward lips at the ends of flanges

# Hole parameters (hole on the back web)
hole_diameter = 10.0
hole_offset_x = 20.0 # Distance from the left edge of the web

# --- Modeling ---

# 1. Create the outer profile sketch
# We will draw the cross-section on the YZ plane and extrude along X
# The shape is a "C" with inward returns (lips)

# Define points for the outer contour
# Assuming the back web is along the Z-axis, centered or starting at origin
# Let's start from bottom-right lip and go around

# Coordinates relative to a local origin at the bottom-back corner (0,0) of the cross-section
# Profile is in YZ plane: Y is width, Z is height.

# Using a workplane based approach to draw the profile as a single polyline
# Points are (Y, Z)
pts = [
    (width, lip_length),              # Top of bottom lip
    (width, 0),                       # Bottom-front corner
    (0, 0),                           # Bottom-back corner
    (0, height),                      # Top-back corner
    (width, height),                  # Top-front corner
    (width, height - lip_length),     # Bottom of top lip
    
    # Inner contour (offset by thickness)
    (width - thickness, height - lip_length),
    (width - thickness, height - thickness),
    (thickness, height - thickness),
    (thickness, thickness),
    (width - thickness, thickness),
    (width - thickness, lip_length),
    (width, lip_length) # Closing the loop to the start
]

# Create the extrusion
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# 2. Add the hole on the back web
# The back web is on the XZ plane (at Y=0 in our previous coordinate system)
# We need to target the face corresponding to Y=0 or Y=thickness depending on side.
# Based on the image, the hole is through the "back" vertical wall.

# Let's find the face. The back face is at x local = 0 relative to the profile sketch plane
# The extrusion went along X global.
# Let's select the face on the "back" of the C-shape.
# In our sketch, the back web is between (0,0) and (0, height).
# So it is the face with normal (0, 1, 0) relative to the sketch plane YZ? 
# No, in YZ plane, the back web is the line from (0,0) to (0, height).
# After extrusion along global X, this becomes a face on the global XY plane? 
# Wait, let's re-orient. 
# Workplane("YZ") -> X is normal. 
# Sketch Y is global Y. Sketch Z is global Z.
# Points: (0,0) is back-bottom. (Width, 0) is front-bottom.
# Extrusion is along Global X.
# So the back web is the plane at Y=0 (global).

# We want to put a hole in the back web.
# The web is the vertical wall. In the image, the hole is on the vertical face.
# Let's select the face with normal pointing towards -Y (or +Y depending on view).
# The inner face of the back web is at Y=thickness. The outer is at Y=0.
# Let's pick the outer face (Y=0) or inner face.
result = (
    result
    .faces("<Y")  # Select the back face (at Y=0)
    .workplane()
    .center(-length/2 + hole_offset_x, 0) # Adjust center relative to face center
    .hole(hole_diameter)
)

# Alternatively, if the hole position needs to be specific from an edge:
# The face center is usually (0,0).
# Length is along the extrusion direction (Local X of the face).
# Height is along the Z direction (Local Y of the face).

# Let's refine the hole placement to match the image better.
# The image shows the hole near the left end of the channel.
# Our extrusion centered the part? No, extrude(length) goes from X=0 to X=length.
# The face center on the back web (size: length x height) is at (length/2, height/2).
# We want the hole at a specific distance from the start.
# Let's re-do the hole operation more explicitly.

result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
    .faces("<Y") # Select back face
    .workplane(centerOption="CenterOfBoundBox")
    # Move to the left edge of the face
    .center(-length/2, 0) 
    # Move to the specific hole location (offset from edge)
    .center(hole_offset_x, 0) 
    # The vertical position (Y in workplane, Z in global) needs to be centered on the web height
    # Since centerOption="CenterOfBoundBox" puts us at height/2, Y offset 0 is correct.
    .hole(hole_diameter)
)