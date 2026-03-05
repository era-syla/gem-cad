import cadquery as cq

# --- Parametric Variables ---
# Plate dimensions
plate_width = 100.0   # Width of the square plate
plate_thickness = 5.0 # Thickness of the plate
corner_radius = 10.0  # Radius of the rounded corners

# Hole dimensions
large_hole_diameter = 8.0
medium_hole_diameter = 6.0
small_hole_diameter = 4.0

# Hole pattern parameters (distances from center)
# Outer set of 4 large holes
outer_hole_spacing = 70.0 # Distance between centers of outer holes (square pattern side)

# Middle set of 4 medium holes
middle_hole_spacing = 45.0 # Distance between centers of middle holes

# Inner cross pattern
# Based on the image, there's a center hole, and 4 holes tightly around it
inner_cross_spacing = 15.0 # Radial distance from center or spacing for the cross

# --- 3D Modeling ---

# 1. Base Plate
# Create a square plate centered at origin
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_width, plate_thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius) # Round the corners
)

# 2. Hole Definitions

# Center Hole
result = base.faces(">Z").workplane().hole(small_hole_diameter)

# Inner "Cross" Pattern (4 small holes closest to center)
# These appear to be arranged in a small square or diamond around the center.
# Let's assume a square pattern rotated or just a square pattern.
# Looking closely, they align with the diagonals of the larger patterns.
inner_locs = [
    (inner_cross_spacing/2.0, inner_cross_spacing/2.0),
    (inner_cross_spacing/2.0, -inner_cross_spacing/2.0),
    (-inner_cross_spacing/2.0, inner_cross_spacing/2.0),
    (-inner_cross_spacing/2.0, -inner_cross_spacing/2.0)
]
result = result.faces(">Z").workplane().pushPoints(inner_locs).hole(small_hole_diameter)


# Middle Pattern (4 medium holes)
# These are the ones midway between center and corners
middle_locs = [
    (middle_hole_spacing/2.0, middle_hole_spacing/2.0),
    (middle_hole_spacing/2.0, -middle_hole_spacing/2.0),
    (-middle_hole_spacing/2.0, middle_hole_spacing/2.0),
    (-middle_hole_spacing/2.0, -middle_hole_spacing/2.0)
]
result = result.faces(">Z").workplane().pushPoints(middle_locs).hole(medium_hole_diameter)


# Outer Pattern (4 large holes near the corners)
outer_locs = [
    (outer_hole_spacing/2.0, 0),
    (-outer_hole_spacing/2.0, 0),
    (0, outer_hole_spacing/2.0),
    (0, -outer_hole_spacing/2.0)
]
# Wait, looking at the image again, the outer holes are not at the corners of a square.
# There seem to be holes aligned on the axes and holes aligned on the diagonals.
# Let's re-evaluate the pattern based on visual inspection.

# Re-analysis of the image pattern:
# 1. Center hole.
# 2. Four holes forming a small square rotated 45 degrees (diamond) or just a small square.
#    Let's look at alignment. They seem aligned diagonally.
# 3. Four holes further out, also aligned diagonally.
# 4. Four LARGE holes aligned on the X and Y axes.

# Let's refactor the hole creation based on this alignment:

# A. Center Hole
result = base.faces(">Z").workplane().hole(small_hole_diameter)

# B. Diagonal Holes (Inner Ring) - Small
inner_diag_offset = 12.0 # Distance from center for inner diagonal holes
inner_diag_locs = [
    (inner_diag_offset, inner_diag_offset),
    (inner_diag_offset, -inner_diag_offset),
    (-inner_diag_offset, inner_diag_offset),
    (-inner_diag_offset, -inner_diag_offset)
]
result = result.faces(">Z").workplane().pushPoints(inner_diag_locs).hole(small_hole_diameter)

# C. Diagonal Holes (Outer Ring) - Medium
outer_diag_offset = 25.0 
outer_diag_locs = [
    (outer_diag_offset, outer_diag_offset),
    (outer_diag_offset, -outer_diag_offset),
    (-outer_diag_offset, outer_diag_offset),
    (-outer_diag_offset, -outer_diag_offset)
]
result = result.faces(">Z").workplane().pushPoints(outer_diag_locs).hole(medium_hole_diameter)

# D. Axis Holes (The largest ones) - Large
# Located on X and Y axes
axis_offset = 30.0
axis_locs = [
    (axis_offset, 0),
    (-axis_offset, 0),
    (0, axis_offset),
    (0, -axis_offset)
]
result = result.faces(">Z").workplane().pushPoints(axis_locs).hole(large_hole_diameter)