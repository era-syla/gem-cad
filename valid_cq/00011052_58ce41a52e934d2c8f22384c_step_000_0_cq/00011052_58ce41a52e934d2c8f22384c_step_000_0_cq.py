import cadquery as cq

# --- Parameter Definitions ---
# Overall envelope dimensions
total_length = 100.0
total_height = 60.0
total_width = 30.0
wall_thickness = 2.0

# Rectangular Box Section (Left)
box_length = 50.0  # Approx half the length
mid_wall_offset = 5.0 # Divider wall position relative to center

# Cylindrical/Rounded Section (Right)
cyl_radius = total_width / 2.0
cyl_center_x = total_length - cyl_radius

# Cutout section (Middle)
cutout_start_x = box_length
cutout_depth = 10.0  # From top face down
cutout_length = 20.0 # Length of the depressed area

# Hinge/Lug features
lug_radius = 4.0
lug_hole_radius = 2.0
lug_thickness = 4.0
lug_protrusion = 6.0
lug_spacing = 12.0 # Vertical spacing between lug centers
lug_group_height_offset = 5.0 # Offset from center line

# --- Geometry Construction ---

# 1. Base Shape: Create the main profile extrusion
# We'll sketch on the XY plane and extrude in Z (height)
base_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(cyl_center_x, 0)
    # Create the rounded end
    .threePointArc((total_length, total_width/2), (cyl_center_x, total_width))
    .lineTo(0, total_width)
    .close()
)

main_body = base_sketch.extrude(total_height)

# 2. Hollow out the rectangular section (Left side)
# We shell the left side or cut pockets. Looking at the image, there's a divider.
# Let's cut two rectangular pockets.

pocket_height = total_height - 2 * wall_thickness
pocket1_width = (total_width / 2) - wall_thickness - (wall_thickness/2) # Simple split
pocket2_width = pocket1_width

# Adjusting for a more specific divider look
divider_x_pos = wall_thickness
pocket_depth = box_length - wall_thickness

# Left Pocket 1
main_body = (
    main_body.faces("<X")
    .workplane()
    .transformed(offset=(0, -total_width/4)) # Shift to lower half
    .rect(pocket_height, (total_width/2) - wall_thickness*1.5)
    .cutBlind(-pocket_depth)
)

# Left Pocket 2
main_body = (
    main_body.faces("<X")
    .workplane()
    .transformed(offset=(0, total_width/4)) # Shift to upper half
    .rect(pocket_height, (total_width/2) - wall_thickness*1.5)
    .cutBlind(-pocket_depth)
)


# 3. Create the "Cutout" or Step-down feature on top
# This removes material from the top face in the middle section
step_cut = (
    cq.Workplane("XY")
    .rect(total_length * 2, total_width * 2) # Big cutter
    .extrude(cutout_depth)
    .translate((cutout_start_x + cutout_length/2 + 20, 0, total_height - cutout_depth/2)) # Rough positioning
)

# Better approach for the step down: Use the existing solid
main_body = (
    main_body.faces(">Z")
    .workplane()
    .center(cutout_start_x - total_length/2 + cutout_length/2, 0) # Adjust center relative to global coords
    .rect(cutout_length, total_width + 1.0) # Overkill width to ensure clean cut
    .cutBlind(-cutout_depth)
)

# 4. Hollow out the cylindrical section (Right side)
# It creates a large pocket on the side face
right_pocket_height = total_height - 2*wall_thickness
right_pocket_depth = cyl_radius - wall_thickness

# Find the flat face resulting from the step-down or the side
# Looking at the image, the pocket is on the flat side face in the rounded area.
# Wait, the image shows the pocket is on the FLAT side of the transition area, 
# and the rounded end is solid or hollowed from the end?
# Let's look closer. The far right is a half-cylinder. 
# There is a large rectangular cutout on the side face (Y-facing) of the cylindrical part.

main_body = (
    main_body.faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .center(total_length/2 - cyl_center_x, 0) # Shift towards cylinder
    .rect(cyl_radius*1.5, right_pocket_height) # Rectangular cut into the cylinder side
    .cutBlind(- (total_width - wall_thickness)) # Cut almost all the way through
)


# 5. Add the Lugs (Hinges)
# Function to create a single lug
def create_lug(workplane):
    return (
        workplane
        .circle(lug_radius)
        .extrude(lug_thickness)
        .faces(">Z").workplane()
        .circle(lug_hole_radius)
        .cutBlind(-lug_thickness)
    )

# There are two sets of lugs.
# Set 1: On the step-down vertical face (facing -X effectively inside the step)
# Set 2: On the main side face (facing -Y)

