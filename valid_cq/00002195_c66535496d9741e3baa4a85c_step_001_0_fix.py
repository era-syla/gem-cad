import cadquery as cq

# Parameters
outer_radius = 20
inner_radius = 14
height = 12
tab_width = 12
tab_length = 14
tab_height = 12
bolt_hole_size = 5
chamfer_size = 1.0

# Create the main half-cylinder clamp body
# The clamp is a half-circle (semicircle) shape with flat tabs on each end

# Build the 2D profile for the clamp body
# Semicircle arc from 0 to 180 degrees with tabs extending on each side

import math

# Create the outer profile as a closed wire
# The shape: two rectangular tabs connected by a semicircular arc

# Tab positions: tabs extend from the ends of the semicircle (at y=0 plane)
# Left tab center at (-outer_radius - tab_length/2, 0)
# Right tab center at (outer_radius + tab_length/2, 0)

# Build the profile using polyline + arc
# Points for the outer profile (looking from front, semicircle opens downward/front)

# The flat base is at y=0, semicircle curves upward
# Left tab outer edge x = -(outer_radius + tab_length)
# Right tab outer edge x = (outer_radius + tab_length)

left_outer_x = -(outer_radius + tab_length)
right_outer_x = (outer_radius + tab_length)
tab_half = tab_width / 2

# Create outer body profile
outer_pts = [
    (left_outer_x, -tab_half),
    (left_outer_x, tab_half),
    (-outer_radius, tab_half),
]

inner_pts_left = [
    (-outer_radius, -tab_half),
]

# We'll build this by creating the solid via extrusion then cutting

# Step 1: Create left tab
left_tab = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_height, centered=True)
    .translate((-outer_radius - tab_length/2, 0, tab_height/2))
)

# Step 2: Create right tab
right_tab = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_height, centered=True)
    .translate((outer_radius + tab_length/2, 0, tab_height/2))
)

# Step 3: Create the semi-cylindrical shell (half annulus)
# Full annulus extruded then cut in half
full_annulus = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Cut bottom half (y < 0)
cut_box = (
    cq.Workplane("XY")
    .box(outer_radius * 2 + 10, outer_radius + 5, height + 2, centered=True)
    .translate((0, -(outer_radius + 5)/2 - 0, height/2))
)

# Actually cut y < 0 half
cut_bottom = (
    cq.Workplane("XY")
    .box((outer_radius + 5) * 2, outer_radius + 5, height + 4, centered=True)
    .translate((0, -(outer_radius + 5)/2, height/2))
)

semi_shell = full_annulus.cut(cut_bottom)

# Step 4: Combine all parts
result = (
    left_tab
    .union(right_tab)
    .union(semi_shell)
)

# Step 5: Add bolt holes to tabs (square/hex holes visible in image - use square holes)
hole_depth = tab_height + 2

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-(outer_radius + tab_length/2), 0)
    .rect(bolt_hole_size, bolt_hole_size)
    .cutBlind(-hole_depth)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .center((outer_radius + tab_length/2), 0)
    .rect(bolt_hole_size, bolt_hole_size)
    .cutBlind(-hole_depth)
)

# Step 6: Apply chamfers to top edges of tabs
result = (
    result
    .edges("|Z")
    .chamfer(chamfer_size)
)