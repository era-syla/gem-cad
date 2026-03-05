import cadquery as cq

# Parametric dimensions
width = 100.0        # Outer width of the frame
length = 100.0       # Outer length of the frame
outer_height = 10.0  # Height of the outer wall
wall_thick = 2.0     # Thickness of the walls
ledge_width = 5.0    # Width of the inner ledge (shelf)
ledge_thick = 2.0    # Thickness of the inner ledge base

# Create the base shape
# We will start by creating the outer block and cutting away the inside
# Strategy:
# 1. Create a base plate (the ledge thickness)
# 2. Add the outer walls
# 3. Cut out the center

# Method: Create a sketch and extrude
# The profile is a rectangle with an inner hole, creating the "ledge".
# Then we add the walls on top.

# Alternative Method: Constructive Solid Geometry (CSG)
# 1. Outer box
# 2. Cut a hole through the center (leaving the ledge width)
# 3. Cut a larger hole from the top (leaving the wall thickness) to form the "L" profile.

# Let's use the CSG approach as it's very readable.

# 1. Create the main outer block
outer_block = cq.Workplane("XY").box(length, width, outer_height)

# 2. Create the cutout for the center hole (all the way through)
# The hole size is determined by subtracting the ledge width from both sides
inner_hole_length = length - (2 * ledge_width)
inner_hole_width = width - (2 * ledge_width)

# 3. Create the cutout for the "step" or "recess"
# This creates the L-profile. We need to cut away the material inside the walls,
# but above the ledge.
# The area to cut is inside the outer walls.
recess_length = length - (2 * wall_thick)
recess_width = width - (2 * wall_thick)
recess_depth = outer_height - ledge_thick

# Perform the cuts
result = (
    outer_block
    # Cut the through-hole in the center
    .faces(">Z").workplane().rect(inner_hole_length, inner_hole_width).cutThruAll()
    # Cut the recess from the top to create the walls and expose the ledge
    .faces(">Z").workplane().rect(recess_length, recess_width).cutBlind(-recess_depth)
)

# Optional: Add fillets to the corners if desired, though the image shows fairly sharp outer corners 
# and slightly rounded inner corners. Let's add a small fillet to the vertical edges for realism.
# result = result.edges("|Z").fillet(0.5) 
# The image shows sharp outer corners, so we will leave them sharp as per standard extrusion look.