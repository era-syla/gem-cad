import cadquery as cq

# --- Parametric Dimensions ---
pipe_outer_diameter = 25.0  # Diameter of the outside of the pipe
pipe_wall_thickness = 2.5   # Thickness of the pipe wall
arm_length = 30.0           # Length of each arm from the center

# Derived dimensions
pipe_radius = pipe_outer_diameter / 2.0
pipe_inner_radius = pipe_radius - pipe_wall_thickness
# The total length of the cylinder needs to account for the intersection at the center.
# We make it long enough to overlap.
full_cylinder_length = (arm_length * 2) 

# --- Geometry Construction ---

# 1. Create the main vertical cylinder (Z-axis)
# We create a cylinder centered at the origin
vertical_arm = cq.Workplane("XY").circle(pipe_radius).extrude(full_cylinder_length/2.0)
vertical_arm_down = cq.Workplane("XY").circle(pipe_radius).extrude(-full_cylinder_length/2.0) # Actually, the image is a 4-way corner piece, let's look closer.
# Re-evaluating image: It looks like a 4-way connector where 3 arms are on a plane (T-shape) and 1 goes up?
# Or is it a 3-way corner (X, Y, Z axes)? No, looking at the shadows and symmetry:
# There is a vertical arm (Z+).
# There is an arm to the right (X+).
# There is an arm to the left (X-)? No, looking at the back left, that's Y+.
# There is an arm to the front (Y-).
# Actually, looking at the intersection lines, it looks like a standard "4-way side outlet tee" or a 4-way corner.
# Let's count the openings visible: Top, Front-Left, Front-Right, Back-Left.
# That looks like 4 arms meeting at 90 degrees.
# Let's assume a standard 4-way connector shape: X+, X-, Y+, Z+.
# Wait, looking really closely at the image provided:
# 1. Top opening (Z axis)
# 2. Right opening (X axis)
# 3. Front opening (Y axis)
# 4. Left opening (X axis, extending backwards in perspective)
# It actually looks like a "Cross" fitting (4 ways on one plane) plus one vertical? No.
# Let's count the visible circular faces.
# Top face.
# Bottom-left face.
# Bottom-right face.
# Back-left face.
# This creates a shape defined by axes: +Z, +X, -X, -Y (or similar).
# Actually, it looks like a 4-way connector on the horizontal plane (like a + sign) is NOT correct.
# It looks like 3 axes meeting at a corner (X, Y, Z) plus one extension.
# Let's trace the arms:
# Arm 1: Straight Up.
# Arm 2: To the "Front Left".
# Arm 3: To the "Front Right".
# Arm 4: To the "Back Left".
# This configuration is usually a "4-way Cross" where you have a straight line (say X-axis) and a straight line (Y-axis) crossing.
# But the vertical one...
# Let's try to interpret standard PVC fittings. This looks like a "4-Way Tee" or "Side Outlet Tee".
# A Side Outlet Tee usually has a T shape + one outlet perpendicular.
# The image shows 4 identical arms radiating from a center.
# 1 Vertical.
# 3 Horizontal spaced at 90 degrees? Or 1 vertical, 1 horizontal line, 1 perpendicular horizontal?
# Let's assume it is a 4-way joint consisting of:
# - A thorough cylinder on the X axis.
# - A thorough cylinder on the Y axis.
# - (Wait, the image shows a vertical one too).
# Let's look at the junction lines.
# It looks like 4 cylinders intersecting at the origin:
# +Z, +X, -X, -Y. 
# Or +Z, +X, -Y, and maybe +Y?
# Let's count the visible pipe ends.
# 1. Top
# 2. Bottom-Left
# 3. Bottom-Right
# 4. Back-Left (partially obscured)
# This suggests 4 arms. 
# To replicate the image perfectly:
# There is a vertical tube.
# There is a horizontal tube going "left-back".
# There is a horizontal tube going "right-back".
# There is a horizontal tube going "front-left".
# This is confusing perspective. 
# Let's assume the standard engineering component: A 4-way connector composed of:
# Cylinder along X axis (full length).
# Cylinder along Y axis (full length).
# This creates a cross "+"
# Then a cylinder along Z axis (half length, just going up).
# If I look at the central joint, the lines suggest clean intersections.
# Let's assume it's a 4-way intersection (X-axis full, Y-axis full). 
# Wait, the image only shows 4 openings. A full cross on X and Y would have 4 horizontal openings. This image shows a vertical one.
# Re-reading the visual cue:
# - One vertical arm pointing UP.
# - Three horizontal arms spaced at 90 degrees (T-shape).
#   - One pointing Left.
#   - One pointing Right.
#   - One pointing "Forward" (towards camera).
# This is a standard "4-Way Tee" often used in furniture grade PVC.
# It consists of a straight pass-through (left-to-right) and two intersecting perpendiculars (one up, one forward).

