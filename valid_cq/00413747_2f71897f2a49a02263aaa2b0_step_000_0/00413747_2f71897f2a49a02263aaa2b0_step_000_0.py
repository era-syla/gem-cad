import cadquery as cq

# --- Dimensions & Parameters ---
body_width = 50.0
body_height = 65.0
thickness = 4.0
rim_width = 2.5        # Width of the border around the grid
groove_depth = 0.6     # Depth of the texture cuts
groove_width = 1.0     # Width of the grid lines
groove_spacing = 12.0  # Spacing between grid lines

# --- 1. Pineapple Body ---
# Create the main elliptical body
body = cq.Workplane("XY").ellipse(body_width/2.0, body_height/2.0).extrude(thickness)

# --- 2. Texture Pattern (Grid) ---
def create_grid_bars(angle):
    """Creates a set of parallel bars rotated by the given angle."""
    wp = cq.Workplane("XY")
    # Generate bars to cover the entire potential area
    # Range is estimated based on object diagonal
    for i in range(-6, 7):
        offset = i * groove_spacing
        # Draw a rectangle centered at the offset
        wp = wp.center(0, offset).rect(150, groove_width).center(0, -offset)
    
    # Extrude the bars and rotate
    return wp.extrude(thickness).rotate((0,0,0), (0,0,1), angle)

# Generate diagonal grids
grid_right = create_grid_bars(45)
grid_left = create_grid_bars(-45)
full_grid = grid_right.union(grid_left)

# Create a masking shape to restrict the grid to the inside of the body (leaving a rim)
mask_w = body_width - (2 * rim_width)
mask_h = body_height - (2 * rim_width)
grid_mask = cq.Workplane("XY").ellipse(mask_w/2.0, mask_h/2.0).extrude(thickness)

# Intersect grid with mask to get the final engraving tool
engraver = full_grid.intersect(grid_mask)

# Position the engraver to cut into the top surface
# Translate Z so the engraver overlaps the top of the body by groove_depth
engraver = engraver.translate((0, 0, thickness - groove_depth))

# Apply the cut to the body
textured_body = body.cut(engraver)

# --- 3. Crown (Leaves) ---
# Define the starting Y height for the crown (overlapping with body top)
y_base = (body_height / 2.0) - 5.0

# Define points for the right side of the crown (Spiky leaf shape)
# Coordinates relative to the center of the ellipse
crown_pts_right = [
    (6, y_base + 4),      # Stem base width
    (32, y_base + 2),     # Lower leaf tip (curling outward/down)
    (18, y_base + 18),    # Lower leaf axil
    (28, y_base + 35),    # Middle leaf tip
    (10, y_base + 40),    # Upper axil
    (0, y_base + 60)      # Top central tip
]

# Construct full polyline points: Center -> Right Side -> Left Side (Mirrored) -> Close
pts = [(0, y_base)]
pts.extend(crown_pts_right)
# Mirror right points for the left side (negate X, reverse order, skip top tip)
pts.extend([(-p[0], p[1]) for p in reversed(crown_pts_right[:-1])])
pts.append((0, y_base))

# Extrude the crown shape
crown = (cq.Workplane("XY")
         .polyline(pts)
         .close()
         .extrude(thickness)
         )

# Add fillets to vertical edges to smooth the leaves for an organic look
crown = crown.edges("|Z").fillet(1.5)

# --- 4. Final Assembly ---
result = textured_body.union(crown)