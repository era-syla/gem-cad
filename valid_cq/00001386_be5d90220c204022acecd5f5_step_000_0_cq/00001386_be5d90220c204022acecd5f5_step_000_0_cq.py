import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the block (X axis)
width = 30.0   # Width/Depth of the block (Y axis)
height = 80.0  # Height of the block (Z axis)
fillet_radius = 10.0 # Radius for the rounded corners

# Create the base block
# We center it on X and Y, but align the bottom to Z=0 for easier visualization
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# Apply fillets
# Looking at the image, there is a prominent rounded corner on the top-left-front.
# It seems like the entire left side (vertical edges) and the top left edge are filleted.
# Let's try selecting edges based on their position.

# 1. Select the vertical edges on the "left" side (e.g., -X direction)
# 2. Select the top edge on the "left" side.
# 3. Or, more simply, select the face on the left and fillet its edges, or select specific edges.

# Strategy:
# Let's assume the block is aligned such that the rounded face is on the negative X side.
# The image shows a rounded corner that blends a vertical edge and a top edge.
# This often happens when you fillet a vertical edge and then the top loop, or vice versa, 
# or select multiple edges at once.

# Based on the specific look (a "suitcase" corner), it looks like:
# - The vertical edges on the left face (-X) are filleted.
# - The top edge on the left face (-X) is filleted.
# Let's try selecting the edges of the face at -X.

result = result.edges("|Z and <X").fillet(fillet_radius)
result = result.edges("|Y and <X and >Z").fillet(fillet_radius)

# Alternatively, looking closely at the specific topology:
# The top-left corner is rounded. The bottom-left corner is rounded.
# It looks like the entire left face (-X) might just be fully rounded over if the radius was half the thickness,
# but here it's a partial round.
# It looks like the two vertical edges at min X and the top horizontal edge at min X are filleted.

# Let's refine the selection to match the image precisely.
# The image shows:
# 1. Front-left vertical edge is rounded.
# 2. Back-left vertical edge is rounded.
# 3. Top-left horizontal edge is rounded.
# 4. The corner where they meet is spherical/smooth.

# This is achieved by selecting those 3 edges and filleting them.
# Or simpler: Select the left face (-X) and fillet its perimeter edges? No, the bottom edge isn't clearly visible as rounded, but usually is in this style.
# Let's look at the bottom left. It does look rounded.

# Let's try filleting the vertical edges on the -X side first, then the top edge on the -X side.
# CadQuery/OCCT handles corner blends automatically.

# Re-creating the object with specific edge selection for robustness:
# Edges parallel to Z, located at X min.
# Edges parallel to Y, located at X min and Z max.

# Let's assume the user wants the specific look in the image.
# It looks like a box where the edge (X_min, Y_min, Z_all), (X_min, Y_max, Z_all) and (X_min, Y_all, Z_max) are filleted.
# Actually, looking at the very bottom left corner, it is rounded too.
# This implies the vertical edges on the left are filleted.
# And the top edge on the left is filleted.
# Is the bottom edge on the left filleted? The image cuts off a bit or shadow obscures it, but usually, symmetry suggests it might be.
# However, the prompt image is a singular view. The top corner is the most prominent feature.

# Let's go with:
# 1. Vertical edges at -X
# 2. Top edge at -X

# Create the box
result = cq.Workplane("XY").box(length, width, height)

# Select vertical edges on the "left" (negative X)
# selector: parallel to Z axis, and having the minimum X coordinate
vertical_edges = result.edges("|Z").filter(lambda e: e.Center().x < 0)

# Select the top edge on the "left" (negative X)
# selector: parallel to Y axis, located at top (max Z) and left (min X)
top_edge = result.edges("|Y").filter(lambda e: e.Center().z > 0 and e.Center().x < 0)

# Apply fillet to vertical edges first
result = result.edges("|Z").filter(lambda e: e.Center().x < -length/2 + 0.1).fillet(fillet_radius)

# Apply fillet to the top edge connecting them
# After the vertical fillet, the top edge is still selectable near min X and max Z
result = result.edges("|Y").filter(lambda e: e.Center().z > height/2 - 0.1 and e.Center().x < -length/2 + fillet_radius + 0.1).fillet(fillet_radius)

# While the above logic works, a more robust single-operation approach often yields cleaner topology for corners.
# Let's try selecting all relevant edges at once if possible, or order them correctly.
# If we fillet the vertical edges first, the top edge becomes shorter.
# If we fillet the top edge first, the vertical edges become shorter.
# The image shows a "ball" corner, which is typical of a 3-way fillet or a chain fillet.
# Let's try a fresh simple block and standard selectors.

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Select the two vertical edges at x_min
    .edges("<X and |Z")
    .fillet(fillet_radius)
    # Select the top edge at x_min (which now connects the tops of the previous fillets)
    .edges("<X and >Z")
    .fillet(fillet_radius)
)