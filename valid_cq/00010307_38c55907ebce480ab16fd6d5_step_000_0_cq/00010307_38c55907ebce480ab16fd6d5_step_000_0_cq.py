import cadquery as cq

# --- Parameters ---
die_size = 20.0
fillet_radius = 1.0  # For the edges of the cube
pip_radius = 2.0     # Radius of the dot
pip_depth = 1.0      # How deep the dot is cut
pip_spacing_factor = 0.25 # Factor of die_size to space pips from center

# Calculate the offset distance for pips based on spacing factor
offset = die_size * pip_spacing_factor

# --- Helper Function for Pips ---
def create_pips(workplane, positions):
    """
    Creates spherical cuts (pips) on a given workplane at specified positions.
    """
    return (
        workplane.workplane(offset=die_size/2.0)
        .pushPoints(positions)
        .sphere(pip_radius)
        # We cut slightly deeper than needed to ensure clean geometry, 
        # but the sphere position needs adjustment to create the "dimple" effect.
        # A sphere centered on the face would stick out half-way.
        # We want to subtract a sphere that is mostly "outside" the cube.
        # Let's shift the sphere down so it barely intersects.
        # Actually, standard dice have spherical caps removed.
        # If we cut with a sphere centered exactly at the face surface:
        # cut(cq.Workplane().sphere(r))
    )

# --- Base Geometry ---
# Create the base cube centered at origin
die = cq.Workplane("XY").box(die_size, die_size, die_size)

# Apply fillets to all edges of the cube
die = die.edges().fillet(fillet_radius)

# --- Creating Faces ---

# Standard Dice Pip Arrangements:
# 1: Center
# 2: Top-Left, Bottom-Right (or variations)
# 3: Top-Left, Center, Bottom-Right
# 4: Top-Left, Top-Right, Bottom-Left, Bottom-Right
# 5: Corners + Center
# 6: Two rows of three

# Define positions relative to the center of a face
pos_center = (0, 0)
pos_tl = (-offset, offset)   # Top-Left
pos_tr = (offset, offset)    # Top-Right
pos_ml = (-offset, 0)        # Middle-Left
pos_mr = (offset, 0)         # Middle-Right
pos_bl = (-offset, -offset)  # Bottom-Left
pos_br = (offset, -offset)   # Bottom-Right


# Face 1 (Top, usually opposite 6) - We don't see 1 in image, but let's assume standard layout.
# Image shows:
# Top Face: 2 pips
# Left Face: 4 pips
# Right Face: 6 pips

# Let's orient based on the view:
# Top Face (Z-positive): 2 Pips
positions_2 = [pos_tl, pos_br] # Diagonal

# Front Face (Y-negative, usually opposite 5): Let's put 4 here to match "Left" visually
# Actually, let's map faces specifically to the axes for clarity.
# Top (Z+) -> 2
# Front (Y-) -> 4 (acting as the left face in the iso view)
# Right (X+) -> 6 (acting as the right face in the iso view)

positions_4 = [pos_tl, pos_tr, pos_bl, pos_br]
positions_6 = [pos_tl, pos_tr, pos_ml, pos_mr, pos_bl, pos_br]

# To make the cutting code cleaner, we define the cut operation logic:
# We need to move a sphere so that it intersects the face to create a dimple.
# To get a dimple of specific radius and depth, we can cut with a sphere.
# Sphere Center distance from face = sqrt(R^2 - r_cut^2) is complex for depth.
# Simpler approach: Create a sphere at the point on the face, then move it 'down' into the material 
# or keep it centered on the face to get a hemisphere cut.
# Looking at the image, they look like shallow spherical caps.
# We will position spheres centered exactly on the face surface for a hemisphere cut, 
# or offset slightly outward for a shallow cut.
# Let's do a shallow cut. Center of sphere is offset outwards by (pip_radius - pip_depth).

cut_offset = pip_radius - pip_depth

def cut_face(part, face_selector, positions):
    # Select the face, create a workplane on it
    wp = part.faces(face_selector).workplane(centerOption="CenterOfMass")
    
    # Create spheres at the positions, shifted outwards to control depth
    # Note: workplane() creates a plane on the surface. Z is normal pointing out.
    # We create spheres at Z = cut_offset.
    
    # We accumulate the spheres into a single shape to cut at once
    spheres = (
        wp.pushPoints(positions)
        .sphere(pip_radius)
        .translate((0, 0, -cut_offset)) # Move sphere so top is inside, or center is outside?
        # Default sphere is at origin. We want the "bottom" of the sphere to penetrate 'pip_depth'.
        # Center is at (0,0,0). Bottom is at Z = -radius.
        # We want bottom at Z = -pip_depth.
        # So we move center to Z = radius - pip_depth.
        # Wait, the cut object is subtracted.
        # We want the sphere center to be 'outside' the cube by (radius - pip_depth).
    )
    
    # Correct math check:
    # If center is at Z=0 (on face), cut depth is Radius.
    # If we want depth D < R, we move center OUT by (R - D).
    move_dist = pip_radius - pip_depth
    
    # Re-generating spheres with correct transform relative to the local workplane
    spheres = (
        wp.pushPoints(positions)
        .sphere(pip_radius)
        .translate((0,0, move_dist)) 
    )
    
    return part.cut(spheres)

# --- Apply Cuts ---

# Top Face (Z max): 2 Pips
# Note: The image shows the 2 pips aligned diagonally.
die = cut_face(die, ">Z", positions_2)

# "Left" Face in image (let's map to -X or -Y depending on preference, let's use -X): 4 Pips
die = cut_face(die, "<X", positions_4)

# "Right" Face in image (let's map to -Y, to make an isometric view work): 6 Pips
# If Top is Z, Left is -X, Right is -Y -> This forms a corner.
die = cut_face(die, "<Y", positions_6)

# (Optional) Fill the rest of the faces to make a complete die, though not strictly in image
# Opposite 2 (Top) is 5 (Bottom)
positions_5 = [pos_tl, pos_tr, pos_center, pos_bl, pos_br]
die = cut_face(die, "<Z", positions_5)

# Opposite 4 (Left/-X) is 3 (Right/+X)
positions_3 = [pos_tl, pos_center, pos_br]
die = cut_face(die, ">X", positions_3)

# Opposite 6 (Right/-Y) is 1 (Back/+Y)
positions_1 = [pos_center]
die = cut_face(die, ">Y", positions_1)

# Result
result = die