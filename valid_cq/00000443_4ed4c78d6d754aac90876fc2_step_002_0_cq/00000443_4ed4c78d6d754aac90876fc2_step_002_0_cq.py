import cadquery as cq

# --- Parametric Dimensions ---
# Base plate dimensions
base_length = 200.0
base_width = 100.0
base_thickness = 15.0

# Raised pad dimensions
pad_offset = 10.0  # Distance from the edge of the base to the pad
pad_length = base_length - (2 * pad_offset)
pad_width = base_width - (2 * pad_offset)
pad_height = 2.0

# Mounting holes (perimeter)
hole_diameter = 4.0
hole_spacing_offset = 5.0 # Distance from edge to hole center
long_edge_count = 10 # Number of holes along the long edge
short_edge_count = 5  # Number of holes along the short edge

# Counterbored holes (corners of the pad)
cb_hole_dia = 6.0
cb_head_dia = 10.0
cb_head_depth = 5.0

# --- Modeling ---

# 1. Create the base block
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. Create the raised pad on top
# We select the top face, work on it, and create the pad
result = (result.faces(">Z").workplane()
          .rect(pad_length, pad_width)
          .extrude(pad_height))

# 3. Create the perimeter mounting holes
# We need to calculate the positions.
# Let's create a list of points for the holes.
hole_x_max = (base_length / 2) - hole_spacing_offset
hole_y_max = (base_width / 2) - hole_spacing_offset

# Points along the long edges (top and bottom in 2D view)
# We distribute points linearly
pts = []

# Long edges
x_step = (2 * hole_x_max) / (long_edge_count - 1)
for i in range(long_edge_count):
    x_pos = -hole_x_max + (i * x_step)
    pts.append((x_pos, hole_y_max))
    pts.append((x_pos, -hole_y_max))

# Short edges (excluding corners which are already covered by the long edge loop if we aren't careful, 
# but typically these patterns share corner holes. Let's fill the gaps between corners).
# Using short_edge_count includes corners, so let's calculate intermediate points.
y_step = (2 * hole_y_max) / (short_edge_count - 1)
for i in range(1, short_edge_count - 1): # Skip 0 and last index to avoid double corners
    y_pos = -hole_y_max + (i * y_step)
    pts.append((hole_x_max, y_pos))
    pts.append((-hole_x_max, y_pos))

# Drill the small perimeter holes
result = (result.faces(">Z").workplane()
          .pushPoints(pts)
          .hole(hole_diameter))

# 4. Create the larger counterbored holes
# These appear to be located at the corners of the raised pad, cutting into the pad and base.
# They look slightly inset into the pad corners.
cb_x_offset = (pad_length / 2) 
cb_y_offset = (pad_width / 2) 

# Adjust position slightly so they cut the corner of the pad nicely as shown in image
# Looking at the image, they are 'notches' or circular cutouts centered on the corner of the pad.
cb_points = [
    (cb_x_offset, cb_y_offset),
    (cb_x_offset, -cb_y_offset),
    (-cb_x_offset, cb_y_offset),
    (-cb_x_offset, -cb_y_offset)
]

result = (result.faces(">Z").workplane()
          .pushPoints(cb_points)
          .cboreHole(cb_hole_dia, cb_head_dia, cb_head_depth))

# Return the final object
if 'show_object' in locals():
    show_object(result)