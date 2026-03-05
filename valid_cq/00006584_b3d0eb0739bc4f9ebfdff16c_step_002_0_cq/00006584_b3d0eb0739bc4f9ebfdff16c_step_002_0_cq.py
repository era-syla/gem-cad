import cadquery as cq

# Parametric dimensions
plate_width = 100.0
plate_height = 40.0
plate_thickness = 5.0

# Cutout dimensions (rectangular windows)
cutout_width = 15.0
cutout_height = 25.0
cutout_offset_x = 30.0  # Distance from center to center of cutout

# Corner hooks/tabs
hook_depth = 5.0
hook_width = 5.0
hook_thickness = 5.0
hook_gap = 5.0 # Space inside the hook

# Central block on the back
center_block_width = 30.0
center_block_height = 15.0
center_block_depth = 15.0

# Pins on the central block
pin_diameter = 4.0
pin_height = 10.0
pin_spacing = 15.0

# Create the main front plate
main_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
)

# Create the cutouts
cutout_left = (
    cq.Workplane("XY")
    .rect(cutout_width, cutout_height)
    .extrude(plate_thickness * 2) # Ensure full cut
    .translate((-cutout_offset_x, 0, 0))
)

cutout_right = (
    cq.Workplane("XY")
    .rect(cutout_width, cutout_height)
    .extrude(plate_thickness * 2)
    .translate((cutout_offset_x, 0, 0))
)

# Create corner hooks (L-shaped tabs on the back corners)
# We need 4 hooks at the corners.
# Let's define one hook shape relative to a corner and then mirror/place them.
def create_hook(x_pos, y_pos):
    # Base leg sticking out back
    leg1 = (
        cq.Workplane("XY")
        .workplane(offset=-plate_thickness/2)
        .center(x_pos, y_pos)
        .box(hook_width, hook_thickness, hook_depth*2, centered=(True, True, False))
        .translate((0, 0, -hook_depth*2))
    )
    
    # The return leg of the hook (forming the 'L')
    # Determine direction based on position
    x_dir = 1 if x_pos > 0 else -1
    
    # We want the hook to point inwards horizontally
    leg2 = (
        cq.Workplane("XY")
        .workplane(offset=-plate_thickness/2 - hook_depth*2)
        .center(x_pos - (x_dir * hook_width/2) + (x_dir * hook_width/2), y_pos) # Adjust center
        .center(-x_dir * hook_width, 0) # Shift inward
        .box(hook_width, hook_thickness, hook_width, centered=(True, True, False)) # Using hook_width as depth for leg2
    )
    # Actually, looking at the image, the hooks are simple "C" or "L" shapes at the very edges.
    # Top Right/Left and Bottom Right/Left.
    # The hooks seem to extend backwards and then turn inwards vertically (towards the center Y line) or horizontally?
    # Looking closely at the top right corner: The protrusion goes back, then turns DOWN.
    # Bottom right corner: Goes back, turns UP.
    
    y_dir = 1 if y_pos > 0 else -1
    
    # Extrude back
    back_piece = (
        cq.Workplane("XY")
        .workplane(offset=-plate_thickness/2)
        .center(x_pos, y_pos)
        .rect(hook_width, hook_thickness)
        .extrude(-hook_depth)
    )
    
    # Extrude the tip (creating the catch)
    tip_piece = (
        back_piece.faces("<Z")
        .workplane()
        .center(0, -y_dir * hook_thickness/2) # Move to edge towards center
        .rect(hook_width, hook_thickness)     # Define tip cross section
        .extrude(hook_thickness)              # Extrude towards center Y
    )
    return back_piece.union(tip_piece)

# Coordinates for corners (centers of the hook bases)
x_c = plate_width/2 - hook_width/2
y_c = plate_height/2 - hook_thickness/2

hooks = (
    create_hook(x_c, y_c)
    .union(create_hook(-x_c, y_c))
    .union(create_hook(x_c, -y_c))
    .union(create_hook(-x_c, -y_c))
)

# Central Block on the back
center_block = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2)
    .box(center_block_width, center_block_height, center_block_depth, centered=(True, True, False))
    .translate((0, 0, -center_block_depth))
)

# Pins on the central block
pin1 = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2 - center_block_depth)
    .center(-pin_spacing/2, 0)
    .circle(pin_diameter/2)
    .extrude(-pin_height)
)

pin2 = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2 - center_block_depth)
    .center(pin_spacing/2, 0)
    .circle(pin_diameter/2)
    .extrude(-pin_height)
)

# Combine everything
result = (
    main_plate
    .cut(cutout_left)
    .cut(cutout_right)
    .union(hooks)
    .union(center_block)
    .union(pin1)
    .union(pin2)
)