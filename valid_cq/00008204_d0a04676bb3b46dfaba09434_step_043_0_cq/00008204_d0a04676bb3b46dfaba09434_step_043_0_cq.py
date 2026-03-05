import cadquery as cq

# Parametric dimensions
width = 10.0      # Width of the square base
depth = 10.0      # Depth of the square base
height = 40.0     # Height of the block
hole_diameter = 3.0 # Diameter of the top hole
hole_depth = 5.0   # Depth of the hole (set deeper or equal to height for through-hole)

# Create the main block
# We start with a workplane on the XY plane
result = (
    cq.Workplane("XY")
    .box(width, depth, height) # Create a centered box
    .faces(">Z")               # Select the top face (positive Z direction)
    .workplane()               # Create a new workplane on the top face
    .hole(hole_diameter, hole_depth) # Cut a hole into the block
)

# If you prefer the hole to go all the way through, you can use:
# .hole(hole_diameter) # Without the depth argument, it cuts through all available material