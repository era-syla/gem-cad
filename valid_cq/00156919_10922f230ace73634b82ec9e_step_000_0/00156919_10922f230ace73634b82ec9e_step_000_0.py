import cadquery as cq

# Parametric dimensions for the L-shaped profile (Angle Iron)
length = 200.0        # Total length of the extrusion
leg_v_height = 60.0   # Height of the vertical leg
leg_h_width = 30.0    # Width of the horizontal leg
thickness = 5.0       # Thickness of the material
inner_radius = 5.0    # Fillet radius for the inner corner
toe_radius = 2.0      # Fillet radius for the tips of the legs

# 1. Sketch the L-profile on the XY plane
# The origin (0,0) corresponds to the outer corner of the angle.
# Coordinates follow the path: Outer Corner -> Horizontal Tip -> Inner Horizontal -> Inner Corner -> Inner Vertical -> Vertical Tip -> Close
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_h_width, 0)
    .lineTo(leg_h_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg_v_height)
    .lineTo(0, leg_v_height)
    .close()
    .extrude(length)
)

# 2. Apply Fillet to the inner corner
# Select the edge closest to the theoretical inner intersection point (thickness, thickness) along the extrusion
inner_edge_selector = cq.NearestToPointSelector((thickness, thickness, length / 2))
result = result.edges(inner_edge_selector).fillet(inner_radius)

# 3. Apply Fillets to the "toes" (the tips of the legs)
# Select the edges at the inner corners of the leg tips to round them off
toe_h_selector = cq.NearestToPointSelector((leg_h_width, thickness, length / 2))
toe_v_selector = cq.NearestToPointSelector((thickness, leg_v_height, length / 2))

# Apply fillets to both toes
result = result.edges(toe_h_selector).fillet(toe_radius)
result = result.edges(toe_v_selector).fillet(toe_radius)