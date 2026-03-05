import cadquery as cq
import math

# Parameters
frame_size = 80  # overall frame size
bar_radius = 4   # radius of the bars
post_radius = 5  # radius of the corner posts
post_height = 40 # height of corner posts
frame_height = 8 # height of the horizontal frame bars

# The frame is a square/hexagonal looking frame - appears to be a square frame
# with corner posts at 4 corners
# Looking at the image: it's a square frame (4 sides) with 4 corner posts

half = frame_size / 2

# Corner positions (square frame)
corners = [
    (-half, -half),
    ( half, -half),
    ( half,  half),
    (-half,  half),
]

result = cq.Workplane("XY")

# Build the horizontal frame bars (rectangular cross-section tubes forming a square)
# Each bar connects adjacent corners

def make_bar(x1, y1, x2, y2, radius, height):
    """Create a cylindrical bar between two points at a given height"""
    length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    angle = math.degrees(math.atan2(y2-y1, x2-x1))
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    
    bar = (cq.Workplane("XY")
           .transformed(offset=(mx, my, height), rotate=(0, 0, angle))
           .cylinder(length, radius, centered=(True, True, True))
    )
    return bar

# Create frame assembly
frame = None

# Horizontal bars along the frame at z = frame_height/2
bar_z = frame_height / 2

# 4 sides of the square frame
sides = [
    (corners[0], corners[1]),
    (corners[1], corners[2]),
    (corners[2], corners[3]),
    (corners[3], corners[0]),
]

for (x1, y1), (x2, y2) in sides:
    bar = make_bar(x1, y1, x2, y2, bar_radius, bar_z)
    if frame is None:
        frame = bar
    else:
        frame = frame.union(bar)

# Corner posts (cylinders going up from z=0)
for (cx, cy) in corners:
    post = (cq.Workplane("XY")
            .transformed(offset=(cx, cy, 0))
            .cylinder(post_height, post_radius, centered=(True, True, False))
    )
    frame = frame.union(post)

# Add small spheres/fillets at corners to smooth connections
for (cx, cy) in corners:
    sphere = (cq.Workplane("XY")
              .transformed(offset=(cx, cy, bar_z))
              .sphere(max(bar_radius, post_radius) * 0.99)
    )
    frame = frame.union(sphere)

result = frame