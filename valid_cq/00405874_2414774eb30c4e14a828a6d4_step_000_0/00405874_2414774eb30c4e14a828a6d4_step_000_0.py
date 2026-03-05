import cadquery as cq

# Parametric dimensions
base_length = 120.0
base_width = 60.0
base_thickness = 5.0
post_diameter = 8.0
post_height = 60.0
post_spacing = 90.0  # Distance between the centers of the two posts

# Generate the geometry
# 1. Create the rectangular base centered on the XY plane
# 2. Select the top face of the base
# 3. Create a workplane on the top face
# 4. Define the center points for the two posts
# 5. Draw the circles for the posts
# 6. Extrude the circles upwards to create the posts
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-post_spacing / 2, 0), (post_spacing / 2, 0)])
    .circle(post_diameter / 2)
    .extrude(post_height)
)