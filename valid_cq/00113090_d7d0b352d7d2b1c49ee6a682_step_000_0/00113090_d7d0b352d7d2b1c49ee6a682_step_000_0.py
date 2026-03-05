import cadquery as cq

# Parameters derived from visual estimation
cyl_radius = 12.0
cyl_height = 15.0
hole_radius = 2.5

arm_width = 8.0
arm_top_z = 13.0        # Top surface height of the arm (slightly below cylinder top)
arm_bottom_z = 5.0      # Bottom surface height of the straight section
tip_end_z = 7.0         # Height of the vertical face at the very tip
tip_bottom_z = 0.0      # Bottom of the latch hook (flush with ground/base)

# Lengths relative to cylinder center
dist_to_hook_start = 28.0 # Distance from center to where the hook shape begins
dist_to_tip = 40.0        # Total distance from center to the tip

# 1. Create the main cylindrical body
# Extruded from XY plane (Z=0 to Z=cyl_height)
main_body = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)

# 2. Create the arm/latch geometry
# We define the side profile on the XZ plane and extrude symmetrically in Y
# The profile includes the straight section and the downward stepping hook
arm_profile = [
    (0, arm_bottom_z),                  # Start inside cylinder
    (dist_to_hook_start, arm_bottom_z), # Bottom of straight section
    (dist_to_hook_start, tip_bottom_z), # Step down to hook bottom
    (dist_to_tip, tip_bottom_z),        # Bottom corner of tip
    (dist_to_tip, tip_end_z),           # Top corner of tip (vertical face)
    (dist_to_hook_start, arm_top_z),    # Top corner of hook start (slope up)
    (0, arm_top_z)                      # Back to inside cylinder
]

arm = (
    cq.Workplane("XZ")
    .polyline(arm_profile)
    .close()
    .extrude(arm_width / 2.0, both=True)
)

# 3. Combine parts and cut the center hole
result = (
    main_body
    .union(arm)
    .faces(">Z")
    .workplane()
    .hole(hole_radius * 2)
)