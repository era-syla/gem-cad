import cadquery as cq

# Parametric dimensions
width = 50.0       # External width/length of the box
height = 15.0      # Total height of one half
wall_thickness = 2.0
corner_radius = 5.0
lip_height = 2.0   # Height of the interlocking lip
lip_thickness = wall_thickness / 2.0 # Thickness of the lip
separation_dist = 60.0 # Distance to separate the two halves in the view

# --- Helper Function to Create a Base Shell ---
def create_shell(w, h, t, r):
    # Create the base block
    base = (cq.Workplane("XY")
            .box(w, w, h)
            .edges("|Z")
            .fillet(r)
    )
    
    # Create the hollow shell
    # We want the bottom to be solid, so we shell from the top face
    shell = base.faces(">Z").shell(-t)
    return shell

# --- Create the Bottom Half (Female Lip) ---
# The bottom half typically has an inner recess or shelf for the top lip to sit on.
# Based on the image, the right object looks like the "bottom" with an inner step.
# Actually, looking closer at the right object, it has a thin wall extending up *inside*.
# Looking at the left object, it has a reduced outer profile at the top.
# Let's assume:
# - Left object = Top Cover (Male part: reduced outer dimension lip)
# - Right object = Bottom Case (Female part: recessed inner dimension)

# However, looking extremely closely at the image:
# The LEFT object has a step-down on the outside. This is a "Male" lip.
# The RIGHT object has a step-down on the inside. This is a "Female" lip.

# Bottom Half Construction (Right object in image)
bottom_half = create_shell(width, height, wall_thickness, corner_radius)

# Create the female recess (cut away the inside top edge)
# We need to cut a "shelf" on the inside rim.
# The cut depth is lip_height. The cut width is lip_thickness.
bottom_half = (bottom_half.faces(">Z")
               .workplane()
               .rect(width - 2*wall_thickness + 2*lip_thickness, 
                     width - 2*wall_thickness + 2*lip_thickness)
               .rect(width - 2*wall_thickness, width - 2*wall_thickness) # Inner void to avoid cutting air
               .cutBlind(-lip_height)
)

# Apply fillets to the bottom edges for aesthetics (as seen in image)
bottom_half = (bottom_half.edges("<Z")
               .fillet(corner_radius / 2.0)
)


# --- Create the Top Half (Male Lip) ---
# Top Half Construction (Left object in image)
top_half = create_shell(width, height, wall_thickness, corner_radius)

# Create the male lip (cut away the outside top edge)
# We remove material from the outside perimeter to leave a thin sticking-out wall.
top_half = (top_half.faces(">Z")
            .workplane()
            .rect(width, width) # Outer bound
            .rect(width - 2*lip_thickness, width - 2*lip_thickness) # Inner bound (defines the lip wall)
            .cutBlind(-lip_height)
)

# Apply fillets to the top edges (which are now at Z=0 relative to creation, but represent the "top" outside face)
# Since we built it bottom-up, the face at Z=-height (relative to workplane) is the cosmetic top.
top_half = (top_half.edges("<Z")
            .fillet(corner_radius / 2.0)
)

# --- Arrange the Parts ---
# Rotate top half to match the orientation in the image (upside down)
top_half_positioned = top_half.rotate((0,0,0), (1,0,0), 180).translate((-separation_dist/2, 0, height))
bottom_half_positioned = bottom_half.translate((separation_dist/2, 0, 0))

# Combine into result
result = top_half_positioned.union(bottom_half_positioned)