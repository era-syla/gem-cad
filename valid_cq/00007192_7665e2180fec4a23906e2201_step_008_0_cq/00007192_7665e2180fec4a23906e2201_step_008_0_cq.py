import cadquery as cq

# Parametric dimensions
# Estimating dimensions based on the visual proportions
length = 80.0
width = 40.0
thickness = 20.0

# Cutout (U-shape) parameters
cutout_width = 20.0  # Width of the slot
cutout_depth = 25.0  # Depth of the slot from the end face

# Hole parameters
hole_diameter = 10.0
hole_center_distance_from_end = 20.0 # Distance from the solid end

# Create the main base block
base = cq.Workplane("XY").box(length, width, thickness)

# Create the U-shaped cutout on one end (let's say the +X side)
# We select the top face, work on it, sketch a rectangle and cut down through all
result = (
    base
    .faces(">X")           # Select the rightmost face
    .workplane()           # Work on that plane
    .rect(cutout_width, thickness) # Create a rectangle for the cutout profile
    .cutBlind(-cutout_depth) # Cut backwards into the object
)

# Create the hole on the other end (the -X side)
# Position: centered on Y, offset from the -X edge
hole_x_pos = -length/2 + hole_center_distance_from_end

result = (
    result
    .faces(">Z")           # Select the top face
    .workplane()           # Work on that plane
    .moveTo(hole_x_pos, 0) # Move to the hole center location
    .hole(hole_diameter)   # Create the through hole
)

# The 'result' variable contains the final geometry as requested