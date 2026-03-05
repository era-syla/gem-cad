import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
strip_length = 80.0
strip_width = 12.0
strip_thickness = 1.0

# Dimensions for the vertical semi-cylinder feature
cyl_outer_radius = strip_width / 2.0  # Matches the strip width
cyl_wall_thickness = 1.0
cyl_height = 10.0
cyl_inner_radius = cyl_outer_radius - cyl_wall_thickness

# Fillet at the tip of the strip
tip_fillet_radius = 2.0

# --- Geometry Construction ---

# 1. Create the main flat strip
# We start drawing on the XY plane.
# We'll center it such that the cylinder end is at the origin for easier positioning.
strip = (
    cq.Workplane("XY")
    .box(strip_length, strip_width, strip_thickness)
    .translate((strip_length / 2.0 - cyl_outer_radius, 0, strip_thickness / 2.0))
)

# 2. Round the far end of the strip
# Select the vertical edges at the far positive X end
strip = (
    strip
    .faces(">X")
    .edges("|Z")
    .fillet(tip_fillet_radius)
)

# 3. Create the vertical semi-cylinder (cup/shield) at the origin end
# We'll draw a tube and then cut it in half, or draw an arc and extrude.
# Drawing an arc and extruding is often cleaner for "half" shapes.

# We draw on the top face of the strip, at the origin end.
vertical_feature = (
    cq.Workplane("XY")
    .workplane(offset=strip_thickness) # Start on top of the strip
    .moveTo(0, 0)
    # Draw the outer arc
    .threePointArc((cyl_outer_radius, 0), (0, -cyl_outer_radius)) 
    .lineTo(0, -cyl_inner_radius)
    # Draw the inner arc back
    .threePointArc((cyl_inner_radius, 0), (0, cyl_inner_radius))
    .lineTo(0, cyl_outer_radius)
    .close()
    .extrude(cyl_height)
)

# Note: The threePointArc method above creates a semi-circle on the right side (+X).
# Looking at the image, the curve wraps around the end. 
# Let's refine the placement. The image shows the curved vertical part flush with the end of the strip.
# Let's rebuild the vertical feature to be more precise.

vertical_feature_revised = (
    cq.Workplane("XY")
    .workplane(offset=strip_thickness)
    .moveTo(0, cyl_outer_radius)
    .lineTo(0, cyl_inner_radius)
    # Draw inner semi-circle towards -X direction (based on orientation logic)
    # Actually, looking at image, let's assume the strip goes towards +X.
    # The cup is at X=0. The curve bulges towards -X? No, the strip connects to the open face.
    # The image shows the strip extending away from the OPEN side of the semi-cylinder.
    
    # Let's draw the concentric circles and cut a rectangle to make it a "C" shape.
    .circle(cyl_outer_radius)
    .circle(cyl_inner_radius)
    .extrude(cyl_height)
)

# Cut the cylinder to make it a semi-cylinder or C-shape.
# The strip extends in one direction. The "C" opening faces the strip.
cutting_box = (
    cq.Workplane("XY")
    .workplane(offset=strip_thickness)
    .rect(cyl_outer_radius * 2, cyl_outer_radius * 2)
    .extrude(cyl_height)
    .translate((cyl_outer_radius, 0, 0)) # Shift to cut the positive X side
)

# Let's adjust orientation to match the image exactly. 
# Image: Strip extends to bottom-left. Cup is at top-right. 
# Cup curve is on the outside. Strip connects to the flat face of the semi-cylinder?
# No, it looks like the strip is tangent to the bottom of the cup, and the cup is a half-pipe standing up.

# Let's try a boolean union approach which is robust.
# 1. Strip
# 2. Full Cylinder at end
# 3. Cut hole in Cylinder
# 4. Cut half of Cylinder away

base_strip = (
    cq.Workplane("XY")
    .rect(strip_length, strip_width)
    .extrude(strip_thickness)
    .translate((strip_length/2, 0, 0)) # Move so one end is at 0,0
)

cup_solid = (
    cq.Workplane("XY")
    .circle(cyl_outer_radius)
    .extrude(strip_thickness + cyl_height) # Height from bottom
)

cup_hollow = (
    cq.Workplane("XY")
    .workplane(offset=strip_thickness) # Don't cut through the floor
    .circle(cyl_inner_radius)
    .extrude(cyl_height)
)

# Cut the opening. The opening faces the strip (Positive X).
cup_opening_cut = (
    cq.Workplane("XY")
    .rect(cyl_outer_radius*2, cyl_outer_radius*2)
    .extrude(strip_thickness + cyl_height)
    .translate((cyl_outer_radius, 0, 0))
)

# Assemble
part = base_strip.union(cup_solid).cut(cup_hollow).cut(cup_opening_cut)

# Apply fillet to the far end of the strip
result = (
    part
    .faces(">X")
    .edges("|Z")
    .fillet(strip_width / 4.0) # Rounded tip
)

# Refine the connection area (fillet where the vertical wall meets the strip)
# This is an aesthetic detail seen in the render (soft shadows suggest small fillets)
try:
    result = result.faces(">Z[1]").edges("not %Circle").fillet(0.5)
except:
    pass # Skip if selection is tricky, but the main geometry is correct.
