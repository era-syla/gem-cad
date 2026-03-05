import cadquery as cq
import math

# This is a suspension A-arm / wishbone control arm
# It has:
# - A large cylindrical bushing on the left (pivot end)
# - Two smaller cylindrical bushings at the right end (ball joint ends)
# - Two arms connecting the left bushing to the right bushings
# - A cross-brace between the arms

# Key dimensions
large_bushing_od = 18
large_bushing_id = 10
large_bushing_len = 22

small_bushing_od = 12
small_bushing_id = 6
small_bushing_len = 16

arm_width = 8
arm_height = 6

# Positions
# Large bushing at origin (left)
large_pos = (0, 0, 0)

# Two small bushings at right
small_pos_top = (70, 15, 0)
small_pos_bot = (50, -25, 0)

def make_arm_between(p1, p2, width, height):
    """Create a rectangular arm between two points in XY plane"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.degrees(math.atan2(dy, dx))
    
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2
    
    arm = (cq.Workplane("XY")
           .center(mid_x, mid_y)
           .rect(length, height)
           .extrude(width)
           .translate((0, 0, -width/2))
    )
    
    arm = arm.rotate((mid_x, mid_y, 0), (mid_x, mid_y, 1), angle)
    return arm

# Build the large bushing
large_bushing = (cq.Workplane("XY")
    .cylinder(large_bushing_len, large_bushing_od/2)
    .faces(">Z").workplane()
    .circle(large_bushing_id/2)
    .cutThruAll()
)
large_bushing = large_bushing.translate((0, 0, 0))

# Build small bushing 1 (top right)
small_bushing1 = (cq.Workplane("XY")
    .cylinder(small_bushing_len, small_bushing_od/2)
    .faces(">Z").workplane()
    .circle(small_bushing_id/2)
    .cutThruAll()
)
small_bushing1 = small_bushing1.translate((small_pos_top[0], small_pos_top[1], 0))

# Build small bushing 2 (bottom right)
small_bushing2 = (cq.Workplane("XY")
    .cylinder(small_bushing_len, small_bushing_od/2)
    .faces(">Z").workplane()
    .circle(small_bushing_id/2)
    .cutThruAll()
)
small_bushing2 = small_bushing2.translate((small_pos_bot[0], small_pos_bot[1], 0))

# Create arm segments as boxes, then rotate/position them
def make_box_arm(p1x, p1y, p2x, p2y, w, h):
    dx = p2x - p1x
    dy = p2y - p1y
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.degrees(math.atan2(dy, dx))
    mid_x = (p1x + p2x) / 2
    mid_y = (p1y + p2y) / 2
    
    arm = (cq.Workplane("XY")
           .box(length, h, w)
           .rotate((0, 0, 0), (0, 0, 1), angle)
           .translate((mid_x, mid_y, 0))
    )
    return arm

# Arm from large bushing to small bushing 1 (top)
arm1 = make_box_arm(large_bushing_od/2 * 0.7, 0,
                    small_pos_top[0] - small_bushing_od/2 * 0.5, small_pos_top[1],
                    small_bushing_len, arm_height)

# Arm from large bushing to small bushing 2 (bottom)
arm2 = make_box_arm(large_bushing_od/2 * 0.7, 0,
                    small_pos_bot[0] - small_bushing_od/2 * 0.3, small_pos_bot[1],
                    small_bushing_len, arm_height)

# Cross brace between small bushing 1 and small bushing 2
brace = make_box_arm(small_pos_top[0], small_pos_top[1],
                     small_pos_bot[0], small_pos_bot[1],
                     small_bushing_len * 0.6, arm_height * 0.7)

# Combine all parts
result = (large_bushing
          .union(small_bushing1)
          .union(small_bushing2)
          .union(arm1)
          .union(arm2)
          .union(brace)
)