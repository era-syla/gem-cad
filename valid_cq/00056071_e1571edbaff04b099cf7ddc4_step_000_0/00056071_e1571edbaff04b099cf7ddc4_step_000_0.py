import cadquery as cq
import math

# Dimensions for the chess pawn
base_diameter = 30.0
base_height = 4.0
base_fillet_height = 2.0
stem_bottom_diameter = 26.0
neck_diameter = 14.0
neck_height = 30.0  # Length of the stem
collar_diameter = 24.0
collar_thickness = 3.0
head_diameter = 18.0

# Calculate radii
r_base = base_diameter / 2.0
r_stem_bot = stem_bottom_diameter / 2.0
r_neck = neck_diameter / 2.0
r_collar = collar_diameter / 2.0
r_head = head_diameter / 2.0
r_collar_top_connection = 10.0 / 2.0

# Initial setup
# We construct a profile in the XZ plane and revolve it around Z
# Start at the origin (0,0,0)
current_y = 0.0

# 1. Base construction
# Draw line out to base radius
p = cq.Workplane("XZ").moveTo(0, 0).lineTo(r_base, 0)

# Base vertical edge
current_y += base_height
p = p.lineTo(r_base, current_y)

# Chamfer/Transition to stem
# Moves slightly inward and upward
current_y += base_fillet_height
p = p.lineTo(r_stem_bot, current_y)

# 2. Stem/Body
# Spline curve from bottom of stem to the neck (just below collar)
# The shape is slightly concave
stem_top_y = current_y + neck_height
mid_y = (current_y + stem_top_y) / 2
mid_x = (r_stem_bot + r_neck) / 2 - 2.0 # Inset control point for concave curve

p = p.spline([(mid_x, mid_y), (r_neck, stem_top_y)], includeCurrent=True)
current_y = stem_top_y

# 3. Collar
# Flare out to collar radius (underside of collar)
p = p.lineTo(r_collar, current_y)

# Vertical edge of collar
current_y += collar_thickness
p = p.lineTo(r_collar, current_y)

# Slope inward on top of collar to meet the head
current_y += 1.0 # Small slope height
p = p.lineTo(r_collar_top_connection, current_y)

# 4. Head (Sphere)
# We need to calculate the center of the sphere to ensure it connects smoothly
# The sphere sits on the connection radius `r_collar_top_connection` at height `current_y`
# Equation of circle: x^2 + (y - Cy)^2 = R^2
# At connection: r_conn^2 + (y_conn - Cy)^2 = r_head^2
# Solve for Cy (Center Y)
dy = math.sqrt(r_head**2 - r_collar_top_connection**2)
center_y = current_y + dy
top_y = center_y + r_head

# Define arc for the head
# We use a three-point arc: start (current), mid (equator), end (top pole)
p = p.threePointArc((r_head, center_y), (0, top_y))

# 5. Finalize
# Close the profile back to the origin
p = p.close()

# Revolve the profile 360 degrees to create the solid
result = p.revolve()