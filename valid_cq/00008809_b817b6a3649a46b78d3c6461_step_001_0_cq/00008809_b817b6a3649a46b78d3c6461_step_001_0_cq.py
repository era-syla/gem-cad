import cadquery as cq

# --- Parameters ---
# Overall dimensions
overall_width = 40.0
overall_length = 35.0  # Length of the main box section
overall_height = 15.0
wall_thickness = 2.0
base_thickness = 2.0

# Mounting tab dimensions
tab_width = 40.0
tab_length = 15.0
tab_fillet_radius = 5.0
tab_hole_diameter = 5.0
tab_hole_spacing = 22.0

# Cutout details
# The U-shaped cutout on the front wall
cutout_radius = 5.0
cutout_center_offset = 8.0 # Offset from the left wall

# Chamfers and Fillets
internal_corner_chamfer = 3.0
external_corner_radius = 4.0

# --- Geometry Construction ---

# 1. Base Shape: Create the main rectangular block and the tab extension
# We will model the outer footprint first.
main_body = (
    cq.Workplane("XY")
    .rect(overall_width, overall_length)
    .extrude(overall_height)
)

# Create the mounting tab section
# We position it at the "back" of the main box
tab_center_y = overall_length/2 + tab_length/2
tab_body = (
    cq.Workplane("XY")
    .center(0, tab_center_y)
    .rect(tab_width, tab_length)
    .extrude(overall_height)
)

# Combine the main box and the tab
full_solid = main_body.union(tab_body)

# 2. Rounding the corners
# The image shows rounded outer corners on the main box and the tab
# Let's fillet the vertical edges.
# The tab needs larger fillets at the back corners.

# Select vertical edges
full_solid = (
    full_solid
    .edges("|Z")
    .fillet(external_corner_radius)
)

# 3. Create the internal shell (hollow out)
# We remove material from the top, leaving walls and a floor.
# Instead of a simple shell, we'll make a subtraction shape to control chamfers.
cavity_shape = (
    cq.Workplane("XY")
    .rect(overall_width - 2*wall_thickness, overall_length - 2*wall_thickness)
    .extrude(overall_height)
    # Move cavity up to create floor
    .translate((0, 0, base_thickness)) 
)

# Apply chamfers to the vertical corners of the cavity
cavity_shape = (
    cavity_shape
    .edges("|Z")
    .chamfer(internal_corner_chamfer)
)

# Subtract the cavity
result = full_solid.cut(cavity_shape)

# 4. Add the mounting holes on the tab
# We need two counterbored or simple holes on the tab. The image shows simple holes.
# Position relative to the tab center.
hole_y_pos = tab_center_y
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-tab_hole_spacing/2, hole_y_pos)
    .hole(tab_hole_diameter)
    .moveTo(tab_hole_spacing/2, hole_y_pos)
    .hole(tab_hole_diameter)
)

# 5. Create the U-shaped cutout on the front/side wall
# Looking at the image, there is a U-shaped slot on one of the side walls (let's say Left or Front).
# Based on orientation relative to the tab, it's on the side perpendicular to the tab.
# Let's place it on the -X face (left side if looking from front, but orientation is arbitrary).
# To match image perspective: 
# If Tab is "Back" (+Y), and the U-cutout is on the "Left" (-X) wall.

cutout_z_center = overall_height # The cutout comes down from the top edge
cutout_depth = 6.0 # How deep down it goes

# We create a cylinder to cut out the U-shape
cutout_shape = (
    cq.Workplane("YZ")
    .center(-overall_length/4, overall_height) # Position roughly on the side wall
    .circle(cutout_radius)
    .extrude(overall_width + 10) # Make it long enough to cut through
    .translate((-overall_width/2 - 5, 0, 0)) # Move to the correct side
)

# Alternatively, sketch it on the side face
cutout_location = (
    result.faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .center(-overall_length/6, overall_height/2) # Fine tuning position based on visual estimate
)

# Let's redefine the cutout to be more precise based on the image:
# It's a U-shape cutting down from the top rim.
result = (
    result
    .faces("<X") # Select the left face
    .workplane(centerOption="ProjectedOrigin")
    # Move to the top edge, somewhat forward from the center
    .moveTo(0, overall_height) 
    .move(-8, 0) # Move along Y (which is X in local coordinates)
    # Draw the U shape profile to cut
    .lineTo(-8, overall_height - 5)
    .threePointArc((-14, overall_height - 8), (-20, overall_height - 5))
    .lineTo(-20, overall_height)
    .close()
    .cutThruAll()
)

# Re-doing the cutout with a simpler cylinder subtraction which often yields cleaner geometry for simple slots
# The slot is on the left wall (-X).
cutout_pos_y = -5.0 # relative to center of main box
cutout_pos_z = overall_height
cutout_r = 3.5

# Create a cutter object
cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-overall_width/2) # Move to the left face plane
    .center(cutout_pos_y, cutout_pos_z)
    .circle(cutout_r)
    .extrude(wall_thickness * 3) # Cut inwards
)

result = result.cut(cutter)


# 6. Final fillet touch-up (optional based on image smoothness)
# The image shows slight chamfers/fillets on the top edges.
try:
    result = result.edges(">Z").fillet(0.5)
except:
    pass # Sometimes fillets fail on complex intersections

# Export or Render
if 'show_object' in globals():
    show_object(result)