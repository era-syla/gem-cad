import cadquery as cq

# --- Parameter Definitions ---
# Main large central box
main_box_length = 60.0
main_box_width = 40.0
main_box_height = 10.0
main_handle_radius = 15.0
main_handle_thickness = 2.0

# Medium box (right side)
med_box_length = 60.0
med_box_width = 15.0
med_box_height = 8.0
med_handle_radius = 10.0
med_handle_thickness = 1.5

# Small box (left side)
small_box_length = 30.0
small_box_width = 10.0
small_box_height = 8.0
small_handle_radius = 6.0
small_handle_thickness = 1.0

# Spacing between objects
spacing = 20.0

def create_handled_box(length, width, height, handle_r, handle_th):
    """
    Creates a rectangular box with a semi-circular handle protrusion on one side.
    """
    # Create the base box centered at origin
    box = cq.Workplane("XY").box(length, width, height)
    
    # Create the handle geometry
    # We'll make a disk, cut a hole in it to make a ring, then cut it in half
    # and attach it to the side.
    
    # Calculate position: attached to the 'front' face (along Y axis)
    # The handle is a semi-circle loop
    
    # Helper to create a torus/ring segment
    # We do this by sweeping a circle or creating a pipe
    path = (
        cq.Workplane("XZ")
        .workplane(offset=width/2.0) # Move to the front face
        .moveTo(-handle_r, 0)
        .threePointArc((0, handle_r/2.0), (handle_r, 0)) # Create an arc
    )
    
    # Create the cross section of the handle
    handle = (
        cq.Workplane("YZ")
        .workplane(offset=-handle_r) # Start at the beginning of the path
        .center(width/2.0, 0)        # Align with the face
        .circle(handle_th/2.0)       # Cross section circle
        .sweep(path)
    )
    
    # Alternatively, a simpler way is just a flat extrusion if the image implies flat handles
    # Looking closely at the image, the handles look like thin loops or semi-circles sticking out.
    # Let's try a simpler approach: A solid semi-cylinder subtracted by a smaller semi-cylinder
    
    handle_outer_r = handle_r
    handle_inner_r = handle_r - handle_th
    
    handle_solid = (
        cq.Workplane("XY")
        .workplane(offset=-height/2.0) # Start at bottom
        .center(0, width/2.0)          # Center on the edge
        .extrude(height)              # Make a construction plane
        .workplane()
        .moveTo(0, 0)
        # Draw outer arc
        .lineTo(handle_outer_r, 0)
        .threePointArc((0, handle_outer_r), (-handle_outer_r, 0))
        .close()
        .extrude(height) # Extrude along Z (which is now perpendicular to XY plane due to workplane shifts?)
        # Actually let's stick to world coordinates to avoid confusion
    )
    
    # Let's rebuild the handle simpler: on the side face
    # We will create a sketch on the XZ plane, projected to the Y-face
    
    handle_sketch = (
        cq.Workplane("XZ")
        .workplane(offset=width/2.0)
        .moveTo(handle_r, 0)
        .threePointArc((0, -handle_r*0.6), (-handle_r, 0)) # Arc curving downwards or upwards? Image shows side attachment.
        # Let's assume the handle is a loop sticking out of the Y face.
    )
    
    # Revised Handle Strategy: A simple torus segment
    handle = (
        cq.Workplane("XY")
        .moveTo(0, width/2.0)
        .circle(handle_r)
        .extrude(height/2.0) # Placeholder thickness
    )
    
    # Let's stick to the visual: It's a box with a loop handle on the long side.
    # We create the box.
    part = cq.Workplane("XY").box(length, width, height)
    
    # We create a torus for the handle
    # Torus major radius = handle_r
    # Torus minor radius (thickness) = handle_th
    
    # Position the torus
    # It needs to be attached to the side face (Y+)
    # Center of torus at (0, width/2, 0)
    # Rotation needed to make it stick out flat or perpendicular?
    # In the image, the handle looks like a semi-circle flat on the ground plane or slightly raised? 
    # Actually, they look like "D" rings or simple curved handles attached to the side.
    
    # Create a path for the handle
    path = (
        cq.Workplane("XY")
        .moveTo(-handle_r, width/2)
        .threePointArc((0, width/2 + handle_r * 0.5), (handle_r, width/2))
    )
    
    # Sweep a circle along that path
    handle = (
        cq.Workplane("YZ")
        .workplane(offset=-handle_r)
        .moveTo(width/2, 0)
        .circle(handle_th)
        .sweep(path)
    )
    
    return part.union(handle)

