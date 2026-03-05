import cadquery as cq
import math

# Parameters
pitch = 8.0
width = 16.0
thickness = 2.0
large_hole_radius = 2.5
small_hole_radius = 1.0
ring_radius = 5.0
num_pitches = 16

slot_length = num_pitches * pitch

# Create the base plate (capsule shape)
result = cq.Workplane("XY").slot2D(slot_length, width).extrude(thickness)

# Lists to hold hole coordinates
ring_centers = []
large_centers = []
small_centers = []

# Distribute hole centers along the length
for i in range(17):
    x = (i - 8) * pitch
    if i % 4 == 0:
        ring_centers.append((x, 0))
    elif i % 2 == 1:
        small_centers.append((x, 0))
    elif i % 4 == 2:
        large_centers.append((x, 0))

# Cut central large holes for both rings and plain large centers
all_large_centers = ring_centers + large_centers
result = result.pushPoints(all_large_centers).circle(large_hole_radius).cutThruAll()

# Cut plain small holes on the centerline
result = result.pushPoints(small_centers).circle(small_hole_radius).cutThruAll()

# Generate and cut the small holes forming the rings around specific large holes
ring_holes = []
for cx, cy in ring_centers:
    for j in range(8):
        angle = j * math.pi / 4
        rx = cx + ring_radius * math.cos(angle)
        ry = cy + ring_radius * math.sin(angle)
        ring_holes.append((rx, ry))

result = result.pushPoints(ring_holes).circle(small_hole_radius).cutThruAll()