# Let's define a lug shape to union
lug_shape = (
    cq.Workplane("XY")
    .circle(lug_radius)
    .extrude(lug_thickness)
    .faces(">Z").workplane()
    .circle(lug_hole_radius)
    .cutBlind(-lug_thickness)
    # Add a tangent rectangle to connect it to the wall
    .faces("<Z").workplane()
    .rect(lug_radius*2, lug_radius*2) # Base connection
    .extrude(lug_thickness)
    .translate((-lug_radius, 0, 0)) # Shift so circle is at end
)
# Re-orient lug for side attachment
lug_solid = (
    cq.Workplane("XZ")
    .move(0,0)
    .lineTo(lug_protrusion, 0)
    .lineTo(lug_protrusion, lug_thickness)
    .lineTo(0, lug_thickness)
    .close()
    .extrude(lug_radius*2) # Base block
)
# Add rounded end
cyl_lug = (
    cq.Workplane("XY")
    .circle(lug_radius)
    .extrude(lug_thickness)
    .rotate((0,0,0), (1,0,0), 90)
    .translate((lug_protrusion, lug_radius, 0))
)
# Add hole
hole_cyl = (
    cq.Workplane("XY")
    .circle(lug_hole_radius)
    .extrude(lug_thickness*3) # long cutter
    .rotate((0,0,0), (1,0,0), 90)
    .translate((lug_protrusion, lug_radius*2, 0))
)

final_lug = (
    lug_solid.union(cyl_lug)
    .cut(hole_cyl)
    .translate((0, -lug_radius, 0)) # Center vertically
)


# Position Set 1 (On the side of the box section)
# Located on the -Y face (front face in standard view), near the transition
lug1_pos = (box_length - 5, 0, total_height/2 - lug_spacing/2)
lug2_pos = (box_length - 5, 0, total_height/2 + lug_spacing/2)

lugs_set_1 = (
    final_lug
    .rotate((0,0,0), (0,0,1), -90) # Face out Y
    .translate((box_length - wall_thickness, 0, total_height/2 - lug_spacing/2 - lug_group_height_offset))
)

lugs_set_1_b = (
    final_lug
    .rotate((0,0,0), (0,0,1), -90)
    .translate((box_length - wall_thickness, 0, total_height/2 + lug_spacing/2 - lug_group_height_offset))
)

# Position Set 2 (Inside the step-down area)
# These are attached to the vertical face created by the step down
# That face is at X = box_length (approx)
lugs_set_2 = (
    final_lug
    .translate((cutout_start_x, total_width - wall_thickness, total_height/2 - lug_spacing/2))
)

lugs_set_2_b = (
    final_lug
    .translate((cutout_start_x, total_width - wall_thickness, total_height/2 + lug_spacing/2))
)

# Actually, looking at the image again:
# One pair is on the front face (-Y) of the box section.
# The other pair is on the front face (-Y) of the *recessed* section (cylindrical part connector).
# Let's reconstruct the lugs simply using push/add on the main body to be more robust.

# Helper to add a lug pair on a face
def add_lug_pair(body, face_selector, x_offset, z_center):
    # Top Lug
    body = (
        body.faces(face_selector).workplane()
        .center(x_offset, z_center + lug_spacing/2)
        .rect(lug_thickness, lug_protrusion * 2) # Base connection
        .extrude(lug_protrusion)
        # Round the end
        .faces(">Z").edges("|Y").fillet(lug_thickness/2 - 0.1) # Approx fillet to round
        # Proper rounding using cylinder union is better usually, but let's try construction
    )
    return body

# Let's stick to the Union method, it's cleaner for complex attachments.
# Define a precise Single Lug object centered at origin
L = cq.Workplane("XY").box(lug_protrusion, lug_thickness, lug_radius*2)
C = (cq.Workplane("XY")
     .workplane(offset=lug_thickness/2)
     .circle(lug_radius).extrude(lug_thickness)
     .rotate((0,0,0), (1,0,0), -90)
     .translate((lug_protrusion/2, 0, 0))
    )
H = (cq.Workplane("XY")
     .workplane(offset=lug_thickness/2)
     .circle(lug_hole_radius).extrude(lug_thickness*3)
     .rotate((0,0,0), (1,0,0), -90)
     .translate((lug_protrusion/2, 0, -lug_thickness))
    )

single_lug = L.union(C).cut(H).translate((-lug_protrusion/2, 0, 0))

# Place Lugs on the Box Section (Front Face / -Y)
# Z height: center of part
z_mid = total_height / 2
x_box_lug = box_length - 4.0

lug_box_lower = single_lug.rotate((0,0,0),(0,0,1), -90).translate((x_box_lug, 0, z_mid - lug_spacing/2))
lug_box_upper = single_lug.rotate((0,0,0),(0,0,1), -90).translate((x_box_lug, 0, z_mid + lug_spacing/2))

