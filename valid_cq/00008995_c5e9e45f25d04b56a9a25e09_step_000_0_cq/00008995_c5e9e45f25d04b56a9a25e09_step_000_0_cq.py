import cadquery as cq

# Parametric dimensions
width = 50.0       # Width of the block (the straight side dimension)
length = 50.0      # Length of the block (the dimension with curved sides)
height = 15.0      # Thickness of the block
bulge_radius = 40.0 # Radius of the curved sides (must be > height/2)

# Create the profile on the side face
# We will draw a profile on the XZ plane and extrude it along Y
# The profile is a rectangle with two curved vertical sides
# Or simpler: Draw the profile on the YZ plane (the cross-section of the bulge) and extrude.
# Let's try creating a sketch on the front plane (XZ), representing the side with the curve.

# Method: Create a sketch of the cross-section with the curved sides and extrude it.
# Looking at the object, let's assume the 'length' direction has the straight edges and 'width' has the curves.
# Actually, looking at the isometric view:
# Top face is a rectangle.
# Two opposing side faces are flat.
# Two opposing side faces are convex curves (cylindrical sections).

# Let's construct it by sketching the cross-section that has the curves.
# This cross-section appears on the face perpendicular to the straight sides.
# Let's say the straight sides run along the Y axis. Then the cross-section is on the XZ plane.
# The cross-section is a rectangle where the vertical sides are replaced by arcs.

# Wait, looking closer:
# The top face is flat. The bottom face is flat.
# The front-left face is curved outwards.
# The back-right face is likely curved outwards too (symmetric).
# The other two vertical faces (front-right and back-left) are flat.

# So, the cross section along one axis is a rectangle.
# The cross section along the other axis is a shape with flat top/bottom and curved sides.

# Let's model this profile on the YZ plane (Side view):
# Height is 'height'. Depth is 'length'.
# The vertical lines (sides of the block in this view) are arcs.
# Top and bottom are straight lines.

# Actually, the simplest way is to extrude a shape that has two straight lines (top/bottom) and two arcs (sides).
# Let's define this sketch on the YZ plane.
# Y corresponds to the length/width dimension. Z corresponds to height.
# The extrusion will be along the X axis.

# Sketch construction:
# 1. Start at (-length/2, height/2)
# 2. Line to (length/2, height/2)  -- Top edge
# 3. ThreePointArc to (length/2, -height/2) via a point further out in Y -- Right curved edge
# 4. Line to (-length/2, -height/2) -- Bottom edge
# 5. ThreePointArc to (-length/2, height/2) via a point further out in -Y -- Left curved edge

# Let's refine the parameters.
# Length: Distance between the chords of the arcs.
# Height: Distance between top and flat bottom faces.
# Radius: The curvature of the side faces.

