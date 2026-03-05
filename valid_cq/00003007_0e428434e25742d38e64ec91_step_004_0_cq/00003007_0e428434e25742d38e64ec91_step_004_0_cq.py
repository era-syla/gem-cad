import cadquery as cq

# --- Parameters ---
# Main body (rectangular block) dimensions
block_length = 40.0
block_width = 40.0
block_height = 20.0
block_fillet_radius = 2.0  # Radius for the vertical edges

# Cylindrical post dimensions
post_diameter = 20.0
post_height = 40.0

# Central hole dimensions (counterbored)
through_hole_diameter = 10.0
counterbore_diameter = 16.0
counterbore_depth = 5.0

# Side cutout dimensions (semi-circular notch)
notch_radius = 12.0
notch_center_offset = 0.0  # Center along the side face

# --- Modeling ---

# 1. Create the main rectangular block
# We center it on X and Y for easier symmetry operations
block = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .translate((0, 0, block_height / 2)) # Shift up so Z=0 is the bottom face
)

# 2. Add the vertical corner fillets
# We select edges parallel to Z axis on the block
block = block.edges("|Z").fillet(block_fillet_radius)

# 3. Create the cylindrical post extending downwards
# We attach it to the bottom face of the block
post = (
    cq.Workplane("XY")
    .circle(post_diameter / 2)
    .extrude(-post_height) # Extrude downwards
)

# Combine block and post
body = block.union(post)

# 4. Create the central counterbored hole
# We locate this on the top face
body = (
    body.faces(">Z")
    .workplane()
    .cboreHole(through_hole_diameter, counterbore_diameter, counterbore_depth)
)

# 5. Create the semi-circular cutout on the side
# Looking at the image, the cutout is on one of the side faces.
# Let's assume it's on the -Y face (back) or +Y face. Based on the cylinder alignment,
# the cylinder looks centered. The cutout is centered on one edge.
# Let's cut from the top down or from the side.
# A cylinder cut is easiest.

# Calculate position: center of the notch is on the edge of the block
# Let's place it on the -Y edge.
notch_location = (0, -block_width / 2, block_height / 2)

notch_cutter = (
    cq.Workplane("XZ") # Working on the vertical plane
    .workplane(offset=-block_width/2) # Move to the front/back face
    .center(0, block_height) # Position at the top edge
    .circle(notch_radius)
    .extrude(block_width) # Cut through enough material
)

# Since the previous approach might be tricky with alignment, let's use a simpler
# subtraction based on global coordinates.
# We want a cylinder running parallel to Z to cut the side.
notch_cutter_geo = (
    cq.Workplane("XY")
    .center(0, -block_width / 2) # Center on the edge
    .circle(notch_radius)
    .extrude(block_height * 2) # Make it tall enough
)

# Apply the cut.
result = body.cut(notch_cutter_geo)

# Re-orient/move if necessary to match the isometric view roughly
# The image shows the post going down, block on top, notch on the back-left-ish.
# The current model has Z=0 at the junction.

if __name__ == "__main__":
    # If running in an environment that supports show_object, display it
    try:
        from cadquery import show_object
        show_object(result)
    except ImportError:
        pass