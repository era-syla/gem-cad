import cadquery as cq

# -- Parametric Dimensions --
plate_length = 150.0   # Total length along X-axis
plate_width_wide = 100.0  # Width at the wide end
plate_width_narrow = 60.0 # Width at the narrow end
thickness = 10.0      # Plate thickness

# Chamfer/Angled cut parameters
# The narrow end is simpler, just a straight edge.
# The wide end has angled cuts. Let's define the flat part of the wide end.
wide_flat_section = 60.0 
narrow_flat_section = 60.0

# Hole Parameters
center_hole_dia = 12.0
center_hole_countersink_dia = 20.0
center_hole_countersink_angle = 90.0

small_hole_dia = 6.0
small_hole_pattern_radius = 25.0
# There seem to be 3 small holes around the big one.
# Looking at the image, there's one central big hole.
# There are 3 smaller holes surrounding it in a triangular pattern.
# And one solitary hole near the wide end.

wide_end_hole_dia = 8.0
wide_end_hole_offset = 50.0 # Distance from center towards the wide end

# -- Geometry Construction --

# Define the points for the outer polygon profile
# Let's center the main large hole at (0,0) for easier hole placement.
# This means the plate extends in -X and +X directions.
# Based on the image, the narrow end is on the left (-X) and wide end on right (+X).

# Calculate coordinates based on assumptions from visual estimation:
# Let's assume the center hole is roughly at 1/3 of the length from the narrow end.
x_narrow = -40.0
x_wide = x_narrow + plate_length

# Points order: clockwise starting from top-left (narrow end)
# Top-Left
p1 = (x_narrow, plate_width_narrow / 2.0)
# Top-Right (start of angled cut)
p2 = (x_wide - (plate_width_wide - wide_flat_section)/2, plate_width_wide / 2.0) 
# Top-Right (end of angled cut / flat face) -> This seems wrong, the image shows a taper along the length.
# Let's re-evaluate the shape. It looks like a symmetric trapezoid with the corners cut off at the wide end?
# Actually, it looks like a simple symmetric shape where the sides taper from the wide end to the narrow end.
# But looking closer at the right side (wide end), the corners are clipped.
# Let's try this:
# 1. Start with the wide end flat face.
# 2. Go to the narrow end flat face.
# 3. The sides connect them.
# The image shows the wide end corners are chamfered/clipped.

# Revised Points Strategy:
# Center hole is at (0,0).
# Narrow end is at x = -40
# Wide end is at x = +80 (Total length approx 120)
dist_to_narrow = 50.0
dist_to_wide = 100.0

# Narrow end (Left)
p_narrow_top = (-dist_to_narrow, plate_width_narrow / 2)
p_narrow_bottom = (-dist_to_narrow, -plate_width_narrow / 2)

# Wide end (Right) - The wide end has a flat vertical segment and then tapers back.
# Actually, looking at the very right edge, it's a straight vertical line.
# Then there are angled lines going back to the main tapered sides. 
# Wait, no, it looks like a standard tapered plate (trapezoid) where the wide end's corners have been chamfered.
p_wide_flat_top = (dist_to_wide, wide_flat_section / 2)
p_wide_flat_bottom = (dist_to_wide, -wide_flat_section / 2)

# We need intermediate points where the main taper meets the corner chamfer
# Let's define the "uncut" width at the wide end.
full_wide_width = 120.0
# The corner chamfer starts at some X.
chamfer_x_start = dist_to_wide - 15.0

# Let's just define the polygon explicitly.
pts = [
    (-dist_to_narrow, plate_width_narrow/2),      # Top Left
    (dist_to_wide - 20, full_wide_width/2),       # Top Right (start of chamfer)
    (dist_to_wide, wide_flat_section/2),          # Top Right (end of chamfer)
    (dist_to_wide, -wide_flat_section/2),         # Bottom Right (start of chamfer)
    (dist_to_wide - 20, -full_wide_width/2),      # Bottom Right (end of chamfer)
    (-dist_to_narrow, -plate_width_narrow/2)      # Bottom Left
]

# Create the base solid
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# -- Add Holes --

# 1. Center Countersunk Hole
result = (result
          .faces(">Z")
          .workplane()
          .hole(center_hole_dia) # Simple through hole first
          .faces(">Z")
          .workplane()
          .cboreHole(center_hole_dia, center_hole_countersink_dia, center_hole_countersink_dia/2 * 0.5) # Approximating countersink as cbore or use specific chamfer later. 
          # Actually, CadQuery's cskHole is better for conical countersinks
         )
         
# Re-doing center hole with cskHole for proper conical shape
result = (cq.Workplane("XY").polyline(pts).close().extrude(thickness)
          .faces(">Z").workplane()
          .cskHole(center_hole_dia, center_hole_countersink_dia, 82) # Standard 82 deg or 90 deg
         )

# 2. Surrounding Small Holes (3 of them)
# Pattern seems to be: one left, one top-right, one bottom-right relative to center hole
# Or strictly triangular: 0, 120, 240 degrees?
# Visually:
# - One hole is towards the narrow end (left), on centerline.
# - Two holes are towards the wide end, symmetric.
# Let's estimate coordinates relative to center (0,0).

small_hole_offset_x_left = -25.0
small_hole_offset_x_right = 15.0
small_hole_offset_y = 20.0

small_holes_pts = [
    (small_hole_offset_x_left, 0),
    (small_hole_offset_x_right, small_hole_offset_y),
    (small_hole_offset_x_right, -small_hole_offset_y)
]

result = (result
          .faces(">Z").workplane()
          .pushPoints(small_holes_pts)
          .hole(small_hole_dia)
         )

# 3. Single Hole at Wide End
# Located on centerline near the right edge
wide_hole_pt = [(dist_to_wide - 25.0, 0)]

result = (result
          .faces(">Z").workplane()
          .pushPoints(wide_hole_pt)
          .hole(wide_end_hole_dia)
         )

# Optional: Fillets on the sharp vertical edges for a more realistic look
# The image shows fairly sharp edges, but engineering parts usually have small radii.
# We will leave them sharp as per the blocky render style, or add very slight fillets if requested.
# The user prompt just asks to create the model. The image is sharp.

# Final check of the variable name
# The requirements say "Create a variable called 'result' containing the final geometry"