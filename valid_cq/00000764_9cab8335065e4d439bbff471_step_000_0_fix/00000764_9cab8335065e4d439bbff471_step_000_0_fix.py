import cadquery as cq
import math

# Parameters
arm_thickness = 8
arm_width = 10
clamp_outer_r = 12
clamp_inner_r = 8
clamp_height = 20
fin_height = 25
fin_thickness = 5

# Create the main curved arm using a sweep path
# The arm curves from lower-left to upper-right
# Left clamp at bottom-left, right clamp at upper-right

# Define the sweep path as a spline
path_pts = [
    (0, 0, 0),
    (20, 10, 0),
    (50, 25, 0),
    (80, 30, 0),
    (100, 25, 0),
]

# Build the arm as a swept solid
arm_path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline([(20, 10), (50, 25), (80, 30), (100, 25)])
)

# Use loft approach instead - build the arm as a box then shape it
# Let's build it more simply with extrude + cuts

# Main arm body - create as a thick curved bar
# We'll approximate with a series of boxes and unions

# Actually, let's build this as an extruded profile swept along a path
# Arm cross section is rectangular

# Build the curved arm using workplane and extrude
# The part has:
# 1. A curved arm body
# 2. Left cylindrical clamp (with split/bolt hole)  
# 3. Right cylindrical clamp (with split/bolt hole)
# 4. A triangular fin/gusset on top

# Arm path: from (0,0) curving up to (100, 30) in XY plane
# Using a series of segments to approximate

def make_arm():
    # Create arm as extruded path
    arm = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .spline([(30, 5), (70, 20), (100, 25)], includeCurrent=True)
        .workplane()
    )
    
    # Use a different approach: create rectangular cross-section swept along path
    profile = cq.Workplane("YZ").rect(arm_thickness, arm_width)
    
    path = cq.Workplane("XY").spline([(0,0), (30,5), (70,20), (100,25)])
    
    swept_arm = profile.sweep(path)
    return swept_arm

# Build components separately and union them

# Curved arm - approximate as a lofted/swept shape
# Create the arm using a simpler method: extrude a rectangular profile

# Path for the arm (in XY plane)
arm_path_wire = (
    cq.Workplane("XY")
    .moveTo(-5, 0)
    .spline([(-5, 0), (25, 8), (55, 22), (95, 27), (105, 25)], includeCurrent=False)
    .wire()
)

# Cross section for sweep
cross_section = cq.Workplane("YZ").rect(arm_width, arm_thickness)

# Build swept arm
try:
    path_wire = cq.Workplane("XY").moveTo(0, 0).spline([(30, 8), (65, 22), (100, 25)], includeCurrent=True)
    swept = cq.Workplane("YZ").rect(arm_width, arm_thickness).sweep(path_wire)
except:
    swept = cq.Workplane("XY").box(110, arm_width, arm_thickness)

# Left clamp cylinder at (0, 0)
left_clamp = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .cylinder(clamp_height, clamp_outer_r)
    .translate((0, 0, clamp_height/2))
)

# Right clamp cylinder at (100, 25)
right_clamp = (
    cq.Workplane("XY")
    .cylinder(clamp_height, clamp_outer_r)
    .translate((100, 25, clamp_height/2))
)

# Combine
combined = swept.union(left_clamp).union(right_clamp)

# Cut inner holes for clamps
left_hole = (
    cq.Workplane("XY")
    .cylinder(clamp_height + 2, clamp_inner_r)
    .translate((0, 0, clamp_height/2))
)
right_hole = (
    cq.Workplane("XY")
    .cylinder(clamp_height + 2, clamp_inner_r)
    .translate((100, 25, clamp_height/2))
)

combined = combined.cut(left_hole).cut(right_hole)

# Add fin/gusset - triangular plate on top of middle section
fin = (
    cq.Workplane("XY")
    .workplane(offset=arm_thickness)
    .moveTo(30, 8)
    .lineTo(70, 22)
    .lineTo(50, 35)
    .close()
    .extrude(fin_thickness)
)

combined = combined.union(fin)

# Add small holes along the arm
for x_pos, y_pos in [(25, 6), (45, 14), (65, 20), (80, 24)]:
    hole = (
        cq.Workplane("XZ")
        .workplane(offset=y_pos)
        .circle(2)
        .extrude(20)
        .translate((x_pos, 0, arm_thickness/2))
    )
    combined = combined.cut(hole)

result = combined