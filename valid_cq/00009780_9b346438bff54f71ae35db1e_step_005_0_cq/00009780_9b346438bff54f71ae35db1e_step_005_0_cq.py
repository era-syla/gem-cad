import cadquery as cq

# Parameters for the mustache shape
width = 100.0   # Total width of the mustache
height = 30.0   # Approximate height of one side
thickness = 10.0 # Extrusion depth

# We will construct one half of the mustache using spline points and mirror it.
# The shape is organic, so we define control points for the top and bottom curves.
# Coordinates are roughly relative to a center origin (0,0).

# Right side control points
# Starting from the center (0,0) and moving right
center_top = (0, 10) # Dip in the middle top
center_bottom = (0, 0) # Point in the middle bottom

# Top curve points (moving right)
p_top_1 = (10, 25) # High point of the lobe
p_top_2 = (25, 20) # Curving down
p_top_3 = (45, 10) # Towards the tip

# Bottom curve points (moving right from center bottom)
p_bot_1 = (10, 5)
p_bot_2 = (25, 10)
p_bot_3 = (45, 10) # Tip meets here

# Tip of the mustache
tip = (50, 15)

# Create the right half profile using splines
# We draw the outline: Center Bottom -> Tip -> Center Top -> Close
# Using spline for smooth organic curves

right_half = (
    cq.Workplane("XY")
    .moveTo(0, 0)  # Start at center bottom
    .spline([(15, 8), (35, 10), (50, 20)], includeCurrent=True) # Bottom curve to tip
    .spline([(35, 25), (15, 30), (0, 15)], includeCurrent=True) # Top curve back to center
    .close()
)

# Extrude the right half
right_solid = right_half.extrude(thickness)

# Mirror to create the left half and unite them
result = right_solid.union(right_solid.mirror("YZ"))

# Optional: Add fillets to smooth sharp edges if desired, 
# but the image shows fairly sharp edges on the extrusion profile itself.
# The profile itself is smooth due to splines.