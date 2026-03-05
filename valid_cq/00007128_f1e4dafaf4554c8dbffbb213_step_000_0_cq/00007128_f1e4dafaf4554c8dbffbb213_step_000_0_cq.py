import cadquery as cq

# Parametric dimensions
# Base block dimensions
length = 100.0  # Total length of the main block
width = 40.0    # Width (depth) of the main block
height = 30.0   # Height of the block

# Protrusion dimensions
protrusion_length = 30.0  # Length of the rectangular part of the protrusion
protrusion_width = 20.0   # How far it sticks out from the main block
chamfer_size = 10.0       # Size of the chamfer on the protrusion corners

# Create the main rectangular block
base = cq.Workplane("XY").box(length, width, height)

# Create the protrusion
# We will create a sketch on the back face and extrude it
# The protrusion is centered along the length
protrusion_sketch = (
    base.faces(">Y")
    .workplane()
    .center(0, 0)  # Center on the face
    .rect(protrusion_length + 2*chamfer_size, height) # Create a rectangle initially wider to account for chamfers
    .extrude(protrusion_width)
)

# Apply chamfers to the vertical edges of the protrusion to match the shape
# The shape in the image has angled sides on the protrusion. 
# A cleaner way to model this specific shape is to draw the profile.

# Let's redefine using a single sketch extrude for the whole profile or union two shapes.
# Method 2: Union of two shapes seems robust.
# Let's refine the protrusion shape. It looks like a trapezoid or a rectangle with chamfered corners.
# Looking closely at the image, it's a rectangular block with a smaller block attached to the side.
# The smaller block has 45-degree angled sides (chamfers) connecting to the main block? 
# No, looking at the top-down profile, it looks like a "T" shape where the intersection corners are filleted or chamfered?
# Actually, looking at the image again:
# It's a large rectangle.
# Attached to the back is a smaller shape.
# That smaller shape has a flat back, and angled sides connecting to the main block.
# This is a trapezoidal prism attached to the back.

# Revised Approach:
# 1. Create the main block centered at origin.
# 2. Create the protrusion shape.
#    The protrusion is a trapezoid when viewed from the top.
#    Long edge against the main block, short edge away.
#    Wait, looking at the image, the protrusion has a flat face parallel to the main block's face, 
#    and then angled sides going *out*? No, the angled sides connect the outer face to the main block?
#    Let's look at the edges.
#    The main block is a simple box.
#    The protrusion sticks out. It has a flat face parallel to the side of the main block.
#    The corners of the protrusion *away* from the main block seem sharp (90 degrees).
#    The corners where the protrusion meets the main block? No, looking at the silhouette...
#    It looks like a simple rectangular block with another trapezoidal block attached.
#    Actually, the protrusion looks like a rectangle with chamfered corners *before* it merges, 
#    or simply a trapezoid.
#    Let's assume it's a rectangular protrusion with large chamfers on the outer corners.
#    Or maybe the angled part is the connection.
    
#    Let's try a different interpretation which is very common in mechanical parts:
#    A base rectangle.
#    A "boss" on the side.
#    The boss is rectangular.
#    There are chamfers.
    
#    Let's look at the "top" face (the large L-shaped/irregular top surface).
#    It consists of the main rectangle + a trapezoid.
#    The trapezoid has a shorter parallel side (outer) and a longer parallel side (inner, attached to main).
#    Yes, this creates the angled sides.

# Dimensions for the trapezoid:
# Inner length (attached to block): let's say 50
# Outer length: let's say 30
# Stick-out distance (width): 20

# Let's build this by drawing the profile on the XY plane and extruding Z.

# Total height
H = 30.0

# Main block
L_main = 100.0
W_main = 40.0

# Protrusion
W_prot = 20.0   # How far it sticks out
L_outer = 20.0  # The flat face at the back
L_inner = 50.0  # The width where it meets the main block

# Create the profile
result = (
    cq.Workplane("XY")
    .moveTo(-L_main/2, -W_main/2)
    .lineTo(L_main/2, -W_main/2)
    .lineTo(L_main/2, W_main/2)
    .lineTo(L_inner/2, W_main/2)       # Start of protrusion base
    .lineTo(L_outer/2, W_main/2 + W_prot) # Angled side out
    .lineTo(-L_outer/2, W_main/2 + W_prot)# Flat outer face
    .lineTo(-L_inner/2, W_main/2)      # Angled side in
    .lineTo(-L_main/2, W_main/2)
    .close()
    .extrude(H)
)

# Alternatively, using boolean operations which might be easier to tune
main_block = cq.Workplane("XY").box(L_main, W_main, H)

# The protrusion is a loft or a prism.
# Let's define the protrusion as a separate solid and union it.
# It is a trapezoidal prism.
# Vertices for the base of the trapezoid (on XY plane):
# (-L_inner/2, W_main/2)
# (L_inner/2, W_main/2)
# (L_outer/2, W_main/2 + W_prot)
# (-L_outer/2, W_main/2 + W_prot)

p_pts = [
    (-L_inner/2, W_main/2),
    (L_inner/2, W_main/2),
    (L_outer/2, W_main/2 + W_prot),
    (-L_outer/2, W_main/2 + W_prot)
]

protrusion = (
    cq.Workplane("XY")
    .polyline(p_pts)
    .close()
    .extrude(H)
)

# Combine them
result = main_block.union(protrusion)