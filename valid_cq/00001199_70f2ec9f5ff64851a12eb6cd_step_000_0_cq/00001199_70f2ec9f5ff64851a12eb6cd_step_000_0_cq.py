import cadquery as cq

# --- Parameters ---
# Standard LEGO-like dimensions (approximate in mm)
pitch = 8.0              # Distance between stud centers
stud_diameter = 4.8      # Diameter of the stud
stud_height = 1.7        # Height of the stud
brick_height = 9.6       # Height of the main brick body (without studs)
wall_thickness = 1.2     # Thickness of the outer walls (standard is usually ~1.2-1.5)

# Brick configuration (rows x columns)
rows = 2
cols = 3

# Calculated overall dimensions
length = cols * pitch
width = rows * pitch

# --- Modeling ---

# 1. Create the main rectangular body
# Using centered=False to make positioning easier relative to origin if needed, 
# but centered=True is often cleaner for symmetry. Let's stick to centering on XY.
brick_body = cq.Workplane("XY").box(length, width, brick_height)

# 2. Create the studs
# We need a grid of points on the top face.
# The top face is at z = brick_height / 2
# The grid starts inset by half a pitch from the edges.

# Define the grid of points for the studs
stud_locs = [
    (
        (c * pitch) - (length / 2) + (pitch / 2), 
        (r * pitch) - (width / 2) + (pitch / 2)
    )
    for r in range(rows)
    for c in range(cols)
]

# Create the studs on the top face
studs = (
    cq.Workplane("XY")
    .workplane(offset=brick_height / 2)
    .pushPoints(stud_locs)
    .circle(stud_diameter / 2)
    .extrude(stud_height)
)

# 3. Combine the body and studs
solid = brick_body.union(studs)

# 4. Hollow out the bottom (Shelling)
# The standard LEGO brick is hollow underneath.
# We select the bottom face (Z negative) and shell it inwards.
# Note: A real LEGO brick has internal tubes for clutch power. 
# This request asks for the model based on the image, which only shows the top.
# However, a solid block isn't very realistic for a "brick".
# To match the visual exactly as a solid block (often used for simple rendering), 
# shelling might be optional, but makes it a "brick".
# Looking at the prompt "based on the provided image", the image shows a solid-looking object 
# from the top. Let's make it a shelled shell to be a valid part, or just a solid if simpler.
# Standard practice for these CAD exercises is usually to make the shell.
# Let's add the shell for completeness as it's a "CAD engineer" persona.

# Select bottom face
result = solid.faces("<Z").shell(-wall_thickness)

# If the user strictly wanted just the visual outer hull as a solid block (easier for printing sometimes without infill issues):
# result = solid 

# Given the prompt asks for "deep knowledge", I will include the shell as it's geometrically correct for this type of part.
# However, generating internal tubes is complex and not visible in the image. 
# I will stick to the shell to make it a hollow box.

# --- Refinement: Internal Tubes (Optional but good for 2x3) ---
# For a 2x3 brick, there are usually solid posts or tubes inside to grip the studs below.
# Since they aren't visible in the image, I will omit the complex internal structure 
# to ensure the code stays robust and focused on the visual input provided.
# The shell command above creates the basic hollow brick.

# --- Final Output ---
result = result

# Export is not requested, just the variable 'result'