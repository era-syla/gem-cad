import cadquery as cq

# --- Dimensions ---
L = 120.0                # Total Length of the part
H = 30.0                 # Total Height
W = 30.0                 # Total Depth (Y axis)
flange_thick = 6.0       # Thickness of the front flange plate
block_height = 22.0      # Height of the main block section
block_depth = W - flange_thick 
pocket_len = 36.0        # Length of central pocket
pocket_width = 14.0      # Width of central pocket
pocket_depth = 14.0      # Depth of central pocket
clamp_x_offset = 48.0    # Distance from center to clamp holes
clamp_hole_dia = 6.0     # Vertical clamp hole diameter
side_hole_dia = 3.5      # Horizontal clamping screw hole diameter
slot_spacing = 100.0     # Distance between mounting slots (center-to-center)
slot_len = 12.0          # Length of mounting slots
slot_w = 5.5             # Width of mounting slots

# --- 1. Base Geometry ---
# Create the L-shaped profile on the YZ plane (Right view)
# (0,0) corresponds to the bottom-front corner
pts = [
    (0, 0),
    (flange_thick, 0),
    (flange_thick, H - block_height),
    (W, H - block_height),
    (W, H),
    (0, H)
]

# Extrude symmetrically along X to create the main solid
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(L/2.0, both=True)
)

# --- 2. Central Pocket ---
# Rectangular cut from the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(pocket_len, pocket_width)
    .cutBlind(-pocket_depth)
)

# --- 3. Through Hole in Pocket ---
# Hole passing through the web in the Y-axis (Front-Back)
result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, H - block_height/2.0) # Vertically centered on the block section
    .hole(8.0)
)

# --- 4. Clamping Features (Ends) ---
# Calculate positions relative to the Top Face center
# Top Face Center Y (Global) = W/2
# Block Section Center Y (Global) = flange_thick + block_depth/2
y_offset_block_center = (flange_thick + block_depth/2.0) - (W/2.0)

# Vertical Clamp Holes
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(-clamp_x_offset, y_offset_block_center), 
                 (clamp_x_offset, y_offset_block_center)])
    .hole(clamp_hole_dia)
)

# Expansion Slits
# Cut from the vertical hole to the back face to allow clamping
slit_len = block_depth / 2.0  # Approximate length from center to back
slit_y_pos = y_offset_block_center + (slit_len / 2.0) # Centered for the rect cut

result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(-clamp_x_offset, slit_y_pos), 
                 (clamp_x_offset, slit_y_pos)])
    .rect(1.0, slit_len) # 1mm wide slit
    .cutBlind(-block_height)
)

# Horizontal Clamping Screw Holes
# Located on the side faces, intersecting the slit region
# Target Global Coordinates for the screw
z_screw_global = H - block_height/2.0
y_screw_global = flange_thick + block_depth * 0.75 # Positioned behind the vertical hole

# Calculate local offsets for side faces
# For >X Face (Right), Center is at (L/2, W/2, H/2)
dy = y_screw_global - (W/2.0)
dz = z_screw_global - (H/2.0)

result = (
    result
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .center(dy, dz)
    .hole(side_hole_dia, 25.0) # Depth to cross the slit
)

result = (
    result
    .faces("<X")
    .workplane(centerOption="CenterOfMass")
    .center(-dy, dz) # Symmetry for the left face
    .hole(side_hole_dia, 25.0)
)

# --- 5. Mounting Slots on Front Flange ---
# Located on the front face (<Y), near the bottom
z_slot_global = 8.0 # Height from bottom
dz_slot = z_slot_global - (H/2.0)

result = (
    result
    .faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .center(0, dz_slot)
    .pushPoints([(-slot_spacing/2.0, 0), (slot_spacing/2.0, 0)])
    .slot2D(slot_len, slot_w, 0) # Horizontal slot (angle=0)
    .cutBlind(-flange_thick)
)

# --- 6. Cosmetic Groove (Top) ---
# Small T-feature near the right clamp
groove_y = y_offset_block_center + 3.0
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(pocket_len/2.0 + 8.0, groove_y)
    .rect(16.0, 1.5)
    .cutBlind(-1.0)
    .center(6.0, 0)
    .rect(1.5, 6.0)
    .cutBlind(-1.0)
)