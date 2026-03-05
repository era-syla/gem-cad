import cadquery as cq

# --- Parameters ---
# Main Plate
plate_width = 160.0
plate_height = 100.0
plate_thickness = 2.0  # Thickness of the base sheet
wall_height = 8.0     # Height of the rim from the base bottom
wall_thickness = 3.0

# Mounting Holes (Corners)
corner_hole_diam = 2.5
corner_hole_inset = 4.0

# Top Edge Cutout Features
# Complex cutout profile approximate dimensions
cutout_center_r = 6.0
cutout_notch_width = 10.0
cutout_usb_width = 12.0
cutout_usb_depth = 4.0

# Internal Ribs/Guides
rib_width = 4.0
rib_height = 4.0 # Height from internal floor
left_rib_x = -35.0
right_rib_x = 35.0
rib_length_top = 40.0 # Upper vertical rails

# Bottom Vent Slots
vent_slot_width = 3.0
vent_slot_spacing = 6.0
vent_slot_height = 10.0 # How far up they go
vent_count = 6

# Bottom Clips/Stand-offs
clip_width = 8.0
clip_depth = 8.0
clip_height = 6.0
clip_y_pos = -plate_height/2 + wall_thickness + clip_depth/2 + 2

# --- Construction ---

# 1. Base Box (Shell)
# Create the outer block
base = cq.Workplane("XY").box(plate_width, plate_height, wall_height)

# Hollow it out to create the rim and floor
# We select the top face and shell inwards.
# Since we want a specific floor thickness, we shell by -wall_thickness
# but this makes the floor wall_thickness. Let's do a pocket instead for more control.
outer_box = cq.Workplane("XY").box(plate_width, plate_height, wall_height)
inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness) # Start cut above floor
    .box(plate_width - 2*wall_thickness, plate_height - 2*wall_thickness, wall_height)
)
result = outer_box.cut(inner_cut)


# 2. Corner Holes
# Select the rim face
result = (
    result.faces(">Z")
    .workplane()
    .rect(plate_width - 2*corner_hole_inset, plate_height - 2*corner_hole_inset, forConstruction=True)
    .vertices()
    .hole(corner_hole_diam)
)

# 3. Top Edge Complex Cutout
# We'll draw a profile on the XZ plane (side view) or XY plane to cut through the top rim.
# Looking at the image, there is a circular notch, some stepped notches, and a rectangular port.
# Let's cut from the Top ("Z") down.

top_wall_y = plate_height/2 - wall_thickness/2
cutout_sketch = (
    cq.Workplane("XY")
    .workplane(offset=wall_height/2) # On top of the box
    .moveTo(0, plate_height/2) 
    
    # Circular cutout
    .moveTo(-8, plate_height/2)
    .threePointArc((0, plate_height/2 - 5), (8, plate_height/2))
    .lineTo(8, plate_height/2 + 5) # Close loop outside
    .lineTo(-8, plate_height/2 + 5)
    .close()
    
    # Rectangular Notch (right side of center)
    .moveTo(15, plate_height/2)
    .rect(cutout_usb_width, wall_thickness * 3, centered=True)
    
    # Smaller Notch (left side)
    .moveTo(-15, plate_height/2)
    .rect(5, wall_thickness * 3, centered=True)
)

# Apply Cutouts
result = result.cut(cutout_sketch.extrude(-wall_height)) # Cut all the way through


# 4. Vertical Guide Ribs (Top Half)
# These are rails attached to the back floor and the top wall
def create_rib(x_pos):
    rib = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness)
        .moveTo(x_pos, plate_height/2 - wall_thickness - rib_length_top/2)
        .box(rib_width, rib_length_top, rib_height)
    )
    return rib

result = result.union(create_rib(left_rib_x))
result = result.union(create_rib(right_rib_x))

# 5. Small Horizontal Tabs on the Ribs
# Small tabs protruding inwards from the ends of the ribs
tab_size = 3.0
tab_left = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .moveTo(left_rib_x + rib_width/2 + tab_size/2, plate_height/2 - wall_thickness - rib_length_top)
    .box(tab_size, rib_width, rib_height) 
)
tab_right = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .moveTo(right_rib_x - rib_width/2 - tab_size/2, plate_height/2 - wall_thickness - rib_length_top)
    .box(tab_size, rib_width, rib_height)
)
result = result.union(tab_left).union(tab_right)


# 6. Bottom Clips/Mounts
# These look like square blocks with intricate internal cuts or snaps.
# Simplified representation: Blocks with a central slot.
def create_bottom_clip(x_pos):
    clip_base = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness)
        .moveTo(x_pos, -plate_height/2 + wall_thickness + clip_depth/2)
        .box(clip_width, clip_depth, clip_height)
    )
    # Add a slot/hole feature
    slot = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness)
        .moveTo(x_pos, -plate_height/2 + wall_thickness + clip_depth/2)
        .rect(clip_width/3, clip_depth/2)
        .extrude(clip_height)
    )
    # Add a cross pin/hole
    pin_hole = (
        cq.Workplane("YZ")
        .workplane(offset=x_pos + clip_width/2)
        .moveTo(-plate_height/2 + wall_thickness + clip_depth/2, plate_thickness + clip_height/2)
        .circle(1.0)
        .extrude(-clip_width)
    )
    
    return clip_base.cut(slot).cut(pin_hole)

result = result.union(create_bottom_clip(left_rib_x))
result = result.union(create_bottom_clip(right_rib_x))

# 7. Bottom Vent Slots
# A series of rectangular cuts through the bottom rim/floor area.
# Based on image, they cut into the floor near the bottom wall.
vent_start_x = -15.0
for i in range(vent_count):
    x_pos = vent_start_x + (i * vent_slot_spacing)
    # Create the cut shape
    vent = (
        cq.Workplane("XY")
        .moveTo(x_pos, -plate_height/2 + wall_thickness/2 + 2) 
        .rect(vent_slot_width, 8) # Rectangular slot on floor
        .extrude(wall_height) # Cut through floor and potentially wall
    )
    # Also need to cut the vertical wall slightly for the "comb" look
    vent_wall = (
        cq.Workplane("XZ")
        .moveTo(x_pos, wall_height/2)
        .rect(vent_slot_width, wall_height)
        .extrude(plate_height) # Extrude along Y to hit the bottom wall
    )
    # Limit the wall cut to just the bottom area
    vent_wall_cut_mask = (
        cq.Workplane("XY")
        .moveTo(0, -plate_height/2)
        .rect(plate_width, 15)
        .extrude(wall_height)
    )
    
    effective_wall_cut = vent_wall.intersect(vent_wall_cut_mask)
    
    result = result.cut(vent).cut(effective_wall_cut)

# Refinement: Add the specific large semicircular cutout on the top edge more precisely 
# to match the specific "half-circle" dip in the rim visible in the image.
semicircle_cut = (
    cq.Workplane("XZ")
    .workplane(offset=plate_height/2) # Back face (top in Y)
    .moveTo(-10, wall_height)
    .threePointArc((-5, wall_height - 4), (0, wall_height))
    .lineTo(0, wall_height+5)
    .lineTo(-10, wall_height+5)
    .close()
    .extrude(-wall_thickness*2)
)
result = result.cut(semicircle_cut)

# Final Rotation to match image orientation roughly (Optional, but good for preview)
# The image shows the inside face.
# result = result.rotate((0,0,0), (1,0,0), -45) 

# Ensure result is exported/visible
# show_object(result)