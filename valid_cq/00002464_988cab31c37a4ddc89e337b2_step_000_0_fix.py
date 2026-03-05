import cadquery as cq

# Dimensions
width = 80   # X direction
depth = 60   # Y direction
height = 60  # Z direction

arch_radius = 35
arch_center_x = width  # arch centered at right side
arch_center_z = 0      # arch starts from bottom

# Build the main block
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
)

# Cut a large arch (quarter circle) from the front face
# The arch cuts from the right side - a quarter circle removing material
# Looking at image: left side is solid block, right side has arch cutout
# Arch: concave quarter circle cut from bottom-right area

# The arch cut: cylinder oriented along Y axis, positioned at top-left of the right face
arch_cut = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(width/2, 0, height))
    .circle(arch_radius + 5)
    .extrude(depth + 10)
)

# Better approach: build the profile and extrude
# Profile in XZ plane:
# - Left side: full rectangle
# - Right side: arch carved out (quarter circle)

# Create the 2D profile in XZ plane (front face)
# The shape: rectangle with quarter-circle cut from bottom-right

import cadquery as cq
import math

w = 80.0
d = 60.0
h = 60.0
r = 42.0  # arch radius

# Build profile in XZ plane
# Points going around the outer shape, then cut the arch
# The arch: center at (w, 0, 0), radius r, quarter circle from (w-r, 0) to (w, r)... 
# Actually from image: arch center is at bottom-right, cuts into the body

# Profile: start at origin, go around
# Bottom: (0,0) -> (w,0)
# Right side up to arch: (w,0) -> (w, h-r) ... no
# Looking at image more carefully:
# - Full left wall (rectangle left portion)
# - Arch opening on the right/front, quarter circle
# - Small tab at bottom front

# Let me use a simpler approach: box minus cylinder

# Main body
body = cq.Workplane("XY").box(w, d, h, centered=(False, True, False))

# Arch cut: quarter cylinder removed from the right-front
# Cylinder along Y axis at position (w, ?, 0), radius r
arch_cyl = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(w, 0, 0))
    .circle(r)
    .extrude(d + 20)
    .translate((0, -(d/2 + 10), 0))
)

result = body.cut(arch_cyl)

# Add a small tab/foot at the bottom front
tab = cq.Workplane("XY").box(w, 10, 8, centered=(False, False, False)).translate((0, d/2, -8))
result = result.union(tab)

# Small notch at top of arch
notch = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(w - r, 0, h - 5))
    .circle(4)
    .extrude(10)
)
result = result.cut(notch)

# Clean up - rebuild properly
result = (
    cq.Workplane("XY")
    .box(w, d, h, centered=(False, True, False))
)

# Cut the arch (quarter circle) - cylinder along Y, centered at (w, 0, 0)
arch_cyl = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, 0, 0))
    .circle(r)
    .extrude(w + 10)
    .translate((-5, 0, 0))
)

result = result.cut(arch_cyl)

# Keep only the part where x >= 0 and z >= 0 (the arch makes a concave corner)
keep_box = cq.Workplane("XY").box(w + 20, d + 20, h + 20, centered=(False, True, False)).translate((-10, 0, -10))
result = result.intersect(keep_box)

# Add bottom tab
tab = (
    cq.Workplane("XY")
    .box(w, 12, 6, centered=(False, True, False))
    .translate((0, 0, -6))
)
result = result.union(tab)