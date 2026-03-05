import cadquery as cq

# Define parametric dimensions based on visual aspect ratio
post_width = 10.0      # X dimension of the cross-section
post_depth = 10.0      # Y dimension of the cross-section
post_height = 140.0    # Z dimension (height)
spacing = 35.0         # Center-to-center distance between the posts

# Create the model
# 1. Start a workplane on the XY plane
# 2. Define two center points for the posts
# 3. Sketch rectangles at those points
# 4. Extrude to create the vertical pillars
result = (
    cq.Workplane("XY")
    .pushPoints([(-spacing / 2, 0), (spacing / 2, 0)])
    .rect(post_width, post_depth)
    .extrude(post_height)
)