import cadquery as cq

# --- Parameters ---
outer_radius = 50.0
ring_thickness = 5.0
height = 5.0
text_height = height  # Make text flush with the ring

# --- Geometry Construction ---

# 1. Create the Outer Ring
outer_ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - ring_thickness)
    .extrude(height)
)

# 2. Create the Central Stylized "7" / Shape
# This shape is somewhat abstract, roughly like a lightning bolt or a '7'
# We will define points to sketch it.
path_points = [
    (-10, 40), # Top left point connecting to ring (approx)
    (5, 45),   # Top point
    (20, 0),   # Middle kink
    (40, -10), # Bottom right extension
    (30, -20), # Bottom tip
    (10, -5),  # Inner corner
    (-5, 10),  # Midsection inner
    (-15, 30), # Back up
]
# Refined shape approximation based on the central "7" structure
# Let's break it down into segments for easier control
central_shape = (
    cq.Workplane("XY")
    .moveTo(-10, 35) # Start near top left
    .lineTo(10, 35)  # Top horizontal bar
    .lineTo(25, -20) # Diagonal down to bottom right
    .lineTo(45, -15) # Short extension right
    .lineTo(45, -25) # Down
    .lineTo(15, -35) # Bottom tip
    .lineTo(-5, 20)  # Diagonal up
    .lineTo(-20, 25) # Curved part start
    .close()
    .extrude(height)
)

# 3. Add the "Ex" text on the left
# The font looks sans-serif, bold.
text_ex = (
    cq.Workplane("XY")
    .text("Ex", fontsize=35, distance=height, font="Arial", halign="center", valign="center")
    .translate((-25, -10, 0)) # Position it to the left
)

# 4. Add the "p" text on the right
# The 'p' is connected to the ring on the right side.
text_p = (
    cq.Workplane("XY")
    .text("p", fontsize=35, distance=height, font="Arial", halign="center", valign="center")
    .translate((35, 15, 0)) # Position it to the right
)

# 5. Add the smaller "End" text
# It looks like "End" or similar small text near the "E" of "Ex"
text_small = (
    cq.Workplane("XY")
    .text("End", fontsize=12, distance=height, font="Arial", halign="center", valign="center")
    .rotate((0,0,0), (0,0,1), 30) # Slight rotation
    .translate((-35, 5, 0))
)

# --- Combine All Parts ---

# Since the prompt asks for a specific complex logo which is likely an artistic SVG extrusion,
# reproducing exact font curves and custom paths is an approximation.
# A more robust approach for the central "7" is needed to match the visual weight.

# Let's rebuild the central shape with a more "logo-like" constructed geometry
# Looking closely, it looks like:
# - A big diagonal bar
# - A top horizontal bar (part of a 7)
# - The 'p' and 'Ex' connect to it.

final_logo = outer_ring.union(text_ex).union(text_p).union(text_small)

# Create a custom shape for the central "7" element to better match image
s7 = (
    cq.Workplane("XY")
    .moveTo(-5, 45) # Top connection to ring
    .lineTo(10, 45)
    .lineTo(15, 10) # Neck
    .lineTo(40, -10) # Leg out
    .lineTo(35, -20) # Leg tip
    .lineTo(5, 5)   # Inner crotch
    .lineTo(-15, 35) # Back up
    .close()
    .extrude(height)
)

result = final_logo.union(s7)

# To ensure everything is a single solid and connected
result = result.clean()