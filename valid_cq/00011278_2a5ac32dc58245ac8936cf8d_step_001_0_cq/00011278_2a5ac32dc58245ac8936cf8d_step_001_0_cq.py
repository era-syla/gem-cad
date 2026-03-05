import cadquery as cq

# --- Parameters ---
width = 60.0       # Width of the main body
depth = 40.0       # Depth of the main body
height = 80.0      # Height of the main body (excluding flanges)
wall_thickness = 2.0  # Thickness of the walls (if it were hollow, though the image looks solid or closed)
corner_radius = 4.0   # Radius for rounded corners of the main body

flange_extension = 2.0  # How much the top/bottom flanges stick out past the body
flange_height = 2.0     # Thickness of the top and bottom flanges
flange_radius = corner_radius + flange_extension # Radius of flange corners

# Groove parameters for the top surface
groove_count = 12
groove_width = 0.5
groove_depth = 0.5
groove_margin = 4.0 # Distance from edge where grooves start/stop
# Calculate spacing. We distribute lines across the depth.
# We want to span 'depth - 2*groove_margin'
groove_span = depth - 2 * groove_margin
groove_pitch = groove_span / (groove_count - 1)


# --- Geometry Construction ---

# 1. Main Body
# Create a rounded rectangle extrusion
main_body = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
    .edges("|Z").fillet(corner_radius)
)

# 2. Bottom Flange
# Create a larger rounded rectangle at the bottom
bottom_flange = (
    cq.Workplane("XY")
    .rect(width + 2*flange_extension, depth + 2*flange_extension)
    .extrude(flange_height)
    .edges("|Z").fillet(flange_radius)
)

# 3. Top Flange
# Create a similar flange at the top
top_flange_wp = cq.Workplane("XY").workplane(offset=height + flange_height)
top_flange = (
    top_flange_wp
    .rect(width + 2*flange_extension, depth + 2*flange_extension)
    .extrude(-flange_height) # Extrude downwards to meet the main body
    .edges("|Z").fillet(flange_radius)
)

# 4. Combine basic shapes
# We shift the main body up by flange_height so it sits on the bottom flange
main_body = main_body.translate((0, 0, flange_height))

# Union the parts
result = bottom_flange.union(main_body).union(top_flange)

# 5. Add Grooves to Top Surface
# We cut thin rectangular slots into the top face
# The top face is at z = height + flange_height
top_face_z = height + flange_height

# We will iterate to create the cuts
for i in range(groove_count):
    # Calculate y-position for this groove centered around 0
    # Start at -groove_span/2, end at +groove_span/2
    y_pos = -groove_span/2 + i * groove_pitch
    
    # We want the groove lines to run along the Width (X axis)
    # Length of groove = width - 2*groove_margin
    groove_length = width - 2 * groove_margin
    
    # Small detail: The image shows little widened ends on the grooves. 
    # Let's approximate the main straight lines first.
    # To keep it simple but accurate to the visual of parallel lines:
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=top_face_z)
        .center(0, y_pos)
        .rect(groove_length, groove_width)
        .extrude(-groove_depth)
    )
    
    # Optional: Add the small squares/rectangles at the ends of the grooves seen in the image
    # These look like little connector pads or endpoints.
    end_feature_size = groove_width * 3.0
    end_feature_depth = groove_depth
    
    # Left end feature
    cutter_end_left = (
        cq.Workplane("XY")
        .workplane(offset=top_face_z)
        .center(-groove_length/2, y_pos)
        .rect(end_feature_size, end_feature_size)
        .extrude(-end_feature_depth)
    )
    
    # Right end feature
    cutter_end_right = (
        cq.Workplane("XY")
        .workplane(offset=top_face_z)
        .center(groove_length/2, y_pos)
        .rect(end_feature_size, end_feature_size)
        .extrude(-end_feature_depth)
    )
    
    result = result.cut(cutter).cut(cutter_end_left).cut(cutter_end_right)

# Export or visualization would happen here normally
# show_object(result)