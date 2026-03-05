import cadquery as cq

# --- Parameters ---
# Bar dimensions
bar_width = 10.0
bar_thickness = 10.0

# Lengths of the individual links (approximate based on visual proportions)
link_long_len = 150.0  # The long, angled bar on the left
link_mid_len = 100.0   # The vertical-ish bar on the right
link_cross_bottom_len = 60.0 # The bottom connecting bar
link_cross_top_len = 40.0    # The top connecting bar

# Pivot hole parameters
hole_diameter = 4.0

# Angles (approximate to achieve the shape)
angle_long = 110.0  # Angle of the long bar relative to horizontal
angle_mid = 80.0    # Angle of the mid bar
angle_cross = 0.0   # Horizontal bars

# --- Geometry Construction ---

def create_bar(length, w, t, hole_d):
    """Creates a basic rectangular bar with holes at both ends."""
    bar = (
        cq.Workplane("XY")
        .box(length, w, t)
        .faces(">Z")
        .workplane()
        .pushPoints([(-length/2 + w/2, 0), (length/2 - w/2, 0)])
        .hole(hole_d)
    )
    return bar

# 1. Create the four individual links
# We create them centered at origin then rotate and move them into place.

# Left Long Bar
# It needs an extra hole in the middle for the top crossbar
bar_long = (
    cq.Workplane("XY")
    .box(link_long_len, bar_width, bar_thickness)
    .faces(">Z")
    .workplane()
    # Bottom hole, Top hole, Mid hole (approximate position)
    .pushPoints([
        (-link_long_len/2 + bar_width/2, 0), 
        (link_long_len/2 - bar_width/2, 0),
        (0, 0) # Middle hole
    ])
    .hole(hole_diameter)
)

# Right Mid Bar
# Needs bottom hole, top hole, and a hole lower down for the bottom crossbar?
# Looking closely, it seems to be: Top pivot, Mid pivot (for bottom crossbar), Bottom pivot (free end)
bar_mid = (
    cq.Workplane("XY")
    .box(link_mid_len, bar_width, bar_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (link_mid_len/2 - bar_width/2, 0),    # Top end
        (-link_mid_len/2 + bar_width/2, 0),   # Bottom end
        (0, 0)                                # Middle pivot
    ])
    .hole(hole_diameter)
)

# Bottom Cross Bar
bar_cross_bottom = create_bar(link_cross_bottom_len, bar_width, bar_thickness, hole_diameter)

# Top Cross Bar
bar_cross_top = create_bar(link_cross_top_len, bar_width, bar_thickness, hole_diameter)


# --- Assembly ---
# We will define positions relative to a global coordinate system to assemble the linkage.
# Let's fix the bottom-left pivot point (connection between Long Bar and Bottom Cross Bar) as (0,0,0)

# Position 1: Long Bar
# Pivot is at bottom end: (-link_long_len/2 + bar_width/2, 0) local
# Move local pivot to origin, then rotate
long_bar_placed = (
    bar_long
    .translate((link_long_len/2 - bar_width/2, 0, 0)) # Shift so bottom pivot is at origin
    .rotate((0,0,0), (0,0,1), angle_long)             # Rotate to stand up
)

# Position 2: Bottom Cross Bar
# Connects to Long Bar at (0,0,0)
# Local pivot is at left end: (-length/2 + w/2, 0)
cross_bottom_placed = (
    bar_cross_bottom
    .translate((link_cross_bottom_len/2 - bar_width/2, 0, 0)) # Shift pivot to origin
    .translate((0, 0, bar_thickness))                         # Offset in Z to stack
)

# Calculate the end point of the bottom cross bar to place the Mid Bar
# End point in X is roughly link_cross_bottom_len - bar_width (distance between hole centers)
# Since angle is 0, it's just translation in X.
dist_bottom_cross = link_cross_bottom_len - bar_width
pivot_mid_bar_lower = (dist_bottom_cross, 0, 0)

# Position 3: Mid Bar
# Connects to Bottom Cross Bar at its middle pivot (0,0) local
mid_bar_placed = (
    bar_mid
    # It seems the bottom cross bar connects to the MIDDLE of the right bar in the image structure?
    # Let's re-examine image.
    # Image: Left bar (long). Top cross bar connects middle of left to top of right.
    # Bottom cross bar connects bottom of left to middle of right.
    # Right bar extends down.
    
    # So for Mid Bar, the connection point is the middle hole (0,0,0) local.
    .rotate((0,0,0), (0,0,1), angle_mid)
    .translate(pivot_mid_bar_lower)
    .translate((0, 0, 0)) # Same Z level as bottom cross bar? Or sandwiched? 
                          # Image shows: Left Bar (Z=0), Bottom Cross (Z=1), Right Bar (Z=0).
                          # Let's put Right Bar back at Z=0 for symmetry with Left Bar.
)

# Position 4: Top Cross Bar
# Connects Middle of Left Bar to Top of Right Bar.
# Need to find coordinates of Middle of Left Bar.
# Center of rotation was bottom hole. Middle hole is distance (link_long_len/2 - bar_width/2) away along the vector.
dist_to_mid_left = link_long_len/2 - bar_width/2 
import math
rad_long = math.radians(angle_long)
pos_mid_left_x = dist_to_mid_left * math.cos(rad_long)
pos_mid_left_y = dist_to_mid_left * math.sin(rad_long)

cross_top_placed = (
    bar_cross_top
    .translate((link_cross_top_len/2 - bar_width/2, 0, 0)) # Shift pivot to origin
    # Rotate to match connection points. 
    # This is a kinematic loop, strictly speaking we need to calculate the exact angle.
    # Visually, let's approximate the angle downward.
    .rotate((0,0,0), (0,0,1), -20) 
    .translate((pos_mid_left_x, pos_mid_left_y, bar_thickness)) # Stack on top (Z=1)
)

# Note: In a static model without a solver, ensuring the 4th link perfectly aligns 
# with the holes of the others requires geometric calculation. 
# The visual approximation places the parts in the correct topology.

# Combine all parts
result = (
    long_bar_placed
    .union(cross_bottom_placed)
    .union(mid_bar_placed)
    .union(cross_top_placed)
)