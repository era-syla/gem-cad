import cadquery as cq

# Parametric dimensions
base_length = 60.0
base_width = 20.0
base_thickness = 5.0
fillet_radius = 2.0

block_height = 25.0  # Total height from bottom
block_width = 15.0   # Width of the raised blocks (along base_length axis)
block_depth = 20.0   # Depth of the blocks (along base_width axis)
gap_width = 10.0     # Gap between the two blocks

hole_diameter = 4.5
c_sink_diameter = 8.0
c_sink_angle = 90.0

# 1. Create the base plate
# We start with a centered rectangle and extrude it
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. Add fillets to the four corners of the base
# Selecting vertical edges
base = base.edges("|Z").fillet(fillet_radius)

# 3. Create the two raised blocks
# There are several ways to do this. A simple way is to draw two rectangles 
# on the top face and extrude.
# The blocks are flush with the sides (Y) and separated by a gap in the middle (X).

# Calculate centers for the blocks
# The gap is centered. The blocks are on either side of X=0.
block_offset = (gap_width / 2.0) + (block_width / 2.0)

# Create the blocks
# We select the top face of the base to sketch on
blocks = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-block_offset, 0), (block_offset, 0)])
    .rect(block_width, block_depth)
    .extrude(block_height - base_thickness)
)

# 4. Create the countersunk holes
# The holes are located on the 'wings' of the base.
# Calculate hole position relative to the center
hole_dist_from_center = (base_length / 2.0) - (base_length - (gap_width + 2*block_width))/2.0 / 2.0 
# Actually, looking at the image, the holes are centered in the remaining space on the flanges.
flange_length = (base_length - (gap_width + 2 * block_width)) / 2.0
hole_x_pos = (base_length / 2.0) - (flange_length / 2.0) 
# Let's adjust this slightly to be more robust. The holes are on the ends.
# Let's place them centered on the "flange" area.
# Flange area starts at block edge: (gap_width/2 + block_width)
# Ends at base_length/2
start_flange = (gap_width / 2.0) + block_width
end_flange = base_length / 2.0
hole_center_x = (start_flange + end_flange) / 2.0

# Use cskHole for countersunk holes
result = (
    blocks.faces(">Z").workplane(offset=-(block_height - base_thickness)) # Go back to base top level
    .pushPoints([(-hole_center_x, 0), (hole_center_x, 0)])
    .cskHole(hole_diameter, c_sink_diameter, c_sink_angle)
)

# Return the final object
if 'show_object' in globals():
    show_object(result)