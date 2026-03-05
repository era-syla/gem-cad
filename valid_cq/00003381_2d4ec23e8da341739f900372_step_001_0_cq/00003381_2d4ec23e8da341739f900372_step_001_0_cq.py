import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the block
width = 30.0     # Width of the square cross-section
height = 30.0    # Height of the square cross-section
bore_dia = 20.0  # Diameter of the central longitudinal hole
hole_dia = 3.0   # Diameter of the small cross holes
hole_inset = 10.0 # Distance from ends to the small holes

# Create the main block
# Workplane centered on XY plane for the cross-section, extruded along Z
# Note: The image shows the long axis, let's align the long axis with X or Z.
# Let's align the long axis with X for easier mental mapping.
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .extrude(length)
)

# Create the central bore
# We select the face on the YZ plane (or center) and cut through
result = (
    result.faces(">X")
    .workplane()
    .circle(bore_dia / 2.0)
    .cutThruAll()
)

# Create the small holes on the top face
# These holes go through the top wall into the bore.
# They are located near the ends.
# Let's select the top face (+Z direction based on YZ plane extrusion along X)
# Wait, if I created rect on YZ and extruded X, top face is +Z (if height is Z)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (length / 2.0 - hole_inset, 0),  # Hole near positive X end
        (-length / 2.0 + hole_inset, 0)  # Hole near negative X end
    ])
    .hole(hole_dia)
)

# Looking closely at the image, there is a hole visible *inside* the bore at the bottom.
# This implies the top holes might go all the way through, or there are corresponding bottom holes.
# The top holes in the image look like they pierce through the top wall.
# The hole visible inside the bore at the bottom suggests the hole goes through the entire part (top to bottom)
# or there is a separate hole on the bottom. Usually, these are set screw holes or mounting holes.
# If they are set screw holes, they might just go through one wall.
# However, the hole visible on the bottom inner surface suggests a through-hole or a bottom hole.
# Let's assume they are through-holes penetrating the entire block (top and bottom walls), 
# effectively creating 4 holes (2 top, 2 bottom) or 2 long holes intersecting the bore.
# The command `.hole(hole_dia)` cuts through the entire part by default if depth isn't specified? 
# No, `hole` usually cuts through everything. Let's verify.
# Documentation: "hole() creates a hole ... through the entire solid if depth is not provided"
# So the code above creates holes through top wall, through void, and through bottom wall.
# This matches the visual cue of seeing a hole on the bottom surface inside the bore.

# If we wanted them to be only through one wall, we would limit the depth.
# Given the image, seeing the hole on the bottom surface suggests it goes all the way through.

# Let's refine the orientation to match the isometric view roughly.
# The view shows the end face, top face, and side face.
# My construction: Extrude along X. End faces are +/- X. Top is +Z. Side is -Y (or +Y).
# This is a standard orientation.

# Final check of parameters relative to image:
# - Aspect ratio looks like ~1:3 or 1:4 (Width : Length). 30x100 is roughly 1:3.3. Good.
# - Bore size relative to face: 20mm in 30mm face leaves 5mm wall. Looks about right.
# - Small holes: fairly small, 3mm looks reasonable.

# Re-constructing cleanly
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .extrude(length) # Extrudes along X axis, centered on YZ plane
    .faces(">X").workplane() # Select the far end face
    .hole(bore_dia) # Cut the central bore through the entire length
    .faces(">Z").workplane() # Select the top face
    .pushPoints([
        (length/2 - hole_inset, 0),
        (-length/2 + hole_inset, 0)
    ])
    .hole(hole_dia) # Cut the vertical holes through the entire part
)