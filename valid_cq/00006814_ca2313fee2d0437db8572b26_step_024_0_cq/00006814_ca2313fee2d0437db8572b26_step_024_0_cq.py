import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of one box
width = 60.0    # Width of the frame
height = 100.0  # Height of the frame
depth = 10.0    # Total depth (thickness) of the frame
wall_thickness = 2.0  # Thickness of the outer walls and back
shelf_thickness = 2.0 # Thickness of the internal shelves/dividers

# --- Helper Function for Tray/Box ---
def make_tray(w, h, d, t_wall, t_shelf, num_shelves=0):
    """
    Creates a rectangular tray/box with optional shelves.
    w: width
    h: height
    d: depth
    t_wall: wall thickness
    t_shelf: shelf thickness
    num_shelves: number of evenly spaced internal horizontal shelves
    """
    # 1. Create the base solid block
    base = cq.Workplane("XY").box(w, h, d)
    
    # 2. Shell it to create the open box. 
    # We select the "front" face (positive Z in default orientation) to be removed.
    # Note: cadquery's box creates it centered.
    # Let's verify orientation. box(w, h, d) makes a box from -w/2 to w/2, etc.
    # We want to remove the face at +d/2.
    shelled = base.faces(">Z").shell(-t_wall)
    
    # 3. Add shelves if requested
    if num_shelves > 0:
        # Calculate spacing
        # Internal height is h - 2*t_wall
        # We need to place 'num_shelves' dividers.
        # This creates (num_shelves + 1) compartments.
        # The shelf positions need to be calculated relative to the center.
        
        internal_height = h - 2 * t_wall
        compartment_height = (internal_height - (num_shelves * t_shelf)) / (num_shelves + 1)
        
        # Start at the bottom internal face and move up
        # Bottom internal y = -h/2 + t_wall
        current_y = -h/2 + t_wall
        
        shelves = []
        for i in range(num_shelves):
            # Calculate center Y position for the shelf
            # Move up by one compartment height
            current_y += compartment_height
            # The shelf center is at current_y + t_shelf/2
            shelf_center_y = current_y + t_shelf/2
            
            # Create the shelf geometry
            # Shelf width is internal width: w - 2*t_wall
            # Shelf depth is internal depth: d - t_wall (since back is t_wall thick)
            # We construct it relative to the global origin
            
            shelf = (
                cq.Workplane("XY")
                .workplane(offset= -d/2 + t_wall + (d - t_wall)/2 ) # Center Z of the shelf volume
                .center(0, shelf_center_y) # Center Y of the shelf
                .box(w - 2*t_wall, t_shelf, d - t_wall)
            )
            shelves.append(shelf)
            
            # Increment current_y by the shelf thickness for the next iteration
            current_y += t_shelf
            
        # Unite shelves with the main body
        for s in shelves:
            shelled = shelled.union(s)
            
    return shelled

# --- Build Part 1 (Left - with 2 dividers) ---
part1 = make_tray(width, height, depth, wall_thickness, shelf_thickness, num_shelves=2)

# --- Build Part 2 (Right - empty) ---
# Looking at the image, the right part looks like a simple tray, possibly a lid or just an empty version.
# However, there is a small feature at the top. It looks like a single shelf very close to the top edge.
# Let's model it as a tray with one specific shelf or just a tray.
# Upon closer inspection of the right object, it has a horizontal bar near the top.
# This could be modeled as a tray with 1 shelf, but the shelf is offset differently, not centered.

# Let's make a custom construction for Part 2 to match the "top bar" look.
part2_base = make_tray(width, height, depth, wall_thickness, shelf_thickness, num_shelves=0)

# Add the specific top bar/divider for the right part
# It looks positioned maybe 10-15% down from the top.
top_gap = 10.0 # Distance from inside top wall to the bar
bar_y_pos = (height/2 - wall_thickness) - top_gap - (shelf_thickness/2)

part2_bar = (
    cq.Workplane("XY")
    .workplane(offset= -depth/2 + wall_thickness + (depth - wall_thickness)/2 )
    .center(0, bar_y_pos)
    .box(width - 2*wall_thickness, shelf_thickness, depth - wall_thickness)
)
part2 = part2_base.union(part2_bar)

# --- Assembly ---
# Move part 2 to the right so they are side-by-side like the image
part2 = part2.translate((width * 1.2, 0, 0))

# Combine into a single result object
result = part1.union(part2)