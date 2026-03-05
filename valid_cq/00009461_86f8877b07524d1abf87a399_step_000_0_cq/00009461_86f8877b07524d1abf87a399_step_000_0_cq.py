import cadquery as cq
import math

# --- Parameters ---
hub_height = 40.0
hub_outer_radius = 12.0
hub_inner_radius = 8.0

arm_length = 80.0  # Distance from center to arm tip
arm_thickness = 4.0  # Thickness of the web
arm_height_start = hub_height
arm_height_end = 8.0

tip_boss_radius = 5.0
tip_hole_radius = 2.5

fillet_radius = 2.0

# Side boss/clamp block parameters
side_block_width = 15.0
side_block_length = 20.0
side_block_height = 20.0
side_block_hole_radius = 4.0

# --- Helper Functions ---
def create_arm(angle):
    """
    Creates a single arm structure oriented at a specific angle.
    The arm consists of a vertical web and a cylindrical tip.
    """
    # 1. Create the web profile
    # The web tapers from the hub height down to the tip height
    pts = [
        (hub_outer_radius, 0),
        (arm_length, 0),
        (arm_length, arm_height_end),
        (hub_outer_radius, arm_height_start)
    ]
    
    web = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .extrude(arm_thickness/2.0, both=True)
    )
    
    # 2. Create the tip boss
    tip_boss = (
        cq.Workplane("XY")
        .center(arm_length, 0)
        .circle(tip_boss_radius)
        .extrude(arm_height_end)
    )
    
    # 3. Create the hole in the tip
    tip_hole = (
        cq.Workplane("XY")
        .center(arm_length, 0)
        .circle(tip_hole_radius)
        .extrude(arm_height_end)
    )
    
    # Combine arm parts
    arm = web.union(tip_boss).cut(tip_hole)
    
    # Rotate the entire arm assembly
    return arm.rotate((0, 0, 0), (0, 0, 1), angle)

# --- Main Geometry Construction ---

# 1. Create the Central Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_outer_radius)
    .extrude(hub_height)
)

hub_hole = (
    cq.Workplane("XY")
    .circle(hub_inner_radius)
    .extrude(hub_height)
)

# 2. Create the three arms (0, 120, 240 degrees)
arm1 = create_arm(0)
arm2 = create_arm(120)
arm3 = create_arm(240)

# 3. Create the clamping/mounting block on the side of the hub
# Based on the image, there is a block protruding from the hub, likely for a screw
# to clamp the hub onto a shaft. It is located between two arms, or aligned with one.
# Looking at the image closely, the block seems to be aligned opposite one arm (or between two).
# Let's align it at 180 degrees (opposite arm1) or 60 degrees. 
# Looking at the specific render, there is one arm pointing "left-back", one "right-back", one "forward".
# The block is attached to the "right-back" arm's side of the hub, or between the forward and right-back.
# Let's place it at -60 degrees (300 degrees) to match the visual relative to the standard orientation.

block_distance = hub_outer_radius - 2.0 # Slight overlap for union
block_center_z = hub_height / 2.0 - 5.0 # Lower down on the hub

side_block = (
    cq.Workplane("XY")
    .center(0, 0)
    .workplane(offset=0) # Reset
    .transformed(rotate=(0, 0, -60)) # Rotate plane to position block
    .center(block_distance + side_block_length/2.0, 0)
    .box(side_block_length, side_block_width, side_block_height, centered=(True, True, False))
)

# Hole through the side block (tangential to hub)
side_block_hole = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 0, -60))
    .center(block_distance + side_block_length/2.0, 0)
    .workplane(offset=side_block_height/2.0)
    .transformed(rotate=(0, 90, 0)) # Rotate to drill sideways through the block
    .circle(side_block_hole_radius)
    .extrude(side_block_length + 10, both=True)
)

# Cut a slit in the hub? The image shows a line on the hub indicating a split hub design.
# Let's add a slit aligned with the block.
slit_thickness = 2.0
slit = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 0, -60))
    .center(hub_outer_radius, 0)
    .box(hub_outer_radius*2, slit_thickness, hub_height, centered=(True, True, False))
)

# --- Assembly ---

# Combine base components
result = hub.union(arm1).union(arm2).union(arm3)

# Add side block
result = result.union(side_block)

# Perform cuts
result = result.cut(hub_hole)
result = result.cut(side_block_hole)
result = result.cut(slit)

# Apply fillets to strengthen the arm-hub connections
# We select edges that are vertical and near the hub radius
try:
    result = result.edges(f"|Z and (not <Z) and (not >Z)").fillet(fillet_radius)
except:
    # Fallback if specific edge selection fails, general filleting can be tricky blindly
    pass

# Ensure the slit goes all the way through to the center hole
# Re-cut the center hole just in case the block union filled it partially
result = result.cut(hub_hole)

# Final result variable
result = result