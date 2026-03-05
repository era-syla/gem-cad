import cadquery as cq

# --- Dimensions & Parameters ---
tray_width = 120.0
tray_length = 180.0
tray_height = 12.0
wall_thickness = 2.0
rail_width = 10.0
floor_thickness = 2.0

# Arm parameters
arm_length = 100.0
arm_width = 6.0
arm_height = 8.0
arm_hole_dia = 3.0

# Hex Grid parameters
hex_circum_dia = 14.0  # Diameter across corners
hex_spacing = 3.0      # Material thickness between hexes
# Calculate spacing offsets
dx = (hex_circum_dia * 0.866025) + (hex_spacing * 0.866025) * 1.5 # X spacing approx
dy = (hex_circum_dia * 0.75) + hex_spacing # Y spacing

# --- 1. Create Main Tray Body ---
# Base block
result = cq.Workplane("XY").box(tray_width, tray_length, tray_height)

# Create the inner pocket (Floor and Side Walls)
# We leave material at the ends (frames)
frame_thickness = 5.0 
pocket_width = tray_width - (2 * rail_width)
pocket_length = tray_length - (2 * frame_thickness)

result = (result.faces(">Z").workplane()
          .rect(pocket_width, pocket_length)
          .cutBlind(-(tray_height - floor_thickness)))

# --- 2. Add Rail Details (Side Grooves) ---
# Create a slot running along the length on the outside faces
groove_height = 4.0
groove_depth = 1.5

# Right side groove (+X)
result = (result.faces(">X").workplane()
          .rect(tray_length, groove_height)
          .cutBlind(-groove_depth))

# Left side groove (-X)
result = (result.faces("<X").workplane()
          .rect(tray_length, groove_height)
          .cutBlind(-groove_depth))

# --- 3. Create Hexagonal Grid Cutout ---
# Pattern: Triangle shape pointing towards the back (+Y)
# Row configuration from back to front: 1, 2, 3, 4 hexes
hex_points = []
start_y = 35.0  # Start position towards the back
rows = [1, 2, 3, 4]

# Manual hex positioning for triangular layout
hex_h_spacing = (hex_circum_dia * 0.866025) + 2.0 # Horizontal spacing (width + gap)
hex_v_spacing = (hex_circum_dia * 0.75) + 2.0     # Vertical spacing

for r_idx, count in enumerate(rows):
    row_y = start_y - (r_idx * hex_v_spacing)
    # Center the row in X
    row_width_total = (count - 1) * hex_h_spacing
    start_x = -row_width_total / 2.0
    
    for c_idx in range(count):
        pt_x = start_x + (c_idx * hex_h_spacing)
        hex_points.append((pt_x, row_y))

# Cut the hexagons through the floor
# We select the floor face or cut from top through all
result = (result.faces(">Z").workplane()
          .pushPoints(hex_points)
          .polygon(6, hex_circum_dia)
          .cutThruAll())

# --- 4. Create Extending Arm ---
# The arm extends from the front-left corner (-X, -Y)
arm_x_pos = -tray_width/2 + rail_width/2
arm_y_pos = -tray_length/2 - arm_length/2
arm_z_pos = 0

arm = (cq.Workplane("XY")
       .box(arm_width, arm_length, arm_height)
       .translate((arm_x_pos, arm_y_pos, arm_z_pos)))

# Add hole to the arm near the end
arm = (arm.faces("-X").workplane()
       .center(0, -arm_length/2 + 10) # Position relative to face center
       .circle(arm_hole_dia / 2)
       .cutThruAll())

# Union the arm with the main body
result = result.union(arm)

# --- 5. Add Corner Details (Latches/Stops) ---
# Small blocks at the back corners of the rails to simulate the molded end-caps
cap_size = rail_width + 1.0
cap_len = 8.0
cap_h = tray_height + 1.0

# Back Left Cap
cap_bl = (cq.Workplane("XY")
          .box(cap_size, cap_len, cap_h)
          .translate((-tray_width/2 + rail_width/2, tray_length/2 - cap_len/2, 0.5)))

# Back Right Cap
cap_br = (cq.Workplane("XY")
          .box(cap_size, cap_len, cap_h)
          .translate((tray_width/2 - rail_width/2, tray_length/2 - cap_len/2, 0.5)))

result = result.union(cap_bl).union(cap_br)

# --- 6. Final Fillets (Optional, for aesthetics) ---
# Fillet vertical edges of the frame for a molded look
# Selecting vertical edges on the outer boundary
try:
    result = result.edges("|Z").filter(lambda e: e.BoundingBox().xmax > tray_width/2 - 5 or e.BoundingBox().xmin < -tray_width/2 + 5).fillet(0.5)
except:
    pass # Skip if selection is too complex
