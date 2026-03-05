import cadquery as cq
import math

# --- Parameters ---
crate_length = 330.0  # approximate standard milk crate size (mm)
crate_width = 330.0
crate_height = 280.0
wall_thickness = 3.0
fillet_radius = 5.0
handle_width = 100.0
handle_height = 30.0
handle_pos_z = 240.0  # Center height of handle
grid_thickness = 2.0  # Thickness of the diamond pattern grid
pattern_angle = 45.0  # Angle for diamond pattern

# --- Helper Functions ---

def create_face_pattern(length, height, angle=45, spacing=35, bar_width=5):
    """
    Creates a diamond lattice pattern sketch.
    """
    # Create a base rectangle
    base = cq.Workplane("XY").rect(length, height)
    
    # Create the cutting shapes (diamonds)
    # We simulate this by creating a grid of diagonal bars
    
    # Calculate diagonal length to cover the rect
    diag_len = math.sqrt(length**2 + height**2) * 1.5
    num_lines = int(diag_len / spacing)
    
    # Create a temporary solid block to cut slots into
    block = cq.Workplane("XY").box(length, height, wall_thickness)
    
    # Create cutters for one direction
    cutters1 = cq.Workplane("XY")
    for i in range(-num_lines, num_lines):
        offset = i * spacing
        cutters1 = cutters1.center(0,0).rect(diag_len, bar_width).rotate((0,0,1), (0,0,0), angle).translate((offset, 0, 0))
    
    # Create cutters for the other direction
    cutters2 = cq.Workplane("XY")
    for i in range(-num_lines, num_lines):
        offset = i * spacing
        cutters2 = cutters2.center(0,0).rect(diag_len, bar_width).rotate((0,0,1), (0,0,0), -angle).translate((offset, 0, 0))

    # Extrude cutters
    c1 = cutters1.extrude(wall_thickness * 2)
    c2 = cutters2.extrude(wall_thickness * 2)
    
    # This approach is computationally heavy with booleans. 
    # A cleaner approach for CadQuery is to construct the negative space (the holes)
    # The holes are diamonds.
    
    return c1.union(c2)

def make_side_wall(length, height):
    """
    Constructs a single side wall with structural ribs, handle, and lattice.
    """
    # 1. Base Wall
    wall = cq.Workplane("XY").box(length, height, wall_thickness)
    
    # 2. Add Border Frame (Rim)
    rim_thickness = 8.0
    rim_depth = 8.0 # Stick out depth
    
    frame = (cq.Workplane("XY")
             .rect(length, height)
             .rect(length - rim_thickness*2, height - rim_thickness*2)
             .extrude(rim_depth)
            )
    
    # 3. Add Vertical Structural Ribs (Corner pillars and center reinforcements)
    rib_width = 15.0
    rib_depth = 6.0
    
    # Corner pillars (simplified as vertical ribs at ends)
    pillar_l = (cq.Workplane("XY")
                .center(-length/2 + rib_width/2, 0)
                .rect(rib_width, height)
                .extrude(rib_depth))
    
    pillar_r = (cq.Workplane("XY")
                .center(length/2 - rib_width/2, 0)
                .rect(rib_width, height)
                .extrude(rib_depth))
                
    # Center Label Plate Area (Solid band at bottom)
    plate_height = 60.0
    plate_y_offset = -height/2 + plate_height/2 + rim_thickness
    plate = (cq.Workplane("XY")
             .center(0, plate_y_offset)
             .rect(length - rim_thickness*2, plate_height)
             .extrude(wall_thickness + 1)) # Slightly thicker than base wall
             
    # 4. Create Lattice Pattern
    # Instead of complex boolean subtraction of thousands of diamonds, 
    # we'll build the lattice additively for performance and robustness in this script.
    
    # Lattice params
    lattice_bar_w = 4.0
    lattice_spacing = 30.0 
    
    # Define area for lattice (exclude label plate and top handle area)
    lattice_area_h = height - plate_height - 60 # Reserve top for handle
    lattice_center_y = (height/2) - (lattice_area_h/2) - 40
    
    # Create diagonal bars
    lattice_sketch = cq.Sketch().rect(length, height) # Clipping boundary
    
    diag_count = 25
    for i in range(-diag_count, diag_count):
        off = i * lattice_spacing
        # Diagonal /
        lattice_sketch = lattice_sketch.push([(off, 0)]).rect(lattice_bar_w, height*2, angle=45, mode='a')
        # Diagonal \
        lattice_sketch = lattice_sketch.push([(off, 0)]).rect(lattice_bar_w, height*2, angle=-45, mode='a')
        
    lattice = (cq.Workplane("XY")
               .placeSketch(lattice_sketch)
               .extrude(wall_thickness)
               )
    
    # Cut lattice to fit inside the frame
    mask = (cq.Workplane("XY")
            .rect(length - rim_thickness*2, height - rim_thickness*2)
            .extrude(wall_thickness*2)
            )
    lattice = lattice.intersect(mask)
    
    # Remove lattice from label plate area
    plate_void = (cq.Workplane("XY")
                  .center(0, plate_y_offset)
                  .rect(length, plate_height)
                  .extrude(wall_thickness*2))
    lattice = lattice.cut(plate_void)
    
    # Remove lattice from handle area
    handle_zone_h = 50.0
    handle_zone_y = height/2 - handle_zone_h/2 - rim_thickness
    handle_void = (cq.Workplane("XY")
                   .center(0, handle_zone_y)
                   .rect(length, handle_zone_h)
                   .extrude(wall_thickness*2))
    lattice = lattice.cut(handle_void)

    # 5. Handle Cutout and Reinforcement
    handle_y_rel = (handle_pos_z - (crate_height/2)) # Adjust relative to center
    # Recalculate based on wall geometry
    handle_y_rel = height/2 - 40 # Approx from top
    
    handle_cutout = (cq.Workplane("XY")
                     .center(0, handle_y_rel)
                     .rect(handle_width, handle_height)
                     .extrude(wall_thickness * 5))
                     
    handle_rim = (cq.Workplane("XY")
                  .center(0, handle_y_rel)
                  .rect(handle_width + 10, handle_height + 10)
                  .rect(handle_width, handle_height)
                  .extrude(rib_depth))

    # Combine parts
    full_wall = wall.union(frame).union(pillar_l).union(pillar_r).union(plate).union(lattice).union(handle_rim)
    full_wall = full_wall.cut(handle_cutout)
    
    return full_wall

