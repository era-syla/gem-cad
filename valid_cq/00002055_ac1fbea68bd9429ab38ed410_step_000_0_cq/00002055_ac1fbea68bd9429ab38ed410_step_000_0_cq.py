import cadquery as cq

# Parametric dimensions
large_cyl_diameter = 40.0
large_cyl_length = 30.0

small_cyl_diameter = 25.0
small_cyl_length = 40.0

neck_diameter = 15.0
neck_length = 10.0

# Create the larger cylinder (the base/main body on the right)
# We orient it along an axis (e.g., Y-axis)
large_cyl = (
    cq.Workplane("XY")
    .circle(large_cyl_diameter / 2.0)
    .extrude(large_cyl_length)
)

# Create the smaller cylinder (the protruding part on the left)
# It is parallel to the large cylinder but offset in position.
# From the image, they look connected by a "neck".
# Let's assume a T-junction or an offset connection.
# Looking closely at the image:
# 1. There is a large cylinder on the right.
# 2. There is a smaller cylinder on the left.
# 3. They are connected by a thinner neck cylinder.
# 4. The axes seem to be perpendicular. The large cylinder looks like a vertical post or horizontal drum, 
#    and the smaller one sticks out from the side via the neck.

# Let's refine the orientation assumption based on the image:
# It looks like two parallel cylinders connected by a perpendicular neck.
# Or, more likely, it's a "cam follower" or "offset pin" style shape.
# Let's assume:
# - Cylinder A (Right): Large diameter, axis along Y.
# - Cylinder B (Left): Smaller diameter, axis along Y (parallel).
# - Connection: A cylinder connecting them, axis along X (perpendicular to A and B).

# Re-evaluating the image perspective:
# The right cylinder face is circular. The left cylinder face is circular.
# They seem to share a plane on one side? No, they look offset.
# Let's try this construction:
# 1. Main large cylinder.
# 2. A neck cylinder perpendicular to the curved surface of the large cylinder.
# 3. A top cylinder perpendicular to the neck (making it parallel to the main cylinder).

# Revised Dimensions for this specific topology
main_cyl_radius = 20.0
main_cyl_height = 25.0

top_cyl_radius = 12.0
top_cyl_height = 35.0

neck_radius = 8.0
neck_height = 10.0 # Distance between the two cylinders surfaces

# Construction
# 1. Create the main large cylinder. Let's align its axis along Z.
main_body = cq.Workplane("XY").circle(main_cyl_radius).extrude(main_cyl_height)

# 2. Create the neck. It needs to protrude from the side of the main body.
# We'll create a plane on the side of the cylinder (e.g., XZ plane, offset by radius)
# However, attaching a cylinder to a cylinder usually involves a union.
# Let's define the center points.

# Let center of main cylinder be (0,0,0) to (0,0,height).
# We want the neck to stick out along the X axis.
# Center of neck starts at cylinder surface? Or center? 
# Let's start neck at center x=0 and go to x = main_radius + neck_length
neck_total_length = main_cyl_radius + neck_height + top_cyl_radius # Distance to center of top cylinder
neck = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center of the main cylinder
    .center(main_cyl_height/2.0, 0) # Move to middle of Z height
    .circle(neck_radius)
    .extrude(neck_total_length) # Extrude along X
)

# 3. Create the top/offset cylinder.
# Its center is at x = neck_total_length.
# Its axis is parallel to Z (or whatever the main axis is).
# Let's align it parallel to the main cylinder.
top_body = (
    cq.Workplane("XY")
    .workplane(offset=main_cyl_height/2.0 - top_cyl_height/2.0) # Center vertically relative to neck
    .center(neck_total_length, 0) # Move to the end of the neck
    .circle(top_cyl_radius)
    .extrude(top_cyl_height)
)

# Combine everything
# Note: The 'neck' calculation above extrudes from x=0. This means it's inside the main cylinder.
# This ensures a solid boolean union without gaps.
result = main_body.union(neck).union(top_body)

