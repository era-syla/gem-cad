import cadquery as cq
import math

# --- Parameters ---
thickness = 5.0
r_outer = 130.0
r_inner = 70.0
angle_half = 40.0  # Half of the sector angle (Total 80 degrees)
slot_width = 10.0
slot_depth = 12.0
slot_radius = slot_width / 2.0

# --- Helper Functions ---
def create_slot_tool(width, depth, thickness, extra_clearance=10.0):
    """
    Creates a U-shaped slot cutting tool.
    The tool is created along the X-axis, starting at x=-extra_clearance.
    The effective cut starts at x=0 and goes to x=depth.
    """
    return (
        cq.Workplane("XY")
        .moveTo(-extra_clearance, width / 2.0)
        .lineTo(depth, width / 2.0)
        .threePointArc((depth + width / 2.0, 0), (depth, -width / 2.0))
        .lineTo(-extra_clearance, -width / 2.0)
        .close()
        .extrude(thickness)
    )

# --- Geometry Construction ---

# 1. Define Key Points for the Annular Sector
# We define the sector centered on the X-axis for symmetry, then rotate later if needed.
# Inner Arc Points
p_in_start = (r_inner * math.cos(math.radians(-angle_half)), r_inner * math.sin(math.radians(-angle_half)))
p_in_mid   = (r_inner, 0)
p_in_end   = (r_inner * math.cos(math.radians(angle_half)), r_inner * math.sin(math.radians(angle_half)))

# Outer Arc Points
p_out_start = (r_outer * math.cos(math.radians(-angle_half)), r_outer * math.sin(math.radians(-angle_half)))
p_out_mid   = (r_outer, 0)
p_out_end   = (r_outer * math.cos(math.radians(angle_half)), r_outer * math.sin(math.radians(angle_half)))

# 2. Create Base Solid (Annular Sector)
base = (
    cq.Workplane("XY")
    .moveTo(*p_in_start)
    .lineTo(*p_out_start)  # Bottom straight edge
    .threePointArc(p_out_mid, p_out_end)  # Outer convex arc
    .lineTo(*p_in_end)  # Top straight edge
    .threePointArc(p_in_mid, p_in_start)  # Inner concave arc
    .close()
    .extrude(thickness)
)

# 3. Create Slots

# Inner Slot (Right side in standard orientation, centered on inner arc)
# Located at (r_inner, 0), pointing inwards (towards +X relative to the hole center, 
# which corresponds to cutting deeper into the solid from the inner radius).
# Since the tool is defined along +X, we position it at r_inner and it cuts towards +X.
inner_slot_tool = (
    create_slot_tool(slot_width, slot_depth, thickness)
    .translate((r_inner, 0, 0))
)

# Top Slot (On the top radial edge)
# Calculate midpoint of the top edge
mx_top = (p_in_end[0] + p_out_end[0]) / 2.0
my_top = (p_in_end[1] + p_out_end[1]) / 2.0

# Calculate orientation. 
# The radial edge is at `angle_half`.
# To cut perpendicular into the material (which is 'below' the top edge), 
# we rotate -90 degrees relative to the edge vector.
rot_top = angle_half - 90.0

top_slot_tool = (
    create_slot_tool(slot_width, slot_depth, thickness)
    .rotate((0, 0, 0), (0, 0, 1), rot_top)
    .translate((mx_top, my_top, 0))
)

# Bottom Slot (On the bottom radial edge)
# Calculate midpoint
mx_bot = (p_in_start[0] + p_out_start[0]) / 2.0
my_bot = (p_in_start[1] + p_out_start[1]) / 2.0

# Orientation: Radial edge is at `-angle_half`.
# Cut perpendicular into material ('above' the bottom edge) -> +90 degrees.
rot_bot = -angle_half + 90.0

bot_slot_tool = (
    create_slot_tool(slot_width, slot_depth, thickness)
    .rotate((0, 0, 0), (0, 0, 1), rot_bot)
    .translate((mx_bot, my_bot, 0))
)

# 4. Apply Cuts
result = base.cut(inner_slot_tool).cut(top_slot_tool).cut(bot_slot_tool)

# 5. Orient to match image (Arc on Left, Points to Right)
result = result.rotate((0, 0, 0), (0, 0, 1), 180)