import cadquery as cq

# Parameters
bowl_radius = 25.0
bowl_thickness = 2.0
hinge_radius = 4.0
hinge_length = 14.0
hinge_hole_radius = 2.5
arm_height = 40.0
arm_width = 5.0
arm_thickness = 5.0

# 1. Create the Main Bowl (Hemisphere Shell)
# Create outer sphere
s_outer = cq.Workplane("XY").sphere(bowl_radius)
# Create inner sphere for cut
s_inner = cq.Workplane("XY").sphere(bowl_radius - bowl_thickness)
# Cut to make hollow
bowl_hollow = s_outer.cut(s_inner)
# Cut the top half to create a hemisphere (keeping Z < 0)
# We use a large box to remove the top half
bowl = bowl_hollow.cut(
    cq.Workplane("XY").workplane(offset=bowl_radius).box(bowl_radius*3, bowl_radius*3, bowl_radius*2)
)

# 2. Left Hinge (Cylindrical Boss)
# Located at (-R, 0, 0), Axis along Y
left_hinge = (
    cq.Workplane("XZ")
    .moveTo(-bowl_radius, 0)
    .circle(hinge_radius)
    .extrude(hinge_length / 2.0, both=True)
)
# Hole for Left Hinge
left_hinge_hole = (
    cq.Workplane("XZ")
    .moveTo(-bowl_radius, 0)
    .circle(hinge_hole_radius)
    .extrude(hinge_length, both=True)
)
left_hinge = left_hinge.cut(left_hinge_hole)

# 3. Right Side Structure
# Base Hinge (Cylindrical Boss) at (R, 0, 0)
right_base = (
    cq.Workplane("XZ")
    .moveTo(bowl_radius, 0)
    .circle(hinge_radius)
    .extrude(hinge_length / 2.0, both=True)
)

# Arm Stem
# A curved beam extending from the right hinge upwards
# Defined by a profile on the XZ plane, extruded in Y
stem_pts = [
    (bowl_radius, 0),  # Start at hinge center
    (bowl_radius - 2, 8),
    (bowl_radius - 10, arm_height),  # Top point inner
    (bowl_radius - 10 + arm_thickness, arm_height), # Top point outer
    (bowl_radius + 4, 0) # Bottom point outer
]

arm_stem = (
    cq.Workplane("XZ")
    .moveTo(stem_pts[0][0], stem_pts[0][1])
    .threePointArc((bowl_radius - 3, arm_height/2), stem_pts[2]) # Inner curve
    .lineTo(stem_pts[3][0], stem_pts[3][1]) # Top flat
    .threePointArc((bowl_radius + 1, arm_height/2), stem_pts[4]) # Outer curve
    .close()
    .extrude(arm_width / 2.0, both=True)
)

# Top Hook (C-Clip)
# Located at the top of the arm
hook_center = cq.Vector(bowl_radius - 10 + arm_thickness/2, 0, arm_height)
hook_od = 6.0
hook_id = 4.0
hook_w = 6.0

# Basic cylinder for hook
hook_geo = (
    cq.Workplane("XZ") # Orientation plane
    .workplane(offset=0) # Centered
    .moveTo(hook_center.x, hook_center.z)
    .circle(hook_od)
    .extrude(hook_w / 2.0, both=True)
)
# Hole
hook_hole = (
    cq.Workplane("XZ")
    .moveTo(hook_center.x, hook_center.z)
    .circle(hook_id)
    .extrude(hook_w, both=True)
)
# Cutout for the C-shape (opening facing roughly towards origin/down)
hook_cut = (
    cq.Workplane("XZ")
    .moveTo(hook_center.x, hook_center.z)
    .rect(hook_od*2, hook_od*2, centered=True) # Start with full rect
    .extrude(hook_w, both=True)
)
# Create a specific cutting shape to open the C-ring
# Rotate a box to cut a segment
cut_box = (
    cq.Workplane("XY")
    .transformed(offset=hook_center, rotate=cq.Vector(0, 0, 0))
    .box(10, 10, 10, centered=(False, True, True)) # Box extending in +X
    .rotateAboutCenter(cq.Vector(0,1,0), -135) # Rotate cut direction
)

hook_final = hook_geo.cut(hook_hole).cut(cut_box)

# Top Tab
# Rectangular block on top of the hook structure
tab = (
    cq.Workplane("XY")
    .transformed(offset=hook_center + cq.Vector(-1, 0, hook_od - 1))
    .box(8, arm_width, 2.5)
)

# 4. Assembly
result = (
    bowl
    .union(left_hinge)
    .union(right_base)
    .union(arm_stem)
    .union(hook_final)
    .union(tab)
)