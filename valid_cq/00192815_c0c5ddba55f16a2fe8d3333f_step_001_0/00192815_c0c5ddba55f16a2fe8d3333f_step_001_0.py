import cadquery as cq

# ==========================================
# 1. Parameters & Dimensions
# ==========================================
# Ring geometry
ring_outer_radius = 42.0
ring_inner_radius = 34.0
thickness = 6.0

# Arrow / Logo geometry
# Defining vertices counter-clockwise starting from the right tip
# Coordinates approximated to match the image proportions
p_tip = (80, 0)            # Rightmost tip
p_wing_top = (25, 50)      # Top wing corner
p_tail_top_out = (-75, 28) # Top tail outer tip
p_tail_top_in = (-75, 10)  # Top tail inner corner
p_crotch = (15, 0)         # Central inner junction
p_tail_bot_in = (-75, -10) # Bottom tail inner corner
p_tail_bot_out = (-75, -28)# Bottom tail outer tip
p_wing_bot = (25, -50)     # Bottom wing corner

logo_pts = [
    p_tip, p_wing_top, p_tail_top_out, 
    p_tail_top_in, p_crotch, p_tail_bot_in, 
    p_tail_bot_out, p_wing_bot
]

# Fillet radii
corner_radius_small = 2.0  # For tips
corner_radius_large = 4.0  # For wing corners
edge_fillet = 1.0          # For the top 3D edges

# ==========================================
# 2. Geometry Construction
# ==========================================

# -- Construct the Arrow Shape --
# Using a Sketch to define the polygon and apply 2D fillets
arrow_sketch = (
    cq.Sketch()
    .polygon(logo_pts)
    # Fillet the convex corners. We select vertices by their position.
    # Exclude the 'crotch' (15,0) to keep it sharp/defined.
    .vertices(">X").fillet(corner_radius_small)       # Right tip
    .vertices(">Y").fillet(corner_radius_large)       # Top wing
    .vertices("<Y").fillet(corner_radius_large)       # Bottom wing
    .vertices("<X").fillet(corner_radius_small)       # All 4 tail points at X=-75
)

# Extrude the arrow
arrow_solid = cq.Workplane("XY").placeSketch(arrow_sketch).extrude(thickness)

# -- Construct the Ring Shape --
# Create a hollow cylinder
ring_solid = (
    cq.Workplane("XY")
    .circle(ring_outer_radius)
    .circle(ring_inner_radius)
    .extrude(thickness)
)

# -- Combine Elements --
# Boolean Union of the arrow and the ring
result = arrow_solid.union(ring_solid)

# -- Finishing --
# Clean the geometry to merge coplanar faces resulting from the union
result = result.clean()

# Apply a fillet to all edges on the top face for the smooth, finished look
result = result.faces(">Z").edges().fillet(edge_fillet)