import cadquery as cq

# Parametric dimensions
arm_length = 85.0       # Length of the straight section
arm_height = 15.0       # Height of the rectangular profile / Thickness of the hook
width = 12.0            # Width of the part (extrusion depth)
hook_gap = 12.0         # Gap inside the hook
slot_length = 18.0      # Length of the slot
slot_width = 7.0        # Width of the slot
slot_offset = 15.0      # Distance from the back face to slot center

# Derived dimensions
r_inner = hook_gap / 2.0
r_outer = r_inner + arm_height
tip_radius = arm_height / 2.0

# Generate the geometry
# 1. Create the main J-hook profile on the XY plane
# Origin (0,0) is located at the transition between the straight arm and the hook curve (bottom edge)
result = (
    cq.Workplane("XY")
    .moveTo(arm_length, 0)
    .lineTo(0, 0)
    # Outer Curve: 180 degree arc counter-clockwise
    # Start: (0,0), End: (0, 2*r_outer), Mid: (-r_outer, r_outer)
    .threePointArc((-r_outer, r_outer), (0, 2 * r_outer))
    # Tip Cap: 180 degree arc clockwise (bulging outwards/right)
    # Connects outer profile to inner profile
    # Start: (0, 2*r_outer), End: (0, 2*r_outer - arm_height)
    .threePointArc((tip_radius, 2 * r_outer - tip_radius), (0, 2 * r_outer - arm_height))
    # Inner Curve: 180 degree arc clockwise
    # Start: (0, 2*r_outer - arm_height), End: (0, arm_height), Mid: (-r_inner, arm_height + r_inner)
    .threePointArc((-r_inner, arm_height + r_inner), (0, arm_height))
    .lineTo(arm_length, arm_height)
    .close()
    .extrude(width)
)

# 2. Cut the slot
# We select the face corresponding to the sketch plane (Z=0 relative to extrusion)
# to define the 2D slot profile, then cut through the entire solid.
result = (
    result.faces("<Z")
    .workplane()
    .moveTo(arm_length - slot_offset, arm_height / 2.0)
    .slot2D(slot_length, slot_width, angle=0)
    .cutThruAll()
)