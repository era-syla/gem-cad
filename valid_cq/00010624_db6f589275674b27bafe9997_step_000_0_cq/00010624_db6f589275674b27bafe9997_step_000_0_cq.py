import cadquery as cq

# Parametric dimensions
base_width = 20.0
base_depth = 20.0
base_height = 40.0

# Top feature dimensions
# The large block on the left
feat1_width = 5.0
feat1_depth = 12.0  # Estimated based on visual proportion
feat1_height = 10.0
feat1_x_offset = - (base_width/2) + (feat1_width/2) # Aligned to left edge
feat1_y_offset = (base_depth/2) - (feat1_depth/2)   # Aligned to back edge

# The tall thin block in the back-right corner
feat2_width = 5.0
feat2_depth = 5.0
feat2_height = 15.0 # Taller than the others
feat2_x_offset = (base_width/2) - (feat2_width/2)   # Aligned to right edge
feat2_y_offset = (base_depth/2) - (feat2_depth/2)   # Aligned to back edge

# The short thin block in the front-right corner
feat3_width = 5.0
feat3_depth = 5.0
feat3_height = 10.0 # Same height as the large block
feat3_x_offset = (base_width/2) - (feat3_width/2)   # Aligned to right edge
feat3_y_offset = - (base_depth/2) + (feat3_depth/2) # Aligned to front edge

# Create the main base block
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# Create the top features
# We select the top face of the base to draw on
result = (
    base.faces(">Z").workplane()
    # Feature 1: Large block on the left
    .center(feat1_x_offset, feat1_y_offset)
    .rect(feat1_width, feat1_depth)
    .extrude(feat1_height)
    
    # Feature 2: Tall block on the back right
    # Reset workplane to the top face of the original base
    .faces("<Z").workplane(offset=base_height/2) # Go back to base top level
    .center(feat2_x_offset, feat2_y_offset)
    .rect(feat2_width, feat2_depth)
    .extrude(feat2_height)

    # Feature 3: Block on the front right
    # Reset workplane again
    .faces("<Z").workplane(offset=base_height/2) # Go back to base top level
    .center(feat3_x_offset, feat3_y_offset)
    .rect(feat3_width, feat3_depth)
    .extrude(feat3_height)
)

# Combine everything into a single solid (although the method above already unites them)
result = result.combine()