# Place Lugs on the Recessed Section
# These are attached to the wall created by the pocket in the cylinder section
# Looking at the image, there is a wall dividing the cutout and the start of the cylinder.
# The lugs are attached to that wall, facing towards the cylinder pocket.
# Actually, looking at the crop, the second set of lugs is on the *same plane* as the first set,
# just further along X, attached to the thinner wall section.

x_cyl_lug = cutout_start_x + cutout_length + 2.0 

lug_cyl_lower = single_lug.rotate((0,0,0),(0,0,1), -90).translate((x_cyl_lug, 0, z_mid - lug_spacing/2))
lug_cyl_upper = single_lug.rotate((0,0,0),(0,0,1), -90).translate((x_cyl_lug, 0, z_mid + lug_spacing/2))

# Union everything
result = main_body.union(lug_box_lower).union(lug_box_upper).union(lug_cyl_lower).union(lug_cyl_upper)

# Refine the Right side Pocket based on the image
# The image shows a very deep, thin-walled pocket on the curved section.
# We cut a simple rect earlier, let's make it follow the curve
pocket_wire = (
    cq.Workplane("XY")
    .moveTo(cutout_start_x + cutout_length, wall_thickness)
    .lineTo(cyl_center_x, wall_thickness)
    .threePointArc((total_length - wall_thickness, total_width/2), (cyl_center_x, total_width - wall_thickness))
    .lineTo(cutout_start_x + cutout_length, total_width - wall_thickness)
    .close()
)

# Re-do the right pocket more accurately
# Remove the previous blind cut logic for step 4 and replace with this:
# We need to regenerate the main body without that simple cut first? 
# No, let's just patch the code structure.

# --- Code Restructuring for Clean Execution ---

# 1. Base Extrusion
base_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(cyl_center_x, 0)
    .threePointArc((total_length, total_width/2), (cyl_center_x, total_width))
    .lineTo(0, total_width)
    .close()
)
res = base_sketch.extrude(total_height)

# 2. Left Box Hollows
res = (
    res.faces("<X")
    .workplane()
    .transformed(offset=(0, -total_width/4 + wall_thickness/4)) 
    .rect(total_height - 2*wall_thickness, (total_width/2) - 1.5*wall_thickness)
    .cutBlind(- (box_length - wall_thickness))
)
res = (
    res.faces("<X")
    .workplane()
    .transformed(offset=(0, total_width/4 - wall_thickness/4))
    .rect(total_height - 2*wall_thickness, (total_width/2) - 1.5*wall_thickness)
    .cutBlind(- (box_length - wall_thickness))
)

# 3. Top Cutout (The step down)
res = (
    res.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(10, 0) # Shift X slightly positive to cover transition area
    .rect(cutout_length, total_width + 1)
    .cutBlind(-cutout_depth)
)

# 4. Right Side Pocket (The large hollow in the curve)
# We cut from the +Y face inwards
res = (
    res.faces(">Y")
    .workplane()
    .center(total_length/2 - cyl_center_x + 5, 0) # Adjust X
    .rect(cyl_radius*1.8, total_height - 2*wall_thickness)
    .cutBlind(-(total_width - wall_thickness))
)

# 5. Lugs
# Re-define single lug for cleaner code flow
L = cq.Workplane("XY").box(lug_protrusion, lug_thickness, lug_radius*2)
C = (cq.Workplane("XY")
     .workplane(offset=lug_thickness/2)
     .circle(lug_radius).extrude(lug_thickness)
     .rotate((0,0,0), (1,0,0), -90)
     .translate((lug_protrusion/2, 0, 0))
    )
H = (cq.Workplane("XY")
     .workplane(offset=lug_thickness/2)
     .circle(lug_hole_radius).extrude(lug_thickness*3)
     .rotate((0,0,0), (1,0,0), -90)
     .translate((lug_protrusion/2, 0, -lug_thickness))
    )
single_lug = L.union(C).cut(H).translate((-lug_protrusion/2, 0, 0))
single_lug = single_lug.rotate((0,0,0),(0,0,1), -90) # Orient facing -Y

# Coordinates
z_lower = total_height/2 - lug_spacing/2
z_upper = total_height/2 + lug_spacing/2
x_set1 = box_length - wall_thickness
x_set2 = box_length + cutout_length - wall_thickness 

# Add lugs
res = res.union(single_lug.translate((x_set1, 0, z_lower)))
res = res.union(single_lug.translate((x_set1, 0, z_upper)))
res = res.union(single_lug.translate((x_set2, 0, z_lower)))
res = res.union(single_lug.translate((x_set2, 0, z_upper)))

result = res