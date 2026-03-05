import cadquery as cq

# Geometric Parameters
thickness = 6.0
total_length = 140.0
handle_width = 24.0
max_width = 60.0
opening_radius = 16.0
tip_protrusion = 22.0  # Distance from opening center to tip front
tip_face_height = 8.0  # Height of the vertical flat face at the tip

# Derived Parameters
handle_radius = handle_width / 2.0
# Calculate X coordinate for the center of the handle end radius
# Total length = tip_protrusion (negative X) + length along positive X
# length along positive X = total_length - tip_protrusion
x_handle_end = total_length - tip_protrusion - handle_radius
x_handle_straight_start = 50.0  # Where the handle becomes parallel

# Key coordinates
# Origin (0,0) is at the center of the U-shaped opening
p_tip_in_top = (-tip_protrusion, opening_radius)
p_tip_out_top = (-tip_protrusion, opening_radius + tip_face_height)
p_opening_top = (0, opening_radius)
p_opening_bottom = (0, -opening_radius)
p_tip_in_bot = (-tip_protrusion, -opening_radius)
p_tip_out_bot = (-tip_protrusion, -(opening_radius + tip_face_height))

# Spline control points for the transition curve
p_flare_top = (-5, max_width / 2.0)
p_neck_top = (x_handle_straight_start * 0.5, handle_radius + 3.0)
p_handle_start_top = (x_handle_straight_start, handle_radius)

# Generate the model
result = (
    cq.Workplane("XY")
    .moveTo(*p_tip_in_top)
    .lineTo(*p_tip_out_top)
    
    # Top profile curve
    .spline([p_flare_top, p_neck_top, p_handle_start_top], includeCurrent=True)
    
    # Top straight handle
    .lineTo(x_handle_end, handle_radius)
    
    # Handle end cap (180 degree arc)
    .radiusArc((x_handle_end, -handle_radius), handle_radius)
    
    # Bottom straight handle
    .lineTo(x_handle_straight_start, -handle_radius)
    
    # Bottom profile curve (mirrored points, reversed order)
    .spline([(x, -y) for x, y in [p_neck_top, p_flare_top]], includeCurrent=True)
    .spline([p_tip_out_bot], includeCurrent=True) # Ensure it hits the exact target
    
    .lineTo(*p_tip_in_bot)
    .lineTo(*p_opening_bottom)
    
    # Inner U-shape opening
    # Drawn CCW: from bottom, through back of throat, to top
    .threePointArc((opening_radius, 0), p_opening_top)
    
    .close()
    .extrude(thickness)
)

# Apply chamfers to the vertical leading edges of the tips
# Using a BoxSelector to reliably grab the vertical edges at the negative X end
result = result.edges(
    cq.selectors.BoxSelector(
        (-tip_protrusion - 1, -100, -10), 
        (-tip_protrusion + 1, 100, 10)
    )
).chamfer(2.5)