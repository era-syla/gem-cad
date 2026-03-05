import cadquery as cq

# Define parametric dimensions
total_length = 100.0
height_left = 20.0
height_right_tall = 60.0
thickness = 10.0
fillet_radius = 5.0
arc_radius = 15.0  # Radius of the dip
dip_center_x_ratio = 0.65 # Position of dip center relative to length

# Calculate derived points
start_point = (0, 0)
bottom_right = (total_length, 0)

# Build the 2D Sketch
# We will draw the profile and then extrude it.
# The shape consists of lines and arcs.
# Let's trace it counter-clockwise starting from bottom-left corner (0,0)

# Create the base sketch
result = (
    cq.Workplane("XY")
    .moveTo(0, height_left) # Start at top-left corner
    .lineTo(0, 0)           # Line down to origin
    .lineTo(total_length, 0) # Line across bottom
    .lineTo(total_length, height_right_tall) # Line up right side
    .lineTo(total_length - 10, height_right_tall) # Small top flat on right
    
    # Create the large curve/dip
    # We define a 3-point arc or use tangent arcs.
    # Looking at the image, there's a slope up from left, a dip, then a steep rise.
    # Let's try defining specific key points for a spline or a series of lines/arcs.
    # A simpler approach for this specific geometry is often constructive solid geometry (CSG) or a subtractive approach,
    # but a sketch is cleaner. Let's trace the top profile specifically.
    
    # Let's approximate the top profile:
    # 1. Slope from (0, height_left) to a peak before the dip.
    # 2. The dip itself.
    # 3. The rise to the right tower.
    
    # Revised strategy: Create a polygon and cut the circle out, then fillet.
    # It's robust and easier to parameterize.
)

# 1. Create the basic trapezoidal/angular shape
base_shape = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(total_length, 0)
    .lineTo(total_length, height_right_tall)
    .lineTo(total_length - 12, height_right_tall) # Top right width
    .lineTo(total_length - 15, height_right_tall * 0.6) # The inner vertical-ish slope
    .lineTo(total_length * 0.45, height_left + 10) # The long slope
    .lineTo(0, height_left)
    .close()
    .extrude(thickness)
)

# 2. Refine the shape to match the organic curve using a subtractive cylinder (the "dip")
# The dip looks like a circular cutout.
dip_center = (total_length * 0.6, height_left + 15)
dip_cutout = (
    cq.Workplane("XY")
    .workplane(offset=-1) # Start cut slightly below
    .moveTo(dip_center[0], dip_center[1])
    .circle(arc_radius)
    .extrude(thickness + 2)
)

# 3. Combine and Fillet
# The shape in the image is very smooth. Let's build a clean profile wire instead of boolean subtract
# to get that specific "swoop" look.

# Final Attempt with specific Polyline + Fillet strategy which is best for this 2D profile
pts = [
    (0, 0),
    (total_length, 0),
    (total_length, height_right_tall),
    (total_length - 12, height_right_tall), # Top right flat
    (total_length * 0.75, height_right_tall * 0.5), # Bottom of the "neck"
    (total_length * 0.5, height_left + 5), # Top of left ramp
    (0, height_left)
]

result = (
    cq.Workplane("XY")
    .moveTo(pts[0][0], pts[0][1])
    .lineTo(pts[1][0], pts[1][1])
    .lineTo(pts[2][0], pts[2][1])
    # Now the top profile. Let's use a 3-point arc for the dip for a smoother look
    .lineTo(pts[3][0], pts[3][1]) # Top of right tower
    
    # Create the swooping curve using a spline for organic feel or radius arcs
    .spline([pts[4], pts[5]], includeCurrent=True)
    
    .lineTo(pts[6][0], pts[6][1])
    .close()
    .extrude(thickness)
)

# The previous spline attempt might be too generic. Let's create the specific "dip" geometry using a cut.
# It creates the most predictable "U" shape seen in the image.

s = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(total_length, 0)
    .lineTo(total_length, height_right_tall)
    .lineTo(total_length - 15, height_right_tall) # Top right flat
    .lineTo(total_length - 20, 35) # Point before arc
    .radiusArc((45, 25), -25) # The dip (endpoint, radius) - negative radius for concave
    .lineTo(0, 20) # Back to start height
    .close()
    .extrude(thickness)
)

# Apply fillets to round all the sharp vertical edges as seen in the image
result = s.edges("|Z").fillet(4.0)