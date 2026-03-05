import cadquery as cq

# ==========================================
# Parameters
# ==========================================
# Overall Dimensions
side_width = 30.0       # Outer width of the square profile
fillet_r = 3.0          # External corner fillet radius
hex_flat_dist = 18.0    # Internal hexagon size (flat-to-flat)

# Segment Dimensions
block_h = 15.0          # Height of the solid corner blocks
gap_h = 20.0            # Height of the recessed "waist" sections
# Calculate total height for a stack of: Block - Gap - Block - Gap - Block
total_height = 3 * block_h + 2 * gap_h

# Feature Dimensions
recess_cut_size = 6.0   # Size of the square cutout removed from corners
hole_diam = 2.5         # Diameter of the corner mounting holes

# Derived Parameters
# 1. Center offset for the corner cut rectangles:
#    We remove a square of 'recess_cut_size' from the corner.
#    The corner of the base square is at 'side_width/2'.
#    The center of the cut square is shifted inward by half its size.
cut_center_dist = (side_width / 2.0) - (recess_cut_size / 2.0)

# 2. Hole location:
#    Placed concentrically with the corner fillet.
hole_center_dist = (side_width / 2.0) - fillet_r

# 3. Hexagon Diameter:
#    CadQuery polygon uses circumradius/diameter.
#    d_circum = d_flat * 2 / sqrt(3)
hex_diam = 2 * (hex_flat_dist / 1.7320508)

# ==========================================
# Modeling
# ==========================================

# 1. Create Base Body
#    A square prism centered in X/Y, sitting on Z=0
result = (
    cq.Workplane("XY")
    .box(side_width, side_width, total_height, centered=(True, True, False))
    .edges("|Z")
    .fillet(fillet_r)
)

# 2. Cut Internal Hexagonal Bore
result = (
    result.faces(">Z")
    .polygon(6, hex_diam)
    .cutThruAll()
)

# 3. Cut Corner Recesses
#    Define the four corner points for the cuts
corner_points = [
    (cut_center_dist, cut_center_dist),
    (cut_center_dist, -cut_center_dist),
    (-cut_center_dist, cut_center_dist),
    (-cut_center_dist, -cut_center_dist)
]

#    Define Z-heights where the gaps start
#    Gap 1 starts after the first block
#    Gap 2 starts after the first block + gap + middle block
gap_starts = [block_h, 2 * block_h + gap_h]

for z_start in gap_starts:
    result = (
        result
        .workplane(origin=(0, 0, z_start)) # Create plane at start of gap
        .pushPoints(corner_points)         # Target the 4 corners
        .rect(recess_cut_size, recess_cut_size)
        .extrude(gap_h, combine='cut')     # Cut upwards for gap height
    )

# 4. Drill Corner Holes
#    These run through the entire height of the corner blocks
hole_points = [
    (hole_center_dist, hole_center_dist),
    (hole_center_dist, -hole_center_dist),
    (-hole_center_dist, hole_center_dist),
    (-hole_center_dist, -hole_center_dist)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diam)
)