def create_curved_block(length, width, height, radius):
    # Check to ensure radius is valid for the given height
    # The sagitta (bulge depth) is determined by radius and height chord
    # Chord length is 'height' in the vertical orientation of the side face profile?
    # No, the curve is along the vertical face. The curve connects the top edge to the bottom edge.
    # Looking at the image, the curve is on the vertical face. The profile of that face is an arc.
    # This means the cross-section perpendicular to the straight sides is bounded by two vertical arcs and two horizontal lines.
    
    # Let's draw on the XZ plane.
    # X direction: width
    # Z direction: height
    # We want top and bottom to be flat (horizontal lines).
    # We want left and right sides to be convex arcs.
    
    # Calculate the x-coordinate of the arc center or intermediate point
    # We'll use a specific radius approach or a bulge amount.
    # Let's stick to a 3-point arc approach for clarity.
    
    # Define points for the profile
    x_half = width / 2.0
    z_half = height / 2.0
    
    # Calculate the bulge offset (sagitta) based on radius and chord (height)
    # Chord = height
    # R = radius
    # sagitta s = R - sqrt(R^2 - (chord/2)^2)
    # This assumes the arc center is horizontally aligned with the midpoint of the side.
    if radius <= height/2:
        raise ValueError("Radius must be greater than half the height to create a valid convex arc.")
        
    s = radius - (radius**2 - (height/2.0)**2)**0.5
    
    # Create the sketch
    # We draw on YZ plane to extrude along X (or XZ to extrude along Y). Let's do XZ plane, extrude Y.
    # Profile shape:
    # Top line: (-x_half, z_half) to (x_half, z_half) - Wait, top is flat?
    # No, looking at the image:
    # The TOP surface is flat.
    # The SIDE surface bulges.
    # This means the profile on the side face (let's say XZ plane) has a curved edge.
    # But if the side face bulges, the top edge is a straight line, and the bottom edge is a straight line.
    # The curve connects top and bottom? That would make the top/bottom faces curved if extruded perpendicular.
    # Let's re-examine the image.
    
    # Image analysis 2:
    # The object looks like a pillow or a cushion shape cut from a rectangular block.
    # The vertical edge (corner) is a sharp line.
    # The face between two vertical corners is curved.
    # The top face is flat.
    # The bottom face is flat.
    # This implies the cross-section parallel to the top face (horizontal cut) is a shape with two straight sides and two curved sides.
    # Let's assume the curve is on the horizontal plane (XY).
    # If the curve is on the XY plane, then when we extrude up (Z), the vertical faces become curved surfaces.
    # The top and bottom faces are just caps of this extrusion.
    
    # Let's check the shading.
    # The side facing us (left) is dark. It has a curved horizon.
    # The vertical edge is straight.
    # The top edge of the side face is curved.
    # If the vertical edge is straight and the top edge is curved, then the top face is NOT a rectangle.
    # If the top face is flat, and its boundary is curved, then the extrusion is along Z, based on a 2D profile in XY.
    
    # VERDICT: The object is an extrusion of a 2D shape with two straight edges and two curved edges.
    # The extrusion creates the thickness (height).
    
    # Construction:
    # Plane: XY
    # Shape: Two horizontal lines (straight) and two vertical curves (arcs).
    # Extrude: Along Z.
    
    l_half = length / 2.0
    w_half = width / 2.0
    
    # We need an arc for the side.
    # Let's assume the "width" sides are the curved ones.
    # Points:
    # Top-Left: (-w_half, l_half)
    # Top-Right: (w_half, l_half)
    # Bottom-Right: (w_half, -l_half)
    # Bottom-Left: (-w_half, -l_half)
    
    # If the "width" sides (left/right in sketch) are curved:
    # Start at Top-Left
    # Line to Top-Right (Flat top edge in sketch)
    # Arc to Bottom-Right (Curved right edge) - bulging out +X
    # Line to Bottom-Left (Flat bottom edge in sketch)
    # Arc to Top-Left (Curved left edge) - bulging out -X
    
    # Sagitta calculation for the arc point
    # Chord length = length (Y dimension)
    chord = length
    s = radius - (radius**2 - (chord/2.0)**2)**0.5
    
    # Midpoints for arcs
    right_mid = (w_half + s, 0)
    left_mid = (-w_half - s, 0)

    # Let's build it
    s = cq.Workplane("XY") \
        .moveTo(-w_half, l_half) \
        .lineTo(w_half, l_half) \
        .threePointArc(right_mid, (w_half, -l_half)) \
        .lineTo(-w_half, -l_half) \
        .threePointArc(left_mid, (-w_half, l_half)) \
        .close() \
        .extrude(height)
        
    return s

# Dimensions estimated from visual proportions
# It looks roughly square in footprint, maybe slightly rectangular.
# Thickness is maybe 1/3 or 1/4 of the width.
L = 60.0
W = 60.0
H = 20.0
R = 70.0 # Radius large enough for a gentle curve

# Wait, looking at the image again very carefully.
# The visible vertical edge in the front center.
# The face to the right of it is curved.
# The face to the left of it is curved.
# If BOTH visible vertical faces are curved, then all 4 sides are curved?
# No, the prompt text usually implies a simpler geometry or the image shows specific features.
# Let's look at the corners.
# The corner pointing at us is sharp (intersection of two faces).
# The top edge of the left face looks straight.
# The top edge of the right face looks curved.
# This contradicts the "extrusion of a 2D shape with 2 straight/2 curved edges" theory if the orientation is standard isometric.

# Alternative interpretation:
# Maybe the CURVE is on the vertical profile?
# If the curve is vertical (barrel distortion):
# - The top face is a rectangle.
# - The side faces bulge outwards.
# - The vertical edges would be curved.
# In the image, the vertical edge connecting the near corner seems straight.
# If the vertical edge is straight, the horizontal cross-sections are constant.
# Therefore, it is a linear extrusion.
# The profile being extruded must be the top face shape.
# Looking at the top face:
# The edge on the right looks like an arc.
# The edge on the left looks like a straight line.
# This suggests the shape has two opposing straight sides and two opposing curved sides.
# The standard "cushion" shape.

# Let's assume:
# - Extrusion along Z axis.
# - Sketch on XY plane.
# - Sketch has 2 straight lines and 2 arcs.
# - Based on the image orientation:
#   - The face on the left is flat (straight top edge).
#   - The face on the right is curved (curved top edge).
#   - Therefore, the front-left face is flat, front-right face is curved.
#   - By symmetry usually implied in such CAD exercises, Back-left is curved, Back-right is flat.
#   - Result: A shape with alternating flat/curved sides? Or parallel pairs?
#   - Usually parallel pairs.
#   - Pair 1: Flat. Pair 2: Curved.

# Let's implement the parallel pairs (2 straight, 2 curved).
# L = 60 (Straight side length), W = 60 (Chord of curved side).
# But in the code logic above, L was the chord. Let's align variables.

# Final Plan:
# Create a 2D sketch on XY plane.
# Two parallel straight lines.
# Two convex arcs connecting them.
# Extrude in Z.

result = create_curved_block(L, W, H, R)