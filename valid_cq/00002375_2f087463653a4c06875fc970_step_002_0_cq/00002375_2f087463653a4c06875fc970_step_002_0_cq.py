import cadquery as cq

# Parametric dimensions
length = 60.0    # Length of the block
width = 30.0     # Width of the block
height = 15.0    # Total height at the center
radius = 40.0    # Radius of the top curvature (larger radius = flatter curve)

# Create the profile
# We will create a sketch on the front plane (XZ) and extrude it
# The profile consists of a flat bottom, vertical sides, and an arc on top.

# Calculate the sagitta (height of the arc) to position the center point correctly
# or use a 3-point arc approach.
# A simpler approach in CadQuery is to make a block and intersect it with a cylinder 
# or use a sketch with an arc.

# Let's use a Sketch-based approach which is very clean.
# We'll draw the cross-section on the YZ plane (width x height) and extrude along X.

result = (
    cq.Workplane("YZ")
    .moveTo(-width / 2, 0)
    .lineTo(width / 2, 0)       # Bottom edge
    .lineTo(width / 2, height - 2) # Right vertical edge (a bit shorter to allow for arc)
    .radiusArc((-width / 2, height - 2), radius) # Top curved edge
    .close()
    .extrude(length)
)

# Re-centering the object if desired, or just leaving it as is.
# The current extrusion goes from Z=0 in the positive X direction (relative to YZ plane)
# Let's center it for better practice.
result = result.translate((-length / 2, 0, 0))

# Looking at the image again, the corners are also rounded/filleted along the length?
# No, the image shows a consistent profile extruded. The top "corners" in the cross-section
# are rounded.
# Let's refine the sketch logic. It looks like a rectangle with the top side replaced by an arc.
# But wait, looking at the corners where the top face meets the side face...
# It looks like a fillet.
# Let's try a simpler approach: A box with the top edges filleted?
# If I fillet the top two long edges of a box, I get a flat top with rounded sides.
# The image shows a continuous curve across the top face.

# Let's stick to the "Extruded Profile" method.
# Profile: 
#  (0,0) -> (width, 0) -> (width, side_height) -> ARC -> (0, side_height) -> close
# The arc goes from (width, side_height) to (0, side_height).
# The "top" of the arc is at 'height'.

# Let's define side_height based on the arc radius and total height.
# Or, more simply, use a 3-point arc: start, end, and a point on the arc (top center).

# Revised Dimensions
L = 60.0
W = 30.0
H_center = 15.0
H_side = 10.0  # Height at the vertical sides

result = (
    cq.Workplane("YZ")
    .moveTo(-W/2, 0)
    .lineTo(W/2, 0)          # Bottom
    .lineTo(W/2, H_side)     # Right side
    .threePointArc((0, H_center), (-W/2, H_side)) # Top arc passing through center peak
    .close()
    .extrude(L)
)

# The extrusion happens along X. Let's center it.
result = result.translate((-L/2, 0, 0))

# Looking at the specific shading in the image, there is a distinct "fillet" look 
# where the top curve meets the vertical side. 
# It might actually be a flat top block with very large fillets, 
# or a "crowned" top. The provided image shows a continuous curve.
# However, there is a faint line or change in shading that suggests a fillet.
# Let's look closer. The top surface looks slightly curved (cambered).
# The transition from the top surface to the vertical side is sharp in the geometry 
# but rendered smooth? No, there's a distinct edge line.
# If I look at the end cap, the top profile is a single arc.
# The line seen running along the length is the edge where the vertical face meets the curved top face.
# So the previous code block is the most accurate interpretation.

# Let's refine the parameters to match proportions.
# Width looks to be about half the length.
# Height looks to be about half the width.
# The curve is gentle.

L = 50.0
W = 30.0
H_total = 12.0
H_side = 8.0

result = (
    cq.Workplane("YZ")
    .moveTo(W/2, 0)
    .lineTo(-W/2, 0)
    .lineTo(-W/2, H_side)
    .threePointArc((0, H_total), (W/2, H_side))
    .close()
    .extrude(L)
    .translate((-L/2, 0, 0)) # Center the extrusion
)

# Rotate to match the isometric view orientation (Z-up) usually preferred
result = result.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -90)
# Wait, standard YZ plane extrusion puts X as the long axis. 
# Usually "result" is just returned without specific orientation unless requested.
# I will output the clean generation script.

# Final check of the geometry:
# 1. Rectangle base on YZ plane.
# 2. Top edge replaced by an arc.
# 3. Extruded.

# Alternative interpretation:
# Is it a block with the top two edges filleted so much they almost meet?
# If they met, there would be a sharp spine or it would be a cylinder segment.
# The image shows a flat-ish curve.
# The 3-point arc profile is the robust way to model this.

# Let's reset the orientation logic to standard CadQuery "Workplane('XY')" base for logical consistency.
# Base on XY, extrude Z? No, the profile is the cross-section.
# Profile on XZ, extrude Y.
# Let's do that.

# Final Logic:
# 1. Sketch on XZ plane.
# 2. Rectangle points: (-w/2, 0) to (w/2, h_side).
# 3. Top is an arc from (w/2, h_side) to (-w/2, h_side) passing through (0, h_top).
# 4. Extrude along Y.

length = 60.0
width = 30.0
height_side = 10.0
height_center = 14.0

result = (
    cq.Workplane("XZ")
    .moveTo(width/2, 0)
    .lineTo(-width/2, 0)
    .lineTo(-width/2, height_side)
    .threePointArc((0, height_center), (width/2, height_side))
    .close()
    .extrude(length/2, both=True) # Extrude symmetrically along Y
)

# This produces the exact shape: a block with a crowned top surface.