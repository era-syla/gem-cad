import cadquery as cq

# Define parametric dimensions
box_length = 40.0
box_width = 20.0
box_height = 15.0
wall_thickness = 1.0  # Assumed thickness for the wireframe-like structure
shelf_height = 5.0    # Height of the solid shelf from the bottom
line_length = 50.0    # Length of the vertical line extending downwards

# Create the main outer wireframe box (represented as a shell or thin-walled box)
# Since the image looks like a wireframe with a solid shelf, we will model it
# as a hollow box with a solid internal face.

# 1. Create the main box shape
box = cq.Workplane("XY").box(box_length, box_width, box_height)

# 2. Create the solid shelf inside. 
# It appears to be a plane or a thin plate located slightly above the bottom.
# We will create a plate that fits inside the box dimensions.
shelf = (
    cq.Workplane("XY")
    .workplane(offset=-box_height/2 + shelf_height)
    .box(box_length, box_width, 1.0) # Give it a small thickness to be visible as a solid
)

# 3. Create the wireframe visualization. 
# CadQuery creates solids by default. To match the "wireframe" look of the box 
# in the diagram while keeping the shelf solid, we can shell the main box 
# or construct it from edges. However, standard CAD models are usually solids.
# The image likely represents a transparent box with an opaque shelf.
# We will create the outer box as a hollow shell.
outer_shell = box.faces("Z").shell(-wall_thickness)

# 4. Create the vertical line.
# In solid modeling, "lines" aren't usually volume, but we can represent it 
# as a very thin cylinder or just an edge for the purpose of the model.
# The line extends from the bottom center downwards.
line_visual = (
    cq.Workplane("XY")
    .workplane(offset=-box_height/2) # Start at bottom of box
    .circle(0.1) # Tiny radius to approximate a line
    .extrude(-line_length)
)

# Combine the parts
# Note: Since the outer box is transparent in the diagram, we just return the geometry.
# A union of the shell, the internal shelf, and the "line".
result = outer_shell.union(shelf).union(line_visual)

# If strictly a wireframe representation is needed without volume for the box walls,
# one might just return the edges, but 'result' usually expects a solid or compound.
# The code above produces a physical approximation of the drawing:
# 1. A hollow rectangular container.
# 2. A solid shelf inside.
# 3. A thin rod extending downwards.