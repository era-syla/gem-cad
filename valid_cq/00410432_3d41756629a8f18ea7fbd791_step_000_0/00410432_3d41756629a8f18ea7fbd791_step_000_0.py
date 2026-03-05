import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
beam_width = 12.0
beam_depth = 12.0
beam_height = 200.0

# Tenon dimensions (top and bottom)
tenon_width = 6.0
tenon_depth = 6.0
tenon_height = 10.0

# Feature locations (Z coordinates relative to center 0)
# Height is 200, so Z ranges from -100 to 100
side_slot_z = 50.0       # Slot on the right face
latch_pocket_z = 45.0    # Complex pocket on front face
front_slot_z = -15.0     # Simple slot on front face

# Feature dimensions
side_slot_dims = (3.0, 18.0)    # Width, Height
front_slot_dims = (2.0, 16.0)   # Width, Height
latch_pocket_dims = (6.0, 12.0) # Width, Height
latch_depth = 3.0               # Depth of the pocket cut

# --- Geometry Generation ---

# 1. Create Main Beam Body
# Centered at origin
result = cq.Workplane("XY").box(beam_width, beam_depth, beam_height)

# 2. Add Top and Bottom Tenons
# Create independent solids for tenons and union them for robust geometry
top_tenon = (
    cq.Workplane("XY")
    .workplane(offset=beam_height/2 + tenon_height/2)
    .box(tenon_width, tenon_depth, tenon_height)
)

bottom_tenon = (
    cq.Workplane("XY")
    .workplane(offset=-(beam_height/2 + tenon_height/2))
    .box(tenon_width, tenon_depth, tenon_height)
)

result = result.union(top_tenon).union(bottom_tenon)

# 3. Create Side Slot (Right Face / +X)
# We select the face at +X and cut inwards
result = (
    result.faces(">X").workplane()
    .center(0, side_slot_z)
    .rect(side_slot_dims[0], side_slot_dims[1])
    .cutBlind(-beam_width * 0.6)  # Deep cut
)

# 4. Create Front Slot (Front Face / -Y)
# We select the face at -Y and cut inwards
result = (
    result.faces("<Y").workplane()
    .center(0, front_slot_z)
    .rect(front_slot_dims[0], front_slot_dims[1])
    .cutBlind(-beam_depth * 0.4)
)

# 5. Create Upper Latch Pocket (Front Face / -Y)
# This involves a rectangular cut and an internal detail
# Step A: Cut the main rectangular pocket
result = (
    result.faces("<Y").workplane()
    .center(0, latch_pocket_z)
    .rect(latch_pocket_dims[0], latch_pocket_dims[1])
    .cutBlind(-latch_depth)
)

# Step B: Add the internal ramp/latch detail
# We construct a wedge shape and union it back into the pocket.
# Calculating positions relative to the global coordinate system:
# Pocket back wall Y position:
y_pocket_back = -beam_depth/2 + latch_depth
# Ramp vertical range (bottom half of pocket)
z_ramp_bottom = latch_pocket_z - latch_pocket_dims[1]/2 + 1.0
ramp_h = 5.0
ramp_protrusion = 2.0 # How far it angles out
ramp_width = 4.0

# Define triangular profile in YZ plane
# Points: (Y, Z)
pts = [
    (y_pocket_back, z_ramp_bottom),                   # Bottom-Back
    (y_pocket_back - ramp_protrusion, z_ramp_bottom + ramp_h), # Top-Front (tip)
    (y_pocket_back, z_ramp_bottom + ramp_h)           # Top-Back
]

# Create the ramp solid
latch_ramp = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(ramp_width)         # Extrudes along X axis
    .translate((-ramp_width/2, 0, 0)) # Center the extrusion on X axis
)

# Combine the ramp detail with the main body
result = result.union(latch_ramp)