import cadquery as cq

# --- Parameter Definitions ---
# Overall Window Dimensions
width = 120.0       # Total width of the window
height = 100.0      # Total height of the window
frame_depth = 10.0  # Thickness of the wall/frame (Z-direction)

# Frame and Sash Dimensions
frame_width = 8.0   # Width of the outer frame border
sash_width = 5.0    # Width of the inner sash frames
muntin_width = 2.0  # Width of the horizontal divider bars (muntins)
glass_thickness = 2.0 # Thickness of the "glass" panes

# --- Derived Parameters ---
# Calculated internal dimensions
inner_opening_width = width - (2 * frame_width)
inner_opening_height = height - (2 * frame_width)

# Calculate dimensions for the two sashes (assuming equal split)
# There is usually a central vertical divider or overlap. 
# Let's model a central vertical mullion as part of the main frame for simplicity, 
# or two sashes side-by-side. The image looks like two distinct sashes side-by-side separated by a mullion.
mullion_width = 4.0 # Vertical bar separating the two sashes
sash_opening_width = (inner_opening_width - mullion_width) / 2

# --- Modeling ---

# 1. Create the Main Outer Frame
# Start with the full block
outer_box = cq.Workplane("XY").box(width, height, frame_depth)

# Create the two main openings (left and right) to form the frame and central mullion
# We cut through the full depth
left_opening_center_x = -(width/2) + frame_width + (sash_opening_width/2)
right_opening_center_x = (width/2) - frame_width - (sash_opening_width/2)

frame = (
    outer_box
    .faces(">Z")
    .workplane()
    .pushPoints([(left_opening_center_x, 0), (right_opening_center_x, 0)])
    .rect(sash_opening_width, inner_opening_height)
    .cutBlind(-frame_depth)
)

# 2. Create the Sashes
# We will create one sash and then place two instances of it.
# The sash sits slightly recessed inside the frame.
sash_recess = 1.0 # How far back the sash sits from the front face
sash_depth = frame_depth - (2 * sash_recess)

def create_sash(w, h, d, border, muntin_h, glass_thk):
    # Outer block of the sash
    sash_block = cq.Workplane("XY").box(w, h, d)
    
    # Internal cutout dimensions
    pane_w = w - (2 * border)
    pane_h_total = h - (2 * border)
    pane_h_single = (pane_h_total - muntin_h) / 2
    
    # Create the cutouts for the glass (upper and lower panes)
    # Positions relative to sash center
    top_pane_center_y = (h/2) - border - (pane_h_single/2)
    bottom_pane_center_y = -(h/2) + border + (pane_h_single/2)
    
    sash_frame = (
        sash_block
        .faces(">Z")
        .workplane()
        .pushPoints([(0, top_pane_center_y), (0, bottom_pane_center_y)])
        .rect(pane_w, pane_h_single)
        .cutBlind(-d) # Cut all the way through initially
    )
    
    # Add the "glass" back in the center
    # This is a thin plate in the middle of the sash depth
    glass = (
        cq.Workplane("XY")
        .workplane(offset = -d/2) # Start at bottom of sash
        .center(0,0)
        .rect(w - 2*border, h - 2*border) # Simplified single sheet of glass inside
        .extrude(glass_thk)
        .translate((0,0, (d - glass_thk)/2)) # Center Z
    )
    
    return sash_frame.union(glass)

# Generate the sash geometry
sash_geo = create_sash(
    sash_opening_width, 
    inner_opening_height, 
    sash_depth, 
    sash_width, 
    muntin_width, 
    glass_thickness
)

# 3. Assemble the Window
# Place the left sash
left_sash = sash_geo.translate((left_opening_center_x, 0, 0))

# Place the right sash
right_sash = sash_geo.translate((right_opening_center_x, 0, 0))

# Combine everything
result = frame.union(left_sash).union(right_sash)

# If running in CQ-Editor or generic export context
if 'show_object' in globals():
    show_object(result)