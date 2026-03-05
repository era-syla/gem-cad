import cadquery as cq

# Parameters derived from image analysis
labels = ["3.25", "3.20", "3.15", "3.10"]
spacing = 16.0           # Distance between centers
handle_diam = 4.0        # Diameter of the lower shaft
handle_length = 35.0     # Length of the lower shaft
head_diam = 10.0         # Diameter of the top cylinder
head_height = 8.0        # Height of the top cylinder
bridge_width = 3.0       # Thickness of the connecting tab
bridge_height = 3.0      # Height of the connecting tab
text_size = 3.2          # Size of the embossed text
text_depth = 1.0         # Extrusion depth of text
text_font = "Arial"      # Font family

# Initialize the final result container
result = None

for i, label in enumerate(labels):
    # Calculate X coordinate for the current gauge
    x_pos = i * spacing
    
    # 1. Create Handle
    # Vertical cylinder along Z-axis
    handle = (
        cq.Workplane("XY")
        .circle(handle_diam / 2.0)
        .extrude(handle_length)
        .translate((x_pos, 0, 0))
    )
    
    # 2. Create Head
    # Cylinder sitting on top of the handle
    head = (
        cq.Workplane("XY")
        .workplane(offset=handle_length)
        .circle(head_diam / 2.0)
        .extrude(head_height)
        .translate((x_pos, 0, 0))
    )
    
    # 3. Create Embossed Text
    # We position the text on the "front" face (XZ plane looking at -Y)
    # Vertical center of the head
    head_z_center = handle_length + (head_height / 2.0)
    
    # Y offset to place text on the surface.
    # Radius of head is head_diam/2. 
    # We position text slightly inside (-radius + overlap) to ensure valid boolean union.
    overlap = 0.2
    y_surface_pos = -(head_diam / 2.0) + overlap
    
    # Create text on XZ plane and extrude in negative Y direction (outwards from front)
    text_obj = (
        cq.Workplane("XZ")
        .text(label, text_size, -text_depth, font=text_font)
        .translate((x_pos, y_surface_pos, head_z_center))
    )
    
    # Assemble the single gauge
    single_gauge = handle.union(head).union(text_obj)
    
    # Union with the accumulating result
    if result is None:
        result = single_gauge
    else:
        result = result.union(single_gauge)
        
    # 4. Create Connecting Bridge
    # Adds a rectangular tab between the current head and the previous one
    if i > 0:
        prev_x_pos = (i - 1) * spacing
        bridge_x_center = (x_pos + prev_x_pos) / 2.0
        
        # Calculate bridge length to span the gap with overlap
        bridge_len = spacing - head_diam + 1.0
        
        bridge = (
            cq.Workplane("XY")
            .box(bridge_len, bridge_width, bridge_height)
            .translate((bridge_x_center, 0, head_z_center))
        )
        
        result = result.union(bridge)

# result now contains the full 3D geometry