# --- Construct the Assemblies ---

# 1. Central Large Box
# This box has some extra detail on top: a rectangular depression or marking.
main_body = cq.Workplane("XY").box(main_box_length, main_box_width, main_box_height)

# Add the detail on top (rectangular cut/groove)
detail_sketch = (
    cq.Workplane("XY")
    .workplane(offset=main_box_height/2.0)
    .rect(main_box_length * 0.6, main_box_width * 0.6)
    .rect(main_box_length * 0.6 - 2, main_box_width * 0.6 - 2) # Inner rect for a groove
)
# We'll just make a simple cut for the visual representation
main_body = main_body.faces(">Z").workplane().rect(main_box_length * 0.5, main_box_width * 0.6).cutBlind(-0.5)

# Add Handle to Main Box
# The handle is on the "front" side (let's say -Y or +Y)
# Based on image, handles are on the same side for all.
# Let's put handle on -Y face
handle_path_main = (
    cq.Workplane("XY")
    .moveTo(-main_handle_radius, -main_box_width/2)
    .threePointArc((0, -main_box_width/2 - main_handle_radius*0.4), (main_handle_radius, -main_box_width/2))
)
handle_main = (
    cq.Workplane("YZ")
    .workplane(offset=-main_handle_radius)
    .moveTo(-main_box_width/2, 0)
    .circle(main_handle_thickness)
    .sweep(handle_path_main)
)
main_obj = main_body.union(handle_main)


# 2. Medium Box (Right side in image)
med_body = cq.Workplane("XY").box(med_box_length, med_box_width, med_box_height)
# Handle on -Y face
handle_path_med = (
    cq.Workplane("XY")
    .moveTo(-med_handle_radius, -med_box_width/2)
    .threePointArc((0, -med_box_width/2 - med_handle_radius*0.4), (med_handle_radius, -med_box_width/2))
)
handle_med = (
    cq.Workplane("YZ")
    .workplane(offset=-med_handle_radius)
    .moveTo(-med_box_width/2, 0)
    .circle(med_handle_thickness)
    .sweep(handle_path_med)
)
med_obj = med_body.union(handle_med)

# Position Medium Box relative to Main
# In image: Diagonal offset? No, looks like exploded view or linear arrangement. 
# The image shows them in a line: Small - Main - Medium
# But rotated. Let's align them linearly first then apply translations.
# The image shows: Small (left-bottom), Main (center), Medium (right-top) along a diagonal axis.

med_obj = med_obj.translate((main_box_length/2 + spacing + med_box_length/2, main_box_width/2 + med_box_width/2, 0))


# 3. Small Box (Left side in image)
small_body = cq.Workplane("XY").box(small_box_length, small_box_width, small_box_height)
# Handle on -Y face
handle_path_small = (
    cq.Workplane("XY")
    .moveTo(-small_handle_radius, -small_box_width/2)
    .threePointArc((0, -small_box_width/2 - small_handle_radius*0.4), (small_handle_radius, -small_box_width/2))
)
handle_small = (
    cq.Workplane("YZ")
    .workplane(offset=-small_handle_radius)
    .moveTo(-small_box_width/2, 0)
    .circle(small_handle_thickness)
    .sweep(handle_path_small)
)
small_obj = small_body.union(handle_small)

# Position Small Box
# Move to left and down
small_obj = small_obj.translate((-main_box_length/2 - spacing - small_box_length/2, -main_box_width/2 - small_box_width/2, 0))

# For the medium object, looking at the image again:
# The main box is center.
# The medium box is to the "Upper Right".
# The small box is to the "Lower Left".
# The handles are all facing the "Lower Right" direction (roughly).

# Let's rotate/orient them to match the isometric-style view better.
# Actually, the user just wants the model. I will arrange them linearly but offset in Y to simulate the "exploded" or separate look.

# Resetting positions to match the visual better:
# Main: (0,0,0)
# Medium (Right): Shifted +X and +Y
# Small (Left): Shifted -X and -Y

# Re-translate Medium
med_obj = med_body.union(handle_med) # reset geometry
med_obj = med_obj.translate((main_box_length/2 + 20, 20, 0))

# Re-translate Small
small_obj = small_body.union(handle_small) # reset geometry
small_obj = small_obj.translate((-main_box_length/2 - 20, -20, 0))

# Combine all into result
result = main_obj.union(med_obj).union(small_obj)