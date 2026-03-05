import cadquery as cq
import math

# Parameters
thickness = 3  # height of the flat part
width = 6      # width of the flat strips

# The shape looks like a Y/fork:
# - A handle (straight bar) going to lower-left
# - Two tines: one going left, one curving up into a U shape (open circle arc)

# Let's build this as a 2D profile then extrude

# The shape in 2D:
# Handle: long bar going diagonally (we'll lay it flat along X axis then rotate)
# Fork: splits into left tine and a U-shaped arc on the right

# Build as a 2D wire profile

handle_length = 80
tine_length = 40
arc_radius = 25
fork_width = width  # width of each arm

# Let's define the 2D outline of the whole shape
# Place handle along -X direction, fork splitting toward +X
# Left tine goes up-left, right tine curves into a U (open arc)

# Strategy: build the closed 2D profile using lines and arcs

# Center of the arc (U shape) will be at some point
# Let's think in 2D:
# Handle runs from left along X axis
# At origin, it splits: one arm goes upper-left at angle, 
# another arm curves into a semicircle (open at bottom)

# Simplified layout:
# - Handle: from (-handle_length, -fork_width/2) to (0, -fork_width/2)
#            and  (-handle_length, fork_width/2) to (0, fork_width/2)
# - Left tine: from (0, fork_width/2) going up-left
# - Right tine: curves into U arc

# Let's use a different approach - build 3 separate solid bars and union them

# Handle bar
handle = (
    cq.Workplane("XY")
    .box(handle_length, fork_width, thickness)
    .translate((-handle_length/2, 0, 0))
)

# Left tine - angled bar going upper-left from near origin
tine_angle = 45  # degrees upward from horizontal
tine_len = 50

left_tine = (
    cq.Workplane("XY")
    .box(tine_len, fork_width, thickness)
)
# Rotate and translate
left_tine = left_tine.rotate((0,0,0),(0,0,1), tine_angle)
left_tine = left_tine.translate((tine_len/2 * math.cos(math.radians(tine_angle+180)),
                                  tine_len/2 * math.sin(math.radians(tine_angle+180)),
                                  0))

# U-shaped arc tine - a curved strip going up and around
arc_r_outer = arc_radius + fork_width/2
arc_r_inner = arc_radius - fork_width/2
arc_center_x = 20
arc_center_y = 20

arc_piece = (
    cq.Workplane("XY")
    .workplane()
    .transformed(offset=(arc_center_x, arc_center_y, 0))
    .circle(arc_r_outer)
    .circle(arc_r_inner)
    .extrude(thickness)
)

# Cut the arc piece to only keep the upper portion (a C-shape open at bottom)
cut_box = (
    cq.Workplane("XY")
    .box(arc_r_outer*2 + 20, arc_r_outer + 20, thickness + 2)
    .translate((arc_center_x, arc_center_y - arc_r_outer/2 - 10, 0))
)

arc_piece = arc_piece.cut(cut_box)

# Now combine: handle + junction + arc piece + left tine
# Junction block to connect them
junction = (
    cq.Workplane("XY")
    .box(fork_width * 3, fork_width * 3, thickness)
    .translate((fork_width, fork_width/2, 0))
)

# Combine all
result = (
    handle
    .union(left_tine)
    .union(arc_piece)
    .union(junction)
)

# Clean up with small fillet on top/bottom edges
try:
    result = result.edges("|Z").fillet(1.0)
except:
    pass