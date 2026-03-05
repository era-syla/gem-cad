import cadquery as cq
import math

# Parameters
radius = 80
thickness = 5
slot_radius = 60  # radius of the arc slot
slot_width = 3
slot_depth = 2
hole_radius = 3
hole_distance = 55  # distance from center

# Create quarter circle base
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(radius, 0)
    .radiusArc((0, radius), -radius)
    .lineTo(0, 0)
    .close()
    .extrude(thickness)
)

# Add chamfer/fillet to top edges
result = result.faces(">Z").edges().chamfer(0.8)

# Cut arc slot on top face
# The slot is an arc at radius ~60, spanning roughly 45 degrees to 80 degrees from x-axis
# We'll create the slot by sweeping a small rectangle along an arc path

# Create arc slot using a series of cuts approximated by sweeping
# Build the slot as a swept profile along an arc

# Define the arc path for the slot
slot_inner = slot_radius - slot_width / 2
slot_outer = slot_radius + slot_width / 2
start_angle = 20
end_angle = 75

# Create slot by making an arc-shaped pocket
# Use a 2D approach: create annular sector and extrude/cut
def make_arc_sector(r_inner, r_outer, ang_start, ang_end):
    pts = []
    n = 20
    for i in range(n + 1):
        ang = math.radians(ang_start + (ang_end - ang_start) * i / n)
        pts.append((r_outer * math.cos(ang), r_outer * math.sin(ang)))
    for i in range(n + 1):
        ang = math.radians(ang_end - (ang_end - ang_start) * i / n)
        pts.append((r_inner * math.cos(ang), r_inner * math.sin(ang)))
    pts.append(pts[0])
    return pts

slot_pts = make_arc_sector(slot_inner, slot_outer, start_angle, end_angle)

slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=thickness - slot_depth)
    .polyline(slot_pts)
    .close()
    .extrude(slot_depth)
)

result = result.cut(slot_cut)

# Cut mounting hole
hole_angle = math.radians(45)
hole_x = hole_distance * math.cos(math.radians(-15))
hole_y = hole_distance * math.sin(math.radians(-15))

# Place hole closer to the straight edges, near bottom right area
hole_x = 50
hole_y = 18

hole_cut = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(hole_x, hole_y)
    .circle(hole_radius)
    .extrude(thickness)
)

result = result.cut(hole_cut)