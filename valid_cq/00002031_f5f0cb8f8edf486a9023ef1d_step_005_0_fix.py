import cadquery as cq

# Servo arm / control horn shape
# Long flat plate with rounded ends, wider at one end, narrower at the other

length = 80.0
wide_end_width = 22.0
narrow_end_width = 12.0
thickness = 3.0

# Build the profile as a series of points
# Wide end (left) centered at x=0, narrow end (right) at x=length

half_wide = wide_end_width / 2.0
half_narrow = narrow_end_width / 2.0

# Create the base plate shape using a workplane and a closed wire
# We'll use a loft-like approach or just draw the outline

# Points for the arm profile (outline)
# Wide end: semi-circle at x=0 with radius half_wide
# Narrow end: semi-circle at x=length with radius half_narrow
# Straight edges connecting them

import cadquery as cq
import math

# Create the arm shape by extruding a 2D profile
# Use a path with lines and arcs

wide_r = wide_end_width / 2.0
narrow_r = narrow_end_width / 2.0

# Build profile using polyline + arcs approach
# Left end (wide) centered at (0,0), right end (narrow) at (length, 0)

result = (
    cq.Workplane("XY")
    .moveTo(0, -wide_r)
    .lineTo(length, -narrow_r)
    .threePointArc((length + narrow_r, 0), (length, narrow_r))
    .lineTo(0, wide_r)
    .threePointArc((-wide_r, 0), (0, -wide_r))
    .close()
    .extrude(thickness)
)

# Now add holes on the wide end
# Center hole
wide_center_x = 0
wide_center_y = 0

# Three holes at the wide end: center + two side holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .hole(4.0)
)

# Two smaller holes flanking the center on the wide end
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-6, 0), (6, 0)])
    .hole(2.5)
)

# Two holes on the narrow end
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(length - 8, -2), (length - 8, 2)])
    .hole(2.0)
)

# Add chamfer/fillet to top edges to give it a finished look
result = (
    result
    .edges("|Z")
    .fillet(1.0)
)