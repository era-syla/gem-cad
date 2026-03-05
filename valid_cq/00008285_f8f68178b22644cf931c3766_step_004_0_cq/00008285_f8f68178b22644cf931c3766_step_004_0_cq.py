import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_length = 250.0
base_width = 110.0
base_height = 20.0

# Key dimensions
key_size = 15.0  # Square key size
key_height = 6.0
key_spacing_x = 22.0 # Center-to-center spacing
key_spacing_y = 22.0 # Center-to-center spacing

# Space bar dimensions
space_bar_length = 4.0 * key_spacing_x + key_size # Spans approx 5 key slots
space_bar_width = key_size

# Layout configuration
rows = 4
cols = 10  # Standard keys

# --- Solid Modeling ---

# 1. Create the main base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Create the grid of standard keys
# Calculate the starting position to center the keys
grid_width = (cols - 1) * key_spacing_x
grid_depth = (rows - 1) * key_spacing_y

start_x = -grid_width / 2.0
start_y = -grid_depth / 2.0

# Create a single key shape to reuse
key_shape = cq.Workplane("XY").box(key_size, key_size, key_height).val()

keys = []

# Generate positions for the standard keys
# We will skip the keys where the spacebar goes
# Looking at the image, the spacebar is in the top row (visually furthest back), 
# spanning roughly the left-center section.
# Actually, standard keyboards have spacebars at the bottom. 
# Let's interpret the image:
# Row 0 (bottom-most in isometric view): 10 keys
# Row 1: 10 keys
# Row 2: 10 keys
# Row 3 (top-most in isometric view): A long bar on the left, then some keys on the right.

# Let's define the grid relative to the top face of the base
top_face = base.faces(">Z").workplane()

# Loop through the grid
for r in range(rows):
    # Y position: row 0 is at -y, row 3 is at +y
    y_pos = -((rows-1) * key_spacing_y / 2) + r * key_spacing_y
    
    # Determine columns for this row
    if r == 3: # The top row in the image containing the spacebar-like key
        # Create the long key
        # It looks like it takes up the first 5 spots roughly
        long_key_x = -((cols-1) * key_spacing_x / 2) + 2 * key_spacing_x # Centered over first 5 slots
        
        long_key = (
            top_face
            .center(long_key_x, y_pos)
            .box(space_bar_length, space_bar_width, key_height, combine=False)
        )
        keys.append(long_key)
        
        # Create the remaining standard keys in this row
        for c in range(5, cols):
            x_pos = -((cols-1) * key_spacing_x / 2) + c * key_spacing_x
            key = (
                top_face
                .center(x_pos, y_pos)
                .box(key_size, key_size, key_height, combine=False)
            )
            keys.append(key)
            
    else:
        # Full rows of standard keys
        for c in range(cols):
            x_pos = -((cols-1) * key_spacing_x / 2) + c * key_spacing_x
            key = (
                top_face
                .center(x_pos, y_pos)
                .box(key_size, key_size, key_height, combine=False)
            )
            keys.append(key)

# 3. Combine everything
result = base
for k in keys:
    result = result.union(k)

# Optional: Add fillets to the base for a smoother look
result = result.edges("|Z").fillet(2.0)
result = result.edges("<Z").fillet(2.0)

# Export or Render
if "show_object" in locals():
    show_object(result)