import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions of the image

# Base Plate
base_width = 80.0
base_depth = 50.0
base_thickness = 8.0
hole_dia = 6.0
hole_inset = 8.0

# Vertical Post (Square Tubing)
post_width = 30.0  # Outer width
post_height = 200.0
wall_thickness = 3.0

# Angled Arm (Square Tubing)
arm_length = 100.0  # Length along the angled vector
arm_angle = 45.0    # Angle from vertical
arm_start_height = 120.0 # Height where the arm branches off

# --- Geometry Construction ---

# 1. Create the Base Plate
# Rectangular base centered on XY plane
base = (
    cq.Workplane("XY")
    .box(base_width, base_depth, base_thickness)
    .faces(">Z")
    .workplane()
    .rect(base_width - 2*hole_inset, base_depth - 2*hole_inset, forConstruction=True)
    .vertices()
    .cboreHole(hole_dia, hole_dia + 4.0, 2.0) # Simple counterbore for visual accuracy
)

# 2. Create the Vertical Post
# Square tube extrusion
vertical_post_solid = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2) # Start on top of the base
    .rect(post_width, post_width)
    .extrude(post_height)
)

# Hollow out the vertical post
vertical_post_hollow = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .rect(post_width - 2*wall_thickness, post_width - 2*wall_thickness)
    .extrude(post_height)
)
# Subtract inner from outer to make tube
post = vertical_post_solid.cut(vertical_post_hollow)


# 3. Create the Angled Arm
# We create a new workplane rotated to the desired angle
arm_plane = (
    cq.Workplane("XZ")
    .transformed(offset=(0, arm_start_height, 0), rotate=(0, -arm_angle, 0))
)

# Create the solid arm
arm_solid = (
    arm_plane
    .rect(post_width, post_width)
    .extrude(arm_length)
)

# Create the hollow part for the arm
arm_hollow = (
    arm_plane
    .rect(post_width - 2*wall_thickness, post_width - 2*wall_thickness)
    .extrude(arm_length)
)

# Make the arm a tube
arm = arm_solid.cut(arm_hollow)


# 4. Combine and Clean Up
# Combine base, post, and arm
structure = base.union(post).union(arm)

# Because the arm penetrates the post, the hollow inside might be blocked.
# To ensure a continuous internal cavity (fluid/cable path), we should re-cut the hollows.
# However, for a simple visual model as requested, a simple boolean union is usually sufficient.
# To make it strictly correct like real tubing welded together:
# We need to ensure the "hollow" of the arm cuts through the wall of the post, 
# and the hollow of the post cuts through the start of the arm.

# Let's refine the union logic to ensure the internal cavity is clear.
# A robust way is to union all solids first, then subtract all hollows.

full_solid_geometry = (
    base
    .union(vertical_post_solid)
    .union(arm_solid)
)

# Create a combined cutter for the internal volume
# We need to extend the hollows slightly to ensure they intersect properly
post_cutter = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .rect(post_width - 2*wall_thickness, post_width - 2*wall_thickness)
    .extrude(post_height)
)

# For the arm cutter, we extend it backwards (negative extrusion) to pierce the main post
arm_cutter = (
    arm_plane
    .rect(post_width - 2*wall_thickness, post_width - 2*wall_thickness)
    .extrude(arm_length, both=True) # Extrude both ways to clear the intersection
)

# Cut the hollows from the main solid
result = full_solid_geometry.cut(post_cutter).cut(arm_cutter)

# Export or display
# show_object(result) # Only needed in CQ-editor