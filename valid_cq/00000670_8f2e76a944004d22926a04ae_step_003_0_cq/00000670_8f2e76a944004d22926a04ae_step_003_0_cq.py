import cadquery as cq

# Parametric dimensions
width = 100.0  # Overall width of the top surface
depth = 100.0  # Overall depth of the top surface
top_thickness = 2.0  # Thickness of the black top plate
side_thickness = 5.0  # Thickness of the side walls
side_height = 10.0   # Total height of the side walls (including top thickness overlap if applicable)

# Create the top plate
# We center it on X and Y for easier manipulation
top_plate = cq.Workplane("XY").box(width, depth, top_thickness)

# Create the side supports
# The image shows supports running along two parallel edges (let's say along the Y-axis edges)
# The supports appear to be attached underneath the top plate

# Left support
left_support = (
    cq.Workplane("XY")
    .workplane(offset=-side_height + top_thickness/2) # Start from bottom of the top plate (approx)
    .center(-width/2 + side_thickness/2, 0) # Move to left edge
    .box(side_thickness, depth, side_height) # Create the wall
)

# Right support
right_support = (
    cq.Workplane("XY")
    .workplane(offset=-side_height + top_thickness/2) # Start from bottom
    .center(width/2 - side_thickness/2, 0) # Move to right edge
    .box(side_thickness, depth, side_height) # Create the wall
)

# Combine the parts
# Since the image shows the top plate as black and sides as gray, they might be distinct bodies 
# or a single assembly. For a single solid geometry, we union them.
# However, visually, the top plate sits *on top* of the rails.
# Let's adjust Z alignment to make it structurally sound.

# Re-aligning:
# Top plate z-min = 0
# Side supports z-max = 0

top_plate_aligned = cq.Workplane("XY").workplane(offset=top_thickness/2).box(width, depth, top_thickness)

support_geometry = (
    cq.Workplane("XY")
    .workplane(offset=-side_height/2) # Center of the box in Z
    .rect(width - side_thickness, depth) # Inner rectangle to cut out
    .rect(width, depth) # Outer rectangle
    .extrude(side_height) # Create the frame
)

# The image specifically shows only TWO sides, not a full frame box.
# Let's reconstruct based strictly on the visual of two parallel rails under a plate.

# 1. Top Plate
plate = cq.Workplane("XY").box(width, depth, top_thickness)

# 2. Side Rails (Legs)
# Located at the edges, extending downwards.
leg_height = 10.0
leg_width = 4.0 # Thickness of the leg
leg_length = depth # Runs the full length

# Leg 1 (Left)
leg1 = (
    cq.Workplane("XY")
    .workplane(offset=-top_thickness/2 - leg_height/2)
    .center(-width/2 + leg_width/2, 0)
    .box(leg_width, leg_length, leg_height)
)

# Leg 2 (Right)
leg2 = (
    cq.Workplane("XY")
    .workplane(offset=-top_thickness/2 - leg_height/2)
    .center(width/2 - leg_width/2, 0)
    .box(leg_width, leg_length, leg_height)
)

# Union the geometry
result = plate.union(leg1).union(leg2)