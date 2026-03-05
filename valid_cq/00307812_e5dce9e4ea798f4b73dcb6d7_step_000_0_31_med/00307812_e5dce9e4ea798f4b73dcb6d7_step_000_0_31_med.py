import cadquery as cq

def create_ambiguous_text_block():
    # Parameters for the block
    depth = 200.0
    font_size = 100.0
    
    # Z-axis extrusion (Top view - letter 'S')
    # Normal is +Z. We start at Z = -depth/2 and extrude up by depth.
    z_solid = cq.Workplane("XY", origin=(0, 0, -depth/2)).text(
        "S", font_size, depth, kind="bold", halign="center", valign="center"
    )
    
    # Y-axis extrusion (Front view - letter 'E')
    # Normal is +Y. We start at Y = -depth/2 and extrude along +Y by depth.
    y_solid = cq.Workplane("XZ", origin=(0, -depth/2, 0)).text(
        "E", font_size, depth, kind="bold", halign="center", valign="center"
    )
    
    # X-axis extrusion (Side view - letter 'C')
    # Normal is +X. We start at X = -depth/2 and extrude along +X by depth.
    x_solid = cq.Workplane("YZ", origin=(-depth/2, 0, 0)).text(
        "C", font_size, depth, kind="bold", halign="center", valign="center"
    )
    
    # Generate the final shape by intersecting all three extrusions
    intersection = z_solid.intersect(y_solid).intersect(x_solid)
    
    return intersection

result = create_ambiguous_text_block()