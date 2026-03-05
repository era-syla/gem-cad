import cadquery as cq

# Parametric dimensions
length = 100.0  # Total length of the part
height = 20.0   # Height at the taller end
thickness = 15.0 # Extrusion thickness
radius_large = 200.0 # Radius for the curved back
radius_small = 10.0 # Radius for the rounded tip

# Create the sketch and extrude
# The shape resembles a blade or airfoil section. 
# We'll construct it using a line for the flat face, and a large arc for the curved face,
# connecting at a sharp point on one end and a blunt/rounded end on the other.

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)          # The straight bottom edge
    .lineTo(length, height * 0.4) # A small straight segment at the tip
    .threePointArc((length/2, height), (0, height)) # The curved top edge
    .close()
    .extrude(thickness)
)

# Refine the shape to match the image more closely
# The image shows a sharp trailing edge on the left and a rounded leading edge on the right
# Let's rebuild the sketch with this specific geometry in mind.

# New approach:
# 1. Start at origin (bottom-left sharp corner)
# 2. Draw line to right (bottom edge)
# 3. Draw vertical line up (nose height)
# 4. Draw arc back to start (top curve)

length = 80.0
height_start = 20.0  # Height at the "thick" left side
height_end = 8.0     # Height at the "thin" right side
width = 10.0         # Depth of extrusion

# Based on the visual, it looks like a loft or a simple extrusion of a 2D profile.
# The profile is:
# - A vertical line on the left.
# - A long curved line on the top.
# - A long curved line on the bottom.
# - A small vertical line on the right.

# Let's try a simpler interpretation: 
# It looks like a segment of a ring or a wedge with curved sides.
# Let's assume a simpler "knife" shape: flat bottom, vertical back, curved top.

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(100, 0)                 # Bottom edge
    .lineTo(100, 15)                # Right vertical edge (blunt tip)
    .threePointArc((50, 25), (0, 30)) # Top curved edge creating the taper
    .close()
    .extrude(15)                    # Thickness
)

# Re-evaluating the image:
# The shape is essentially a wedge.
# Left side: Sharp edge (looks like a height of ~20-30).
# Right side: Appears to taper down significantly, maybe to a point or small edge.
# The top face is curved. The side facing us is curved.
# Actually, looking at the shading, the side facing us (the long face) is concave or convex? 
# No, it looks like a standard flat extrusion of a curved profile.

# Let's go with a specific geometric construction that creates this specific "scimitar" or blade-like wedge.

L = 100.0
H_back = 25.0
H_front = 10.0
Thickness = 12.0

# Construction points
p0 = (0, 0)
p1 = (L, 0)
p2 = (L, H_front)
p3 = (0, H_back)

# Control point for the top curve (concave slightly)
p_curve_top = (L/2, (H_back + H_front)/2 - 5) 

# Control point for bottom curve (convex)
p_curve_bottom = (L/2, -15)

# Wait, looking at the crop, it's simpler.
# It is a solid block.
# Left face: Tall rectangle.
# Right face: Short rectangle.
# Top face: Curved surface connecting them.
# Bottom face: Curved surface connecting them.
# Front face: Flat.
# Back face: Flat.

# Actually, the most likely geometry given typical CAD primitive exercises is an extrusion of a 2D shape on the XY plane.
# The shape on the XY plane:
# Point 1: (0,0)
# Point 2: (L, 0) 
# Point 3: (L, thickness)
# Point 4: (0, thickness)
# That's just a rectangle.

# Let's look at it "Edge on".
# The visible face is the side of the extrusion.
# The profile is:
# Start at (0,0).
# Go to (Length, 0).
# Go UP to (Length, Tip_Height).
# Arc back to (0, Back_Height).
# Close.

# Let's refine dimensions based on the visual proportions.
length_dim = 120.0
back_height = 30.0
tip_height = 10.0
extrusion_depth = 20.0

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length_dim, 0)                           # Bottom straight edge
    .lineTo(length_dim, tip_height)                  # Small vertical tip
    # Create a gentle curve for the top edge. 
    # Using a 3-point arc. Midpoint is slightly lower than a straight line to give that "swoop" look?
    # No, the image shows a convex top edge (bulges out).
    .threePointArc((length_dim/2, (back_height + tip_height)/2 + 5), (0, back_height)) 
    .close()
    .extrude(extrusion_depth)
)

# Rotate to match image orientation roughly (standing up)
result = result.rotate((0,0,0), (1,0,0), -90)