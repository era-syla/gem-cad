import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions of the resulting assembly
wall_width = 100.0  # Total width
wall_height = 80.0  # Total height
thickness = 20.0    # Thickness of the blocks

# Grid dimensions
rows = 3
cols = 2

# Individual block dimensions (base size before puzzle features)
block_w = wall_width / cols
block_h = wall_height / rows

# Puzzle connector parameters
tab_radius = 5.0    # Radius of the circular locking tab
neck_width = 6.0    # Width of the neck connecting the tab
tab_offset = 0.0    # Offset from center of the edge (0 = centered)

def create_puzzle_piece(i, j, width, height, thick, t_rad, n_w):
    """
    Creates a single puzzle piece based on its grid position.
    
    Args:
        i (int): Row index (0 to rows-1)
        j (int): Column index (0 to cols-1)
        width (float): Base width of the block
        height (float): Base height of the block
        thick (float): Thickness of the block
        t_rad (float): Tab radius
        n_w (float): Neck width
        
    Returns:
        cq.Workplane: The solid puzzle piece
    """
    
    # Start with a base rectangle
    piece = cq.Workplane("XY").box(width, height, thick)
    
    # Helper to create a tab cutter/adder shape
    # We create a shape that represents the "male" part.
    # It consists of a neck and a circle.
    
    def make_tab_shape(r, neck_w):
        # Center of the circle part relative to the edge
        # The circle center needs to be pushed out enough so the neck connects
        # Distance from edge to circle center:
        circle_center_dist = r * 0.8 # Slight overlap to ensure robust geometry
        
        # We construct a 2D profile to extrude
        # This is a bit complex, simpler to just use boolean cylinders and boxes
        return None 

    # Instead of complex 2D sketches, let's use boolean operations on the solid.
    # We define the "male" tab shape as a separate solid object positioned correctly.
    
    # Tab geometry parameters
    neck_length = t_rad * 1.5 # How far the tab sticks out
    
    # We need to determine for each of the 4 edges (Top, Right, Bottom, Left)
    # whether it has a Male (+1), Female (-1), or Flat (0) connector.
    # This pattern mimics standard jigsaw puzzle logic or the specific image pattern.
    
    # Analyzing the image:
    # It looks like a 2x3 grid.
    # Row 0 (Bottom): 
    #   Col 0: Top=Male, Right=Male
    #   Col 1: Top=Male, Left=Female (matches Col 0 Right)
    # Row 1 (Middle):
    #   Col 0: Top=Male, Bottom=Female (matches Row 0 Top), Right=Male
    #   Col 1: Top=Male, Bottom=Female (matches Row 0 Top), Left=Female
    # Row 2 (Top):
    #   Col 0: Bottom=Female, Right=Male
    #   Col 1: Bottom=Female, Left=Female
    
    # Let's formalize the connectivity matrix for the image pattern:
    # 0 = Flat, 1 = Male (Out), -1 = Female (In)
    # Order: [Top, Right, Bottom, Left]
    
    conns = [0, 0, 0, 0]
    
    # Logic based on the visual pattern in the image
    # Note: The image shows the center vertical line having tabs pointing to the RIGHT.
    # The horizontal lines seem to have tabs pointing UP.
    
    # Top Edge Logic
    if i < rows - 1:
        conns[0] = 1 # Male pointing Up
    else:
        conns[0] = 0 # Flat top edge
        
    # Right Edge Logic
    if j < cols - 1:
        conns[1] = 1 # Male pointing Right
    else:
        conns[1] = 0 # Flat right edge
        
    # Bottom Edge Logic
    if i > 0:
        conns[2] = -1 # Female (accepting the Male from below)
    else:
        conns[2] = 0 # Flat bottom edge
        
    # Left Edge Logic
    if j > 0:
        conns[3] = -1 # Female (accepting the Male from left)
    else:
        conns[3] = 0 # Flat left edge

    # Perform Boolean Operations
    
    # 1. TOP EDGE (y = +height/2)
    if conns[0] != 0:
        # Create the tab shape
        # Neck
        neck = (cq.Workplane("XY")
                .center(0, height/2)
                .box(n_w, neck_length * 2, thick))
        # Head
        head = (cq.Workplane("XY")
                .center(0, height/2 + t_rad*0.5)
                .cylinder(thick, t_rad))
        
        tab_shape = neck.union(head)
        
        if conns[0] == 1:
            piece = piece.union(tab_shape)
        else:
            piece = piece.cut(tab_shape)

    # 2. RIGHT EDGE (x = +width/2)
    if conns[1] != 0:
        neck = (cq.Workplane("XY")
                .center(width/2, 0)
                .box(neck_length * 2, n_w, thick))
        head = (cq.Workplane("XY")
                .center(width/2 + t_rad*0.5, 0)
                .cylinder(thick, t_rad))
        
        tab_shape = neck.union(head)
        
        if conns[1] == 1:
            piece = piece.union(tab_shape)
        else:
            piece = piece.cut(tab_shape)

    # 3. BOTTOM EDGE (y = -height/2)
    if conns[2] != 0:
        neck = (cq.Workplane("XY")
                .center(0, -height/2)
                .box(n_w, neck_length * 2, thick))
        # Note: Center placement is slightly different depending on union or cut to ensure tight fit?
        # Ideally, we use the exact same geometry to ensure fit.
        # The logic: if Bottom is Female, it corresponds to the Top Male of the piece below.
        # The Top Male was at +height/2 + offset. 
        # So relative to this piece's center, the cutout shape is at -height/2 + offset (which is effectively inside)
        
        # Actually, simpler logic: The "Tab" geometry is defined centered on the edge line.
        # If Male, we add it. If Female, we subtract it.
        # Since the tab head center is 'outside' the box boundary, subtracting it creates the socket.
        
        head = (cq.Workplane("XY")
                .center(0, -height/2 - t_rad*0.5)
                .cylinder(thick, t_rad))
        
        tab_shape = neck.union(head)
        
        if conns[2] == 1:
            piece = piece.union(tab_shape)
        else:
            piece = piece.cut(tab_shape)

    # 4. LEFT EDGE (x = -width/2)
    if conns[3] != 0:
        neck = (cq.Workplane("XY")
                .center(-width/2, 0)
                .box(neck_length * 2, n_w, thick))
        head = (cq.Workplane("XY")
                .center(-width/2 - t_rad*0.5, 0)
                .cylinder(thick, t_rad))
        
        tab_shape = neck.union(head)
        
        if conns[3] == 1:
            piece = piece.union(tab_shape)
        else:
            piece = piece.cut(tab_shape)

    # Position the piece in the global assembly
    # x position: j * width
    # y position: i * height
    # We need to shift because piece center is (0,0)
    x_pos = j * width + width/2
    y_pos = i * height + height/2
    
    piece = piece.translate((x_pos, y_pos, 0))
    
    return piece

# Build the assembly
assembly_parts = []

for r in range(rows):
    for c in range(cols):
        part = create_puzzle_piece(r, c, block_w, block_h, thickness, tab_radius, neck_width)
        assembly_parts.append(part)

# Combine all parts into one compound object for the 'result'
if assembly_parts:
    result = assembly_parts[0]
    for p in assembly_parts[1:]:
        result = result.union(p)

# Center the final result
result = result.translate((-wall_width/2, -wall_height/2, 0))