# Refine visually based on image:
# The image shows the smaller cylinder (left) is longer than the larger cylinder (right)?
# Or maybe the large one is just a "head".
# Let's adjust dimensions to match the visual proportions better.
# Right cylinder (main): Large diameter, short length.
# Left cylinder (top): Smaller diameter, longer length.
# Neck: Small diameter, short length.

dim_main_dia = 30.0
dim_main_len = 15.0

dim_small_dia = 18.0
dim_small_len = 35.0

dim_neck_dia = 12.0
dim_neck_len = 10.0  # Gap between them

# Re-doing construction with clearer relative positioning
# Axis A (Main): Along Y axis
# Axis B (Small): Along Y axis, offset by (RadiusA + Gap + RadiusB) in X
# Connector: Along X axis

# Center of Main Cylinder
c1 = (
    cq.Workplane("XZ")
    .circle(dim_main_dia / 2.0)
    .extrude(dim_main_len)
)

# Center distance
center_dist = (dim_main_dia/2.0) + dim_neck_len + (dim_small_dia/2.0)

# Small Cylinder (offset)
# We center it vertically relative to the main cylinder for symmetry? 
# The image shows the small cylinder is centered on the neck, and the neck is centered on the large cylinder.
c2 = (
    cq.Workplane("XZ")
    .center(center_dist, 0)
    .circle(dim_small_dia / 2.0)
    .extrude(dim_small_len)
)

# The Extrusions above go from Y=0 to Y=length.
# To center them relative to the neck (which we'll put at some Z height?), let's handle the Z/Y alignment.
# Let's act as if Y is the "long" axis of the cylinders.
# We want the neck to connect the midpoints of the lengths.

# Redoing with Workplane("XY") as the cross-section plane for cylinders, Extruding in Z.
# Then we rotate the whole thing or just build that way.
# Let's stick to creating simple shapes and uniting them at coordinates.

# 1. Right Cylinder (Large, short)
# Oriented along Y axis. Centered at local origin.
right_cyl = cq.Solid.makeCylinder(
    radius=dim_main_dia / 2.0,
    height=dim_main_len,
    pnt=cq.Vector(0, -dim_main_len / 2.0, 0),
    dir=cq.Vector(0, 1, 0)
)

# 2. Left Cylinder (Small, long)
# Oriented along Y axis. Parallel to Right Cylinder. Offset in X.
left_cyl_x_offset = -center_dist # Moving to the left
left_cyl = cq.Solid.makeCylinder(
    radius=dim_small_dia / 2.0,
    height=dim_small_len,
    pnt=cq.Vector(left_cyl_x_offset, -dim_small_len / 2.0, 0),
    dir=cq.Vector(0, 1, 0)
)

# 3. Neck Cylinder
# Oriented along X axis. Connects origin to offset.
# Length covers the gap + overlap into bodies to ensure solid union.
neck = cq.Solid.makeCylinder(
    radius=dim_neck_dia / 2.0,
    height=abs(left_cyl_x_offset), # Distance between centers
    pnt=cq.Vector(0, 0, 0), # Start at center of right cyl
    dir=cq.Vector(-1, 0, 0) # Point towards left cyl
)

# Convert Solids to Compound/Workplane for final result variable
result = cq.Workplane("XY").newObject([right_cyl, left_cyl, neck])
result = result.combine()

# Adjust alignment: The image shows the ends might not be centered. 
# The neck connects the side of the large cylinder to the side of the small cylinder.
# The small cylinder (left) seems shifted "forward" (towards the camera) compared to the right one?
# No, usually these are symmetric "dumbbells". Let's assume symmetry.
# The previous code centers them on the Y-axis.

# Final check of image proportions:
# The Right cylinder looks like a thick disk.
# The Left cylinder looks like a longer shaft.
# The code implements this logic.