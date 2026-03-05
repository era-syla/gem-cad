import cadquery as cq

# --- Parametric Dimensions ---
# Central Panel Dimensions
panel_width = 120.0
panel_height = 80.0
panel_thickness = 2.0
rim_thickness = 4.0
rim_width = 3.0

# Side Arm Dimensions
arm_extension = 25.0  # How far out the main side block goes
arm_height = 40.0
arm_depth = 15.0
side_plate_thickness = 3.0

# Top Mounting Bracket Dimensions
mount_angle = 45.0
mount_size = 20.0
mount_thickness = 2.0

# --- Geometry Construction ---

# 1. Main Central Panel
# Create the base rectangle
panel = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)

# Create the rim around the panel
# We subtract a smaller box from a slightly larger one to make a frame, then union it
rim_outer_w = panel_width + (2 * rim_width)
rim_outer_h = panel_height + (2 * rim_width)
rim = (cq.Workplane("XY")
       .box(rim_outer_w, rim_outer_h, rim_thickness)
       .faces(">Z").workplane()
       .rect(panel_width, panel_height)
       .cutBlind(-rim_thickness) # Cut all the way through or just make a recess
       )
# In the image, the rim seems to be flush on the back or front. Let's align them.
# Let's assume the rim frames the panel.
main_body = panel.union(rim)


# 2. Side Structures (Symmetrical)
# We will model one side and mirror it.

def create_side_assembly(is_right_side=True):
    side_factor = 1 if is_right_side else -1
    
    # Position relative to the main panel edge
    x_offset = (panel_width / 2) * side_factor
    
    # A. The rounded side plate (vertical fin)
    # It looks like a rectangle with a rounded top/bottom or a specific contour.
    # Looking closely, it's a plate extending backwards.
    plate_h = panel_height * 0.7
    plate_w = 30.0
    
    # Sketching the profile of the side fin
    # It has a rounded back edge
    s_plate = (cq.Workplane("YZ")
               .workplane(offset=x_offset)
               .moveTo(0, 0)
               .lineTo(plate_w, 0)
               .threePointArc((plate_w + 5, plate_h/2), (plate_w, plate_h))
               .lineTo(0, plate_h)
               .close()
               .extrude(side_plate_thickness * -side_factor) # Extrude inwards
               )
    
    # Move the plate to align vertically with the center
    s_plate = s_plate.translate((0, 0, -plate_h/2))

    # B. The Top Angled Mounting Bracket
    # This sits on top of the side assembly.
    # It looks like a triangular prism or a bent sheet metal part.
    # Let's model it as a solid block with a cut for simplicity based on the isometric view.
    
    bracket_base_z = panel_height / 2
    bracket_x = x_offset # Start at the edge
    
    # Create a workplane angled at 45 degrees for the top piece
    # Or simply extrude a triangle profile
    
    tri_pts = [
        (0, 0),
        (25, 0),
        (0, 25)
    ]
    
    bracket = (cq.Workplane("YZ")
               .workplane(offset=bracket_x)
               .polyline(tri_pts).close()
               .extrude(15 * -side_factor) # Width of the bracket
               )
               
    # Move bracket to top corner
    bracket = bracket.translate((0, 0, bracket_base_z))
    
    # Hollow out the bracket to make it look like bent sheet metal or a frame
    # We cut a smaller triangle from inside
    cut_tri_pts = [
        (2, 2),
        (20, 2),
        (2, 20)
    ]
    bracket_cut = (cq.Workplane("YZ")
                   .workplane(offset=bracket_x + (2 * side_factor)) # Offset for wall thickness
                   .polyline(cut_tri_pts).close()
                   .extrude(11 * -side_factor)
                   )
    
    bracket = bracket.cut(bracket_cut)
    
    # C. Connecting features or details
    # The image shows some specific cutouts on the side fin.
    # Let's add a cylindrical boss or cutout on the back of the fin.
    boss = (cq.Workplane("YZ")
            .workplane(offset=x_offset + (side_plate_thickness/2 * -side_factor))
            .moveTo(25, 0)
            .circle(5)
            .extrude(5 * -side_factor)
            )

    return s_plate.union(bracket)

# Create Right Side
right_arm = create_side_assembly(is_right_side=True)

# Create Left Side (Mirror of Right)
# CadQuery creates a mirror copy
left_arm = right_arm.mirror(mirrorPlane="YZ")

# 3. Assembly
result = main_body.union(right_arm).union(left_arm)

# 4. Refinement (Optional Fillets)
# Adding some fillets to smooth edges as seen in molded parts
try:
    result = result.edges("|Z").fillet(1.0)
except:
    pass # Skip fillet if topology makes it fail

# Final Result
# show_object(result) is not needed for the requested output, just the variable assignment