# Construction Plan:
# 1. Create a Cylinder along X-axis (Left-Right).
# 2. Create a Cylinder along Z-axis (Up direction, starting from center).
# 3. Create a Cylinder along Y-axis (Forward direction, starting from center).
# 4. Union them.
# 5. Fillet the connections to make it look molded (optional but good).
# 6. Shell or hollow out the result to make it a pipe.

# Dimensions setup
L = arm_length
D = pipe_outer_diameter
R = D / 2.0

# 1. Cylinder along X (Full width: -L to +L)
c_x = cq.Workplane("YZ").circle(R).extrude(L*2).translate((-L, 0, 0))

# 2. Cylinder along Z (Center to +L)
c_z = cq.Workplane("XY").circle(R).extrude(L)

# 3. Cylinder along Y (Center to -L or +L depending on view). 
# In the image, one arm points towards us-left, one us-right.
# Standard isometric view: X is down-right, Y is up-right, Z is up.
# The image shows:
# - Vertical arm (+Z)
# - Arm to bottom-right (+X?)
# - Arm to bottom-left (-Y?)
# - Arm to back-left (-X?)
# It looks like a "Corner" (3-way) plus one extra.
# Let's stick to the "4-Way Tee" topology:
# X-axis: Through hole (2 arms)
# Z-axis: 1 arm
# Y-axis: 1 arm
# Total 4 arms.

# X Axis cylinder (Left and Right arms)
# We center it to make intersection clean
part_x = cq.Workplane("YZ").circle(R).extrude(L*2).translate((-L, 0, 0))

# Y Axis cylinder (Front arm) - We only need one side for a 4-way tee
part_y = cq.Workplane("XZ").circle(R).extrude(L).translate((0, 0, 0)) # Extrudes in +Y

# Z Axis cylinder (Top arm)
part_z = cq.Workplane("XY").circle(R).extrude(L)

# Union the solid shapes
solid_shape = part_x.union(part_y).union(part_z)

# Apply fillets to the junctions for realism
# We select edges that are shared by the cylinders
# The edges usually form "saddle" shapes at the intersection.
try:
    solid_shape = solid_shape.edges().fillet(pipe_radius * 0.1)
except:
    # Fallback if fillet fails (complex geometry intersections sometimes fail in kernels)
    pass

# Create the hollow pipe geometry
# We can do this by creating a "negative" shape and cutting it, or using shell.
# Shelling complex intersections can be tricky in OCCT, but let's try.
# Alternatively, recreate the structure with smaller cylinders and cut.
# Cutting is more robust for this specific topology.

# Inner Cylinders
R_inner = pipe_radius - pipe_wall_thickness
L_inner = L * 1.1 # slightly longer to ensure clean cut

# Inner X (Through)
cut_x = cq.Workplane("YZ").circle(R_inner).extrude(L_inner*2).translate((-L_inner, 0, 0))

# Inner Y (One side)
cut_y = cq.Workplane("XZ").circle(R_inner).extrude(L_inner)

# Inner Z (One side)
cut_z = cq.Workplane("XY").circle(R_inner).extrude(L_inner)

# Combine cutters
cutters = cut_x.union(cut_y).union(cut_z)

# Final operation
result = solid_shape.cut(cutters)