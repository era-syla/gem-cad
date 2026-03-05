import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the plate
width = 40.0         # Width of the plate
thickness = 10.0     # Thickness of the plate

# Slot dimensions
slot_height = 30.0   # Height of the rectangular cutout
slot_width = 15.0    # Width of the rectangular cutout

# Top hole dimensions
hole_diameter = 3.0  # Diameter of the top holes
hole_spacing = 20.0  # Distance between the two holes
hole_depth = 15.0    # Depth of the holes (assuming they might not go all the way through, but let's make them deep enough)

# Create the main body
# We start with a box centered at the origin for X and Y, sitting on Z=0 or centered on Z.
# Let's center it on all axes for symmetry.
result = cq.Workplane("XY").box(width, thickness, height)

# Create the rectangular slot in the center
# We select the front face (normal along Y)
result = result.faces(">Y").workplane().rect(slot_width, slot_height).cutThruAll()

# Create the two holes on the top face
# We select the top face (normal along Z)
# The holes are aligned along the X-axis (width)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter, depth=hole_depth)
)

# If the holes are meant to go all the way through the length, we could use cutThruAll, 
# but based on typical parts like this, they look like mounting holes or tap drill holes.
# The image shows the top face.
# Let's assume a reasonable depth or through-hole. Given the aspect ratio, 
# they likely don't go through the whole height. .hole() creates a counterbore/hole.
# If I wanted them to be simple cuts, I could use cutBlind. .hole() is cleaner.