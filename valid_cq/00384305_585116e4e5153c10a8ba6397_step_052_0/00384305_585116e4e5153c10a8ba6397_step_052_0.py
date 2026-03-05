import cadquery as cq

# --- Parameters ---
thickness = 2.0
slot_width = 12.0
finger_width = 10.0
slot_straight_len = 25.0  # Length of the straight part of the slot
back_margin = 15.0        # Solid material behind the slots for brackets
plate_back_len = 50.0     # Solid material behind slots for the flat plate
bracket_height = 35.0     # Height of the vertical flange
hole_diam = 3.5

def create_component(num_slots, part_type):
    """
    Creates a slotted component.
    part_type: 'bracket' (L-shape) or 'plate' (flat)
    """
    # Calculate overall width
    # Width = n*slot + (n+1)*finger
    total_width = (num_slots * slot_width) + ((num_slots + 1) * finger_width)
    
    # Calculate depth based on type
    # Total slot depth = straight length + radius (half width)
    slot_total_depth = slot_straight_len + (slot_width / 2)
    
    if part_type == 'bracket':
        body_depth = slot_total_depth + back_margin
    else:
        body_depth = slot_total_depth + plate_back_len
        
    # --- 1. Base Horizontal Geometry ---
    # Create the main plate centered on X, with the back edge at Y=0
    # Extending to -Y direction
    
    # Center of box in Y needs to be at -body_depth/2 to align back edge to 0
    base = (cq.Workplane("XY")
            .workplane(offset=0)
            .moveTo(0, -body_depth / 2)
            .box(total_width, body_depth, thickness)
           )
    
    # --- 2. Cut Slots ---
    # Slots start from the front edge (Y = -body_depth)
    front_edge_y = -body_depth
    
    # Calculate starting X position (leftmost slot center)
    # Left edge is at -total_width/2
    start_x = -total_width/2 + finger_width + slot_width/2
    
    for i in range(num_slots):
        x_pos = start_x + i * (finger_width + slot_width)
        
        # Cut the straight rectangular portion
        # Rect centered at y = front_edge_y + length/2
        rect_center_y = front_edge_y + slot_straight_len / 2
        base = (base.faces(">Z").workplane()
                .moveTo(x_pos, rect_center_y)
                .rect(slot_width, slot_straight_len)
                .cutThruAll()
               )
        
        # Cut the circular end
        circle_center_y = front_edge_y + slot_straight_len
        base = (base.faces(">Z").workplane()
                .moveTo(x_pos, circle_center_y)
                .circle(slot_width / 2)
                .cutThruAll()
               )

    # --- 3. Add Type-Specific Features ---
    if part_type == 'bracket':
        # Create Vertical Flange (L-Bracket)
        # Attached to the back edge (Y=0), bending downwards
        # Dimensions: Width x Height x Thickness
        
        # We model this as a box attached to the back
        # Position X=0
        # Position Y: We want the back face of the flange to be at Y=0? 
        # Actually, let's overlap it slightly or make it flush. 
        # Standard sheet metal bend: The flange thickness sits behind the bend line.
        # Let's position the flange box such that its front face is at Y=0 (adding to depth) 
        # or inside face at -thickness (maintaining depth).
        # Let's align back of flange to Y=0. Center Y = -thickness/2.
        
        # Position Z: Top of flange flush with top of plate.
        # Plate top is at +thickness/2.
        # Flange box height is bracket_height.
        # Flange center Z = thickness/2 - bracket_height/2.
        
        flange = (cq.Workplane("XZ")
                  .workplane(offset=-thickness/2)
                  .moveTo(0, thickness/2 - bracket_height/2)
                  .box(total_width, bracket_height, thickness)
                 )
        
        # Union the flange
        result_part = base.union(flange)
        
        # Add Mounting Holes to Vertical Flange
        # Holes on the back face (XZ plane)
        # Position them near the bottom corners
        hole_z = thickness/2 - bracket_height + 8 # 8mm from bottom
        hole_x_offset = total_width/2 - 10
        
        result_part = (result_part.faces(">Y").workplane()
                       .pushPoints([(-hole_x_offset, hole_z), (hole_x_offset, hole_z)])
                       .hole(hole_diam)
                      )
                      
    else: # part_type == 'plate'
        result_part = base
        
        # Add Mounting Holes to the back solid area
        # Area is between Y=0 and Y=-(body_depth - slot_total_depth) approx
        # Let's center them in the solid margin area
        margin_center_y = -plate_back_len / 2
        hole_x_spacing = total_width/2 - 15
        hole_y_spacing = 15
        
        result_part = (result_part.faces(">Z").workplane()
                       .pushPoints([
                           (-hole_x_spacing, margin_center_y + hole_y_spacing/2),
                           (hole_x_spacing, margin_center_y + hole_y_spacing/2),
                           (-hole_x_spacing, margin_center_y - hole_y_spacing/2),
                           (hole_x_spacing, margin_center_y - hole_y_spacing/2)
                       ])
                       .hole(hole_diam)
                      )
    
    return result_part

# --- Create the Assembly ---

# Left Part: L-Bracket with 2 slots
part_left = create_component(num_slots=2, part_type='bracket')
# Position: Move to the left
part_left = part_left.translate((-90, 0, 0))

# Middle Part: Flat Plate with 3 slots
part_mid = create_component(num_slots=3, part_type='plate')
# Position: Center (offset slightly in Y to align fronts if desired, but 0 is fine)
# The image shows them aligned roughly by the back or mounting plane. 
# Our origin is the back edge (Y=0) for all parts.
part_mid = part_mid.translate((0, 0, 0))

# Right Part: L-Bracket with 3 slots
part_right = create_component(num_slots=3, part_type='bracket')
# Position: Move to the right
part_right = part_right.translate((100, 0, 0))

# Combine all into one result object
result = part_left.union(part_mid).union(part_right)