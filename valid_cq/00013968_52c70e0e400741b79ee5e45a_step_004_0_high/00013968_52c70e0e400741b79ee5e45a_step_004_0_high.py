import cadquery as cq

# --- Parameter Definitions ---
# Dimensions derived from standard "8-bar" logo proportions
height = 50.0          # Overall height of the letters
thickness = 5.0        # Extrusion thickness
letter_spacing = 6.0   # Gap between letters

# Stripe parameters (Scanline effect)
num_stripes = 8
stripe_pitch = height / num_stripes
stripe_fill_ratio = 0.6  # Ratio of solid bar to total pitch (approx 60% solid)
stripe_height = stripe_pitch * stripe_fill_ratio

# --- Geometry Construction ---

# 1. Letter 'I' Construction
# Simple rectangular block
i_width = 18.0
wp_i = (
    cq.Workplane("XY")
    .moveTo(i_width / 2, height / 2)
    .rect(i_width, height)
    .extrude(thickness)
)

# 2. Letter 'B' Construction
# Block with rounded outer corners and two internal cutouts
b_width = 38.0
b_start_x = i_width + letter_spacing
b_center_x = b_start_x + b_width / 2

# Create the main body of B
b_body = (
    cq.Workplane("XY")
    .moveTo(b_center_x, height / 2)
    .rect(b_width, height)
    .extrude(thickness)
    .edges("|Z and >X")  # Select vertical edges on the right side
    .fillet(12.0)        # Round the corners
)

# Create cutouts for B (Square holes with small fillets)
cutout_w = 14.0
cutout_h = 10.0
cutout_x = b_start_x + 19.0  # Horizontal center of cutout

# Top cutout
cutout_top = (
    cq.Workplane("XY")
    .moveTo(cutout_x, height * 0.72)
    .rect(cutout_w, cutout_h)
    .extrude(thickness)
    .edges("|Z")
    .fillet(2.0)
)

# Bottom cutout
cutout_bottom = (
    cq.Workplane("XY")
    .moveTo(cutout_x, height * 0.28)
    .rect(cutout_w, cutout_h)
    .extrude(thickness)
    .edges("|Z")
    .fillet(2.0)
)

# Apply cutouts to B
wp_b = b_body.cut(cutout_top).cut(cutout_bottom)

# 3. Letter 'M' Construction
# Geometric construction using a polyline to form the block 'M'
m_width = 50.0
m_start_x = b_start_x + b_width + letter_spacing
leg_width = 13.0
v_drop_outer = 18.0  # Depth of V from top for outer edge
v_drop_inner = 35.0  # Depth of V tip

# Define points for M (Counter-Clockwise starting bottom-left)
m_pts = [
    (m_start_x, 0),                                    # Bottom Left
    (m_start_x + leg_width, 0),                        # Inner Left Leg Bottom
    (m_start_x + leg_width, height - v_drop_outer),    # Inner Left V start
    (m_start_x + m_width / 2, height - v_drop_inner),  # V Bottom tip (middle)
    (m_start_x + m_width - leg_width, height - v_drop_outer), # Inner Right V start
    (m_start_x + m_width - leg_width, 0),              # Inner Right Leg Bottom
    (m_start_x + m_width, 0),                          # Bottom Right
    (m_start_x + m_width, height),                     # Top Right
    (m_start_x + m_width - leg_width, height),         # Top Right Inner
    (m_start_x + m_width / 2, height - 12),            # V Top Peak (middle)
    (m_start_x + leg_width, height),                   # Top Left Inner
    (m_start_x, height)                                # Top Left
]

wp_m = (
    cq.Workplane("XY")
    .polyline(m_pts)
    .close()
    .extrude(thickness)
)

# Union all letters into one solid base
base_letters = wp_i.union(wp_b).union(wp_m)

# 4. Create Stripe Mask
# Create a set of horizontal bars to intersect with the letters
mask_wp = cq.Workplane("XY")
total_width = m_start_x + m_width + 10 # Width covering all letters

for i in range(num_stripes):
    # Calculate center Y of each stripe
    # Stripes are arranged from bottom to top
    y_center = (i * stripe_pitch) + (stripe_height / 2)
    
    # Add rectangle to the pending wires
    # Center X is roughly middle of the whole logo
    mask_wp = mask_wp.moveTo(total_width / 2, y_center).rect(total_width + 20, stripe_height)

# Extrude the mask
stripes_solid = mask_wp.extrude(thickness)

# 5. Final Boolean Intersection
# Intersect the full letters with the stripes to get the final geometry
result = base_letters.intersect(stripes_solid)