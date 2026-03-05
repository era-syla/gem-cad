import cadquery as cq

# --- Parameter Definitions ---

# Block Part Parameters
block_length = 50.0
block_width = 30.0
block_height = 15.0

# Block Top Holes (Circular)
top_hole_dia = 4.0
top_hole_spacing = 20.0  # Center-to-center

# Block Side Holes (Hexagonal)
hex_flat_to_flat = 10.0
hex_hole_depth = 5.0  # Depth of hex pocket
# Inner hole for the hex pocket (usually for a screw shank)
hex_inner_hole_dia = 5.0 
side_hole_spacing = 30.0

# T-Bracket Parameters
t_main_length = 60.0
t_main_width = 10.0
t_main_height = 15.0
t_stem_length = 15.0  # Protrusion length from main bar
t_stem_width = 10.0  # Usually same thickness as main bar

# T-Bracket Holes
bracket_hole_dia = 5.0
bracket_cbore_dia = 9.0
bracket_cbore_depth = 3.0
bracket_end_hole_spacing = 40.0 # Distance between holes on main bar

# --- Part 1: Rectangular Block with Hex Recesses ---

# Create base block
block = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create top circular holes
# We select the top face, push points relative to center
top_holes = (
    block.faces(">Z").workplane()
    .pushPoints([(top_hole_spacing / 2, 0), (-top_hole_spacing / 2, 0)])
    .hole(top_hole_dia)
)

# Create side hexagonal recesses (sockets) and through holes
# We assume the hex shapes are on the "front" face (>Y or <Y depending on orientation, let's use >Y)
# The image shows them on the long face.

# Helper to make a hex cut
def make_hex_cut(part, x_pos):
    # Create the hexagonal pocket
    part = (
        part.faces(">Y").workplane(centerOption="CenterOfBoundBox")
        .center(x_pos, 0)
        .polygon(6, hex_flat_to_flat / (2 * 0.866025) * 2) # circumradius calculation
        .cutBlind(-hex_hole_depth)
    )
    # Create the through hole inside the pocket
    part = (
        part.faces(">Y").workplane(centerOption="CenterOfBoundBox")
        .center(x_pos, 0)
        .hole(hex_inner_hole_dia)
    )
    return part

block_with_holes = make_hex_cut(top_holes, side_hole_spacing / 2)
block_with_holes = make_hex_cut(block_with_holes, -side_hole_spacing / 2)


# --- Part 2: T-Shaped Bracket ---

# Create the main bar
main_bar = cq.Workplane("XY").box(t_main_length, t_main_width, t_main_height)

# Create the stem (the 'T' part)
# Positioned at the center, protruding in -Y
stem = (
    cq.Workplane("XY")
    .center(0, -(t_main_width/2 + t_stem_length/2))
    .box(t_stem_width, t_stem_length, t_main_height)
)

# Fuse them together
t_bracket_body = main_bar.union(stem)

# Add holes to the main bar (Counterbored)
t_bracket_holes = (
    t_bracket_body.faces(">Y").workplane()
    .pushPoints([(bracket_end_hole_spacing / 2, 0), (-bracket_end_hole_spacing / 2, 0)])
    .cboreHole(bracket_hole_dia, bracket_cbore_dia, bracket_cbore_depth)
)

# Add hole to the stem (Simple hole through the side)
# Looking at the image, there is a hole going through the stem part in the X direction
t_bracket_final = (
    t_bracket_holes.faces(">X").workplane(centerOption="CenterOfBoundBox")
    # Need to target the stem area specifically or use absolute coordinates.
    # The stem is at Y negative.
    .moveTo(0, -(t_main_width/2 + t_stem_length/2)) 
    .hole(bracket_hole_dia)
)

# --- Assembly / Final Layout ---

# Move the T-bracket so it's visible next to the block, similar to image
t_bracket_moved = t_bracket_final.translate((60, -30, 0))

# Combine for result
result = block_with_holes.union(t_bracket_moved)