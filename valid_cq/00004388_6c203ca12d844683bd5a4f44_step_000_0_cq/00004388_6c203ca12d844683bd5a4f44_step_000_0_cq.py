import cadquery as cq

# Parameters for the grid structure
arrow_shaft_length = 80.0
arrow_shaft_width = 4.0
arrow_shaft_height = 4.0

arrow_head_length = 15.0
arrow_head_width = 15.0
arrow_head_base_width = 4.0 # Should match shaft width for smooth transition usually, or slightly larger

cross_bar_length = 70.0 # Spans across the three arrows
cross_bar_width = 4.0
cross_bar_height = 4.0

# Spacing
arrow_spacing = 20.0
cross_bar_spacing = 20.0
num_arrows = 3
num_cross_bars = 3

def create_arrow():
    """Creates a single arrow geometry."""
    # Create the shaft
    shaft = cq.Workplane("XY").box(arrow_shaft_length, arrow_shaft_width, arrow_shaft_height)
    
    # Create the arrow head
    # We'll draw a triangle profile and extrude it
    # The tip should be at the end of the shaft
    
    # Coordinates for the arrow head polygon (pointing in +X)
    # The shaft ends at x = arrow_shaft_length / 2
    tip_x = (arrow_shaft_length / 2) + arrow_head_length
    base_x = (arrow_shaft_length / 2)
    
    p1 = (tip_x, 0)
    p2 = (base_x, arrow_head_width / 2)
    p3 = (base_x, -arrow_head_width / 2)
    
    arrow_head = (
        cq.Workplane("XY")
        .polyline([p1, p2, p3, p1])
        .close()
        .extrude(arrow_shaft_height)
    )
    # Center the extrusion vertically to match the shaft (which is centered by .box)
    arrow_head = arrow_head.translate((0, 0, -arrow_shaft_height / 2))
    
    return shaft.union(arrow_head)

def create_grid():
    """Assembles the arrows and cross bars into a grid."""
    
    grid = cq.Assembly()
    
    # Create and place arrows
    base_arrow = create_arrow()
    
    arrows_union = None
    
    for i in range(num_arrows):
        # Calculate Y offset to center the group around Y=0
        y_offset = (i - (num_arrows - 1) / 2) * arrow_spacing
        moved_arrow = base_arrow.translate((0, y_offset, 0))
        
        if arrows_union is None:
            arrows_union = moved_arrow
        else:
            arrows_union = arrows_union.union(moved_arrow)

    # Create and place cross bars
    cross_bar = cq.Workplane("XY").box(cross_bar_width, cross_bar_length, cross_bar_height)
    
    final_shape = arrows_union
    
    for i in range(num_cross_bars):
        # Calculate X offset. We want them spaced out along the shaft.
        # Let's position them relative to the center of the shaft length, but shifted back a bit from the head
        # The shaft goes from -L/2 to L/2. Head starts at L/2.
        # Let's center the grid of crossbars slightly behind the arrow heads.
        
        # Center of the crossbar group
        center_x_offset = 0 
        
        x_offset = (i - (num_cross_bars - 1) / 2) * cross_bar_spacing + center_x_offset
        moved_bar = cross_bar.translate((x_offset, 0, 0))
        
        if final_shape is None:
            final_shape = moved_bar
        else:
            final_shape = final_shape.union(moved_bar)
            
    return final_shape

# Generate the final model
result = create_grid()