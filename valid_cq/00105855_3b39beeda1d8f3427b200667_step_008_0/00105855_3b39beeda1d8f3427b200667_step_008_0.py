import cadquery as cq

# --- Parameters ---
rod_diameter = 4.0
rod_radius = rod_diameter / 2.0
bend_radius = 5.0

# Dimensions estimated from the image
# Coordinate system assumption:
# Origin (0,0,0) at the start of the main horizontal rod section
# +Y: Along the main long rod
# +Z: Vertical Up
# +X: Transverse Right

main_length = 120.0
drop_height = 25.0
foot_length = 20.0
riser_height = 35.0
arm_length = 45.0
hook_return_length = 12.0
stub_length = 15.0

# --- Main Wire Path ---
# Defined as a series of 3D points
# Path starts at the tip of the bottom-left foot
p_foot_tip = (-foot_length, 0, -drop_height)
p_foot_corner = (0, 0, -drop_height)
p_main_start = (0, 0, 0)
p_junction = (0, main_length, 0)
p_riser_top = (0, main_length, riser_height)
p_arm_end = (-arm_length, main_length, riser_height)
p_hook_tip = (-arm_length, main_length - hook_return_length, riser_height)

main_points = [
    p_foot_tip,
    p_foot_corner,
    p_main_start,
    p_junction,
    p_riser_top,
    p_arm_end,
    p_hook_tip
]

# Create the raw wire for the main path
main_wire_raw = cq.Wire.makePolygon([cq.Vector(*p) for p in main_points])

# Apply fillets to the corners to simulate bent wire
# This smooths the transitions between segments
main_wire = main_wire_raw.fillet(bend_radius)

# --- Stub Wire Path ---
# The short straight segment protruding to the right at the far junction
p_stub_end = (stub_length, main_length, 0)
stub_points = [p_junction, p_stub_end]

stub_wire = cq.Wire.makePolygon([cq.Vector(*p) for p in stub_points])

# --- Sweep Geometry ---

# 1. Generate Main Body
# The start segment (foot) goes from p_foot_tip to p_foot_corner along the +X axis.
# We create a profile plane perpendicular to this start vector (YZ plane).
# The origin of the plane is set to the start point of the path.
main_body = (
    cq.Workplane("YZ", origin=p_foot_tip)
    .circle(rod_radius)
    .sweep(cq.Workplane(obj=main_wire))
)

# 2. Generate Stub Body
# The stub goes along the +X axis.
# Profile plane is YZ, centered at the junction point.
stub_body = (
    cq.Workplane("YZ", origin=p_junction)
    .circle(rod_radius)
    .sweep(cq.Workplane(obj=stub_wire))
)

# --- Combine ---
# Union the main bent wire and the welded stub
result = main_body.union(stub_body)