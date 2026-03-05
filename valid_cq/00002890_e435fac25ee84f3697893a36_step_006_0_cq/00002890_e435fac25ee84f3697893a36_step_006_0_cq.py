import cadquery as cq

# Parametric dimensions
box_length = 60.0
box_width = 40.0
box_height = 40.0
wall_thickness = 4.0
bottom_thickness = 4.0

# Baffle/Divider dimensions
baffle_height = 25.0
baffle_thickness = 4.0
# The image shows an angled top edge on the internal baffle
baffle_top_angle = 15.0  # degrees approximately

# Create the main box shell
# 1. Create a solid block
# 2. Shell it from the top face
box = (
    cq.Workplane("XY")
    .box(box_length, box_width, box_height)
    .faces("+Z")
    .shell(-wall_thickness)
)

# Create the internal baffle
# The baffle is positioned in the center, perpendicular to the length
baffle_sketch = (
    cq.Workplane("XZ")
    .workplane(offset=-baffle_thickness / 2.0)
    .moveTo(-box_length/2 + wall_thickness, -box_height/2 + bottom_thickness)
    .lineTo(box_length/2 - wall_thickness, -box_height/2 + bottom_thickness)
    .lineTo(box_length/2 - wall_thickness, -box_height/2 + bottom_thickness + baffle_height)
    # Creating the slight slope on top visible in the image
    .lineTo(-box_length/2 + wall_thickness, -box_height/2 + bottom_thickness + baffle_height + 5) 
    .close()
    .extrude(baffle_thickness)
)

# Alternative approach for the baffle to match the specific "L" or "Angled" shape visible
# Looking closer at the image, the internal part isn't just a straight wall. 
# It looks like a smaller rectangular extrusion rising from the floor, 
# perhaps centered or slightly offset.
# Let's refine the baffle to match the image more precisely. 
# It looks like a partial wall in the middle.

# Refined Baffle logic
internal_feature_width = box_width - (2 * wall_thickness)
internal_feature_thickness = 4.0
internal_feature_height = box_height * 0.6

# The internal feature in the image actually looks like a vertical plate
# oriented along the long axis (length) or short axis?
# Looking at perspective: The box is long. The internal plate is perpendicular to the long axis.
# It seems to be attached to the bottom and side walls?
# No, looking closely at shadows, it appears to be a divider in the middle of the "trough".
# Let's assume it's a baffle running across the width.

baffle = (
    cq.Workplane("XY")
    .workplane(offset=-box_height/2 + bottom_thickness)
    # Draw a rectangle for the baffle base
    .rect(internal_feature_thickness, internal_feature_width)
    .extrude(internal_feature_height)
)

# However, looking extremely closely at the crop, the top of the internal feature is angled.
# It looks like a simple vertical plate that has a chamfer or angle on top.
# Let's stick to a simple vertical divider with a slight angle on top as interpreted earlier,
# but positioned centrally.

final_baffle = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Centered along X
    .moveTo(-internal_feature_width/2, -box_height/2 + bottom_thickness)
    .lineTo(internal_feature_width/2, -box_height/2 + bottom_thickness)
    .lineTo(internal_feature_width/2, -box_height/2 + bottom_thickness + internal_feature_height)
    # Add a slope to the top edge to match the visual cue
    .lineTo(-internal_feature_width/2, -box_height/2 + bottom_thickness + internal_feature_height - 3.0) 
    .close()
    .extrude(internal_feature_thickness) # This extrudes along X
)

# Combine the box and the internal feature
result = box.union(final_baffle)