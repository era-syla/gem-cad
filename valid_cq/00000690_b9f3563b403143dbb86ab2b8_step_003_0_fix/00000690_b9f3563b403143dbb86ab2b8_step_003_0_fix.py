import cadquery as cq
import math

# A-arm / wishbone suspension control arm
# Main structure: two arms meeting at a pivot point, with mounting holes

# Overall dimensions
arm_length = 100
arm_width = 8
arm_height = 10
pivot_radius = 10
mount_radius = 8

def make_arm_profile(length, width, height):
    """Create a single arm as a tapered solid"""
    pts = [
        (0, -width/2),
        (length, -width/2 * 0.6),
        (length, width/2 * 0.6),
        (0, width/2),
    ]
    result = (cq.Workplane("XY")
              .polyline(pts)
              .close()
              .extrude(height))
    return result

# Create the A-arm (wishbone shape)
# The arm has two branches that meet at the ball joint end

# Dimensions
total_length = 120
arm_sep = 40  # separation between the two mounting points
thickness = 8
height = 12
pivot_d = 20
mount_d = 16
hole_d = 8
pivot_hole_d = 10

# Branch 1: upper arm going from left mount to ball joint
# Branch 2: lower arm going from right mount to ball joint
# Ball joint at the tip (right side)

# We'll build this in the XY plane
# Ball joint center at (total_length, 0)
# Mount 1 at (0, arm_sep/2)
# Mount 2 at (0, -arm_sep/2)

ball_pt = (total_length, 0)
mount1_pt = (0, arm_sep/2)
mount2_pt = (0, -arm_sep/2)

# Create arm 1 (upper branch)
def make_branch(start, end, w, h):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.degrees(math.atan2(dy, dx))
    
    branch = (cq.Workplane("XY")
               .center(start[0], start[1])
               .rect(length, w, centered=False)
               .extrude(h)
               .translate((-0, -w/2, 0)))
    return branch

# Build the A-arm using sweep along paths
# Simpler approach: use lofted/extruded rectangles rotated into place

def rotated_box(cx, cy, dx, dy, w, h):
    """Create a box along the direction from (cx,cy) to (cx+dx, cy+dy)"""
    angle = math.degrees(math.atan2(dy, dx))
    length = math.sqrt(dx*dx + dy*dy)
    box = (cq.Workplane("XY")
           .box(length, w, h, centered=False))
    # Rotate around Z at origin, then translate
    box = box.rotate((0, 0, 0), (0, 0, 1), angle)
    box = box.translate((cx, cy, -h/2))
    return box

# Direction vectors
d1x = ball_pt[0] - mount1_pt[0]
d1y = ball_pt[1] - mount1_pt[1]
d2x = ball_pt[0] - mount2_pt[0]
d2y = ball_pt[1] - mount2_pt[1]

arm1 = rotated_box(mount1_pt[0], mount1_pt[1], d1x, d1y, arm_width, height)
arm2 = rotated_box(mount2_pt[0], mount2_pt[1], d2x, d2y, arm_width, height)

# Mount bosses
boss1 = cq.Workplane("XY").center(mount1_pt[0], mount1_pt[1]).cylinder(height, pivot_d/2)
boss2 = cq.Workplane("XY").center(mount2_pt[0], mount2_pt[1]).cylinder(height, pivot_d/2)
boss1 = boss1.translate((0, 0, -height/2))
boss2 = boss2.translate((0, 0, -height/2))

# Ball joint boss
ball_boss = cq.Workplane("XY").center(ball_pt[0], ball_pt[1]).cylinder(height, mount_d/2)
ball_boss = ball_boss.translate((0, 0, -height/2))

# Combine all parts
result = (arm1.union(arm2)
             .union(boss1)
             .union(boss2)
             .union(ball_boss))

# Cut mounting holes
result = (result
    .faces(">Z")
    .workplane()
    .pushPoints([mount1_pt, mount2_pt])
    .circle(hole_d/2)
    .cutThruAll())

result = (result
    .faces(">Z")
    .workplane()
    .pushPoints([ball_pt])
    .circle(pivot_hole_d/2)
    .cutThruAll())

# Add fillets to soften edges
try:
    result = result.edges("|Z").fillet(2)
except:
    pass