def make_bottom(length, width):
    """
    Creates the bottom grid.
    """
    base = cq.Workplane("XY").box(length, width, wall_thickness)
    
    # Rim
    rim = (cq.Workplane("XY")
           .rect(length, width)
           .rect(length - 15, width - 15)
           .extrude(5))
    
    # Simple Grid pattern for bottom
    grid_w = 4.0
    grid = cq.Workplane("XY")
    
    # X bars
    for i in range(1, 6):
        grid = grid.rect(length, grid_w).translate((0, (i*width/7) - width/2, 0))
        grid = grid.rect(length, grid_w).translate((0, -(i*width/7) + width/2, 0))
    
    # Y bars
    for i in range(1, 6):
        grid = grid.rect(grid_w, width).translate(((i*length/7) - length/2, 0, 0))
        grid = grid.rect(grid_w, width).translate((-(i*length/7) + length/2, 0, 0))
        
    grid_solid = grid.extrude(wall_thickness)
    
    return base.union(rim).union(grid_solid)

# --- Assembly ---

# 1. Create one side wall instance
side_wall_geo = make_side_wall(crate_length, crate_height)

# 2. Create the four sides by rotating and translating
front = side_wall_geo.rotate((0,0,0), (1,0,0), 90).translate((0, -crate_width/2 + wall_thickness/2, crate_height/2))
back = side_wall_geo.rotate((0,0,0), (1,0,0), 90).rotate((0,0,1),(0,0,0), 180).translate((0, crate_width/2 - wall_thickness/2, crate_height/2))
left = side_wall_geo.rotate((0,0,0), (1,0,0), 90).rotate((0,0,1),(0,0,0), 90).translate((-crate_length/2 + wall_thickness/2, 0, crate_height/2))
right = side_wall_geo.rotate((0,0,0), (1,0,0), 90).rotate((0,0,1),(0,0,0), -90).translate((crate_length/2 - wall_thickness/2, 0, crate_height/2))

# 3. Create Bottom
bottom = make_bottom(crate_length - wall_thickness*2, crate_width - wall_thickness*2)
bottom = bottom.translate((0, 0, wall_thickness/2))

# 4. Corner Reinforcements (Fillets/Chamfers simulation)
# Real milk crates have complex corner geometry. We add corner posts to merge the gaps.
corner_post_sz = 12.0
corner_post = cq.Workplane("XY").rect(corner_post_sz, corner_post_sz).extrude(crate_height)

c1 = corner_post.translate((-crate_length/2 + corner_post_sz/2, -crate_width/2 + corner_post_sz/2, crate_height/2))
c2 = corner_post.translate((crate_length/2 - corner_post_sz/2, -crate_width/2 + corner_post_sz/2, crate_height/2))
c3 = corner_post.translate((-crate_length/2 + corner_post_sz/2, crate_width/2 - corner_post_sz/2, crate_height/2))
c4 = corner_post.translate((crate_length/2 - corner_post_sz/2, crate_width/2 - corner_post_sz/2, crate_height/2))

# 5. Union all
result = front.union(back).union(left).union(right).union(bottom)
result = result.union(c1).union(c2).union(c3).union(c4)

# Apply global fillet to accessible edges for molded look (optional, computationally expensive)
# result = result.edges("|Z").fillet(2.0) 

# Final Cleanup to ensure variable name matches requirement
result = result