import cadquery as cq

# Define parametric dimensions
L = 60.0    # Length of each leg
T = 12.0    # Thickness of the bracket
H = 70.0    # Height of the bracket

# Coordinates for the L-bracket profile in the XY plane
# The outer corner is at (L, 0)
# Front leg extends from X=0 to X=L along Y=0
# Side leg extends from Y=0 to Y=L along X=L
pts = [
    (0, 0),
    (L, 0),
    (L, L),
    (L - T, L),
    (L - T, T),
    (0, T)
]

# Create the base solid by extruding the L-profile
result = cq.Workplane("XY").polyline(pts).close().extrude(H)

# Add countersunk holes to the front face (which points in the -Y direction)
# The face bounds are X from 0 to L. The "clear" region before the inner wall is X from 0 to L-T.
# We center the hole pattern within this clear region.
# The default workplane origin on this face is its bounding box center (L/2, H/2).
# We offset the local X coordinate to perfectly center the holes in the clear region.
center_x_local = -T / 2.0 

# Define the spacing for the 2x2 hole pattern
spacing_x = 24.0
spacing_z = 40.0

hole_pts = [
    (center_x_local - spacing_x/2, -spacing_z/2),
    (center_x_local + spacing_x/2, -spacing_z/2),
    (center_x_local - spacing_x/2,  spacing_z/2),
    (center_x_local + spacing_x/2,  spacing_z/2)
]

# Apply the countersunk holes
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints(hole_pts)
    .cskHole(diameter=6.0, cskDiameter=12.0, cskAngle=90.0)
)