import cadquery as cq

# Parametric dimensions
length = 100.0       # Total length of the plate
width = 25.0         # Total width of the plate
thickness = 3.0      # Thickness of the plate
corner_radius = 5.0  # Radius of the rounded corners

# Hole parameters
large_hole_diameter = 6.0
small_hole_diameter = 3.5

# Hole positions (relative to center)
# The image shows two larger holes at the ends and two smaller holes near the middle
# We'll calculate positions based on the length
outer_hole_spacing = length - (2 * corner_radius) - 5.0 # Distance between outer holes
inner_hole_spacing = 30.0 # Distance between inner holes

# Create the base plate with rounded corners
# We start with a rectangle and extrude it
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .edges("|Z") # Select vertical edges
    .fillet(corner_radius) # Apply fillet to corners
)

# Create the holes
# We'll cut the holes through the plate
# Outer holes (larger)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-outer_hole_spacing/2, 0), (outer_hole_spacing/2, 0)])
    .hole(large_hole_diameter)
)

# Inner holes (smaller)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-inner_hole_spacing/2, 0), (inner_hole_spacing/2, 0)])
    .hole(small_hole_diameter)
)

# Optional: Add the small tab feature visible on the left side
# Based on the image, there seems to be a small downward protrusion 
# on the bottom-left edge. Let's add a small tab there.
tab_width = 8.0
tab_height = 2.0
tab_depth = 2.0

# We locate the left face and draw a rectangle on the bottom edge
result = (
    result.faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .center(0, -thickness/2) # Move to bottom edge
    .rect(width/2, tab_height) # Create rectangle for tab
    .extrude(tab_depth) # Extrude outwards slightly
)