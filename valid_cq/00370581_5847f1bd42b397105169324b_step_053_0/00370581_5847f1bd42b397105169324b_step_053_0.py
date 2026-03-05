import cadquery as cq

def create_tool_holder(num_slots, is_l_bracket):
    """
    Creates a parametric tool holder bracket.
    
    :param num_slots: Number of U-shaped slots
    :param is_l_bracket: True for L-shaped wall bracket, False for flat plate
    """
    # Dimensions
    thickness = 3.0
    depth = 90.0
    flange_height = 40.0
    slot_width = 22.0
    finger_width = 18.0
    slot_length = 50.0
    hole_dia = 4.5
    
    # Calculate total width based on slots and fingers
    total_width = (num_slots * slot_width) + ((num_slots + 1) * finger_width)
    
    # 1. Generate Base Shape
    if is_l_bracket:
        # Create L-profile extruded along X axis
        # Define points on YZ plane (Local Y=Global Y, Local Z=Global Z)
        pts = [
            (0, 0),
            (depth, 0),
            (depth, thickness),
            (thickness, thickness),
            (thickness, flange_height),
            (0, flange_height)
        ]
        # Extrude along X
        base = cq.Workplane("YZ").polyline(pts).close().extrude(total_width)
        # Center the part on X axis
        base = base.translate((-total_width / 2, 0, 0))
    else:
        # Create Flat Plate centered on XY plane
        base = cq.Workplane("XY").box(total_width, depth, thickness)
        # Align coordinate system to match L-bracket (Back edge at Y=0, Bottom at Z=0)
        base = base.translate((0, depth / 2, thickness / 2))

    # 2. Cut U-Shaped Slots
    # Select top face (Z = thickness)
    # Use ProjectedOrigin to keep (0,0) at the global origin projection
    wp_slots = base.faces(">Z").workplane(centerOption="ProjectedOrigin")
    
    # Calculate starting X position
    current_x = -total_width / 2 + finger_width + slot_width / 2
    
    for _ in range(num_slots):
        r = slot_width / 2
        # Center Y of the arc part of the slot
        cy = depth - slot_length + r
        
        # Define points for the U-shape path
        p_front_left = (current_x - r, depth + 1.0) # Start slightly outside
        p_arc_start = (current_x - r, cy)
        p_arc_mid = (current_x, cy - r)           # Bottom of U
        p_arc_end = (current_x + r, cy)
        p_front_right = (current_x + r, depth + 1.0)
        
        # Draw the slot profile (Wire)
        wp_slots = (wp_slots
                    .moveTo(*p_front_left)
                    .lineTo(*p_arc_start)
                    .threePointArc(p_arc_mid, p_arc_end)
                    .lineTo(*p_front_right)
                    .lineTo(*p_front_left)
                    .close())
        
        # Move to next slot position
        current_x += (slot_width + finger_width)
        
    # Cut all accumulated wires through the part
    base = wp_slots.cutThruAll()
    
    # 3. Create Mounting Holes
    hole_margin = 15.0
    
    if is_l_bracket:
        # Holes on the vertical back flange (Face at Y=0)
        # Select back face (Normal points to -Y)
        wp_holes = base.faces("<Y").workplane(centerOption="ProjectedOrigin")
        
        # Hole height on flange
        h_z = flange_height * 0.6
        
        pts = [
            (-total_width/2 + hole_margin, h_z),
            (total_width/2 - hole_margin, h_z)
        ]
        base = wp_holes.pushPoints(pts).hole(hole_dia)
    else:
        # Holes on the flat plate surface, near the back edge
        wp_holes = base.faces(">Z").workplane(centerOption="ProjectedOrigin")
        
        # Hole position from back edge
        h_y = 15.0
        
        pts = [
            (-total_width/2 + hole_margin, h_y),
            (total_width/2 - hole_margin, h_y)
        ]
        base = wp_holes.pushPoints(pts).hole(hole_dia)
        
    return base

# Create the assembly components as shown in the image
# Left: 2 slots, L-bracket
left_part = create_tool_holder(num_slots=2, is_l_bracket=True).translate((-160, 0, 0))

# Center: 3 slots, Flat plate
center_part = create_tool_holder(num_slots=3, is_l_bracket=False).translate((0, 0, 0))

# Right: 3 slots, L-bracket
right_part = create_tool_holder(num_slots=3, is_l_bracket=True).translate((160, 0, 0))

# Combine into single result
result = left_part.union(center_part).union(right_part)