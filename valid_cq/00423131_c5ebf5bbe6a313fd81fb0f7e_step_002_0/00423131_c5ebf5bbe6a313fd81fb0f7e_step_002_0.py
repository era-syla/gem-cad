import cadquery as cq

# Parametric dimensions
handle_radius = 12.0
handle_length = 90.0
arm_length = 55.0
arm_neck_radius = 7.0
ball_radius = 16.0

# 1. Main Handle Shaft (Cylinder aligned along X axis)
# Created on YZ plane and extruded in X
handle_shaft = cq.Workplane("YZ").circle(handle_radius).extrude(handle_length)

# 2. Handle Grip End (Sphere to round off the start of the handle)
# Centered at (0, 0, 0)
handle_end = cq.Workplane("YZ").sphere(handle_radius)

# 3. Elbow Joint (Sphere at the junction)
# Centered at (handle_length, 0, 0)
elbow = cq.Workplane("YZ").workplane(offset=handle_length).sphere(handle_radius)

# 4. Tapered Arm (Cone connecting Handle to Ball)
# Aligned along Y axis. Created by lofting two circles on XZ planes.
# Base circle at Y=0, Top circle at Y=arm_length.
# Both centered at X=handle_length in global coordinates.
arm = (
    cq.Workplane("XZ")
    .center(handle_length, 0)
    .circle(handle_radius)           # Base profile matching elbow radius
    .workplane(offset=arm_length)    # Move along Y axis
    .circle(arm_neck_radius)         # Top profile (narrow neck)
    .loft(combine=False)
)

# 5. Ball End (Sphere at the tip of the arm)
# Centered at (handle_length, arm_length, 0)
ball_end = (
    cq.Workplane("XZ")
    .workplane(offset=arm_length)
    .center(handle_length, 0)
    .sphere(ball_radius)
)

# Combine all components into the final solid
result = (
    handle_shaft
    .union(handle_end)
    .union(elbow)
    .union(arm)
    .union(ball_end)
)