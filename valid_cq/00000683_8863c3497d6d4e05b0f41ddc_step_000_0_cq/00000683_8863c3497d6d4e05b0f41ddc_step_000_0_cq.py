import cadquery as cq

# Parametric dimensions
# Overall dimensions
L_base = 100.0  # Length of the base
H_overall = 120.0 # Total height
W_overall = 40.0 # Width (thickness) of the part

# L-shape parameters
H_base_front = 40.0 # Height of the front vertical section
L_top_back = 40.0   # Length (depth) of the top section

# Feature parameters
fillet_radius = 5.0 # Radius for the outer edges

# Create the base profile sketch
# We will draw the side profile (an L-shape with a slope) and extrude it
# The profile looks like a polygon defined by points (0,0), (L,0), (L,H), (L-L_top, H), ...

# Define points for the polygon (counter-clockwise starting from origin)
# Origin is bottom-left corner of the side profile
pts = [
    (0, 0),                           # Bottom-left
    (L_base, 0),                      # Bottom-right
    (L_base, H_overall),              # Top-right
    (L_base - L_top_back, H_overall), # Top-left inner corner
    (0, H_base_front)                 # Slope connects back to this point
]

# Create the solid block
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(W_overall)
)

# Apply fillets
# Looking at the image, there's a continuous fillet running along the outer "spine" edge
# specifically on the face that corresponds to the angled profile.
# It seems the fillet is applied to the edges formed by the extrusion profile on one side.
# Or possibly all external vertical edges. Let's look closer.
# The image shows rounding on the top-right vertical edge, the top horizontal edge, 
# the sloped edge, and the front vertical edge. Essentially the entire 'upper' perimeter on one side.

# Let's select the edges on the +Z face (the face defined by the profile shape if extruded in Z)
# However, the code above extrudes in Z. So the profile is on XY plane (bottom) and offset XY plane (top).
# Wait, standard orientation usually puts "UP" as Z. 
# Let's re-orient for clarity. Let's make the profile on YZ plane and extrude in X.
# This makes "Up" Z and "Right" Y.

result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(W_overall)
)

# Now, we want to fillet the edges on the "front" face (the one at X=W_overall).
# Based on the shading, the fillet runs along the top, slope, and front vertical edge.
# It also wraps around the corner.

# Let's identify the edges.
# The edges to fillet are on the face with normal (1, 0, 0)
# We want the perimeter edges of that face, excluding the bottom edge and the back edge?
# Looking closely at the image:
# The vertical back edge is filleted.
# The top horizontal edge is filleted.
# The sloped edge is filleted.
# The front vertical edge is filleted.
# The bottom edge is NOT filleted.

# So we want to select the edges on the extruded face (X max) and fillet them,
# except the bottom one.

result = (
    result
    .faces(">X") # Select the front face
    .edges()     # Get all edges of that face
    .fillet(fillet_radius)
)

# Wait, looking very closely at the bottom corner of the image, the bottom edge is sharp.
# The previous step filleted ALL edges of the >X face.
# Let's restrict the selection.
# Select >X face edges, then exclude the one with center Z approx 0.

result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(W_overall)
)

# We need a more robust edge selection.
# Edges on the positive X face.
# We want to exclude the bottom edge (min Z) and potentially the back edge (max Y) if it's sharp.
# But in the image, the back edge (the tall vertical one) IS rounded.
# The bottom edge looks sharp.
# So, filter edges on face >X, exclude the one that is at Z=0.

edges_to_fillet = (
    result
    .faces(">X")
    .edges("not <Z") # Select edges on the face, excluding the bottom-most one
)

result = edges_to_fillet.fillet(fillet_radius)