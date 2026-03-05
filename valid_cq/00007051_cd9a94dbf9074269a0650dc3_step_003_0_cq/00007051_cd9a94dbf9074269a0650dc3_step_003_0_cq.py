import cadquery as cq

# --- Parameter Definitions ---

# Shared parameters (assumed thickness)
thickness = 2.0

# Part 1: Servo Horn / Bracket (Left part)
# Main body dimensions
horn_width_top = 20.0     # Width of the wider section at the top
horn_width_bottom = 10.0  # Width of the rounded bottom
horn_length = 40.0        # Total vertical length
tab_width = 8.0           # Width of the top tab
tab_height = 5.0          # Height of the top tab
shoulder_height = 10.0    # Height of the straight section before tapering

# Hole parameters
hole_diameter = 2.5
hole_spacing = 5.0
bottom_radius = horn_width_bottom / 2.0

# Part 2: Slotted Plate (Right part)
plate_length = 30.0
plate_width = 25.0
slot_length = 15.0
slot_width = 2.0

# --- Geometry Construction ---

# 1. Create the Left Part (Servo Horn/Bracket)
# We will define points for a polygon and extrude it.
# The shape is roughly symmetric, but drawing the full outline is easier.

# Define coordinates relative to a center or bottom point.
# Let's place the center of the bottom arc at (0,0) for easier hole placement.

pts = [
    (-tab_width/2, horn_length),                 # Top-left of tab
    (tab_width/2, horn_length),                  # Top-right of tab
    (tab_width/2, horn_length - tab_height),     # Bottom-right of tab
    (horn_width_top/2, horn_length - tab_height),# Top-right shoulder
    (horn_width_top/2, horn_length - tab_height - shoulder_height), # Bottom-right shoulder start
    (horn_width_bottom/2, 0),                    # Bottom-right before arc
    (-horn_width_bottom/2, 0),                   # Bottom-left before arc
    (-horn_width_top/2, horn_length - tab_height - shoulder_height), # Bottom-left shoulder start
    (-horn_width_top/2, horn_length - tab_height),# Top-left shoulder
    (-tab_width/2, horn_length - tab_height)     # Bottom-left of tab
]

horn_body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Add the rounded bottom
# We select the bottom face (at Z=0 roughly) or draw a circle and fuse
bottom_arc = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .circle(bottom_radius)
    .extrude(thickness)
    # Cut the top half of the circle so it doesn't overlap weirdly inside, 
    # though union handles overlaps fine. Just unioning a cylinder is easiest.
)

# Combine body and bottom arc
part1 = horn_body.union(bottom_arc)

# Cut the holes
# Holes are arranged vertically starting from near the bottom center
part1 = (
    part1.faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (0, hole_spacing), (0, hole_spacing * 2)])
    .hole(hole_diameter)
)

# 2. Create the Right Part (Slotted Plate)
# We'll position this offset from the first part so they appear side-by-side as in the image.

offset_x = 40.0
offset_y = 25.0

part2 = (
    cq.Workplane("XY")
    .center(offset_x, offset_y)
    .box(plate_length, plate_width, thickness)
    .faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width, angle=90) # 90 degrees to align slot vertically relative to plate
    .cutThruAll()
)

# --- Final Assembly ---

# Combine both parts into a single result object for visualization
result = part1.union(part2)