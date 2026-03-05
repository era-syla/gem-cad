import cadquery as cq

# Dimensions
length = 90.0           # Total length of the part
width = 45.0            # Total width (widest section)
thickness = 5.0         # Thickness of the plate
narrow_width = 25.0     # Width of the narrower section
narrow_length = 30.0    # Length of the narrower section
fillet_radius = 5.0     # Radius for the corners

# Derived coordinates
# Coordinate system: Origin aligned roughly with bottom-left, 
# but constructed via specific points for the profile.
# Profile shape: A rectangle with a rectangular cutout on the front-left corner
# or a union of a wider rectangle and a narrower one.

# Points definition (Counter-Clockwise starting from Back-Left)
# Back edge is aligned with y = width
# Front edge of wide part is aligned with y = 0
# Front edge of narrow part is aligned with y = width - narrow_width

pts = [
    (0, width),                                     # Back-Left
    (0, width - narrow_width),                      # Front-Left
    (narrow_length, width - narrow_width),          # Inner Corner (re-entrant)
    (narrow_length, 0),                             # Step Outer Corner
    (length, 0),                                    # Front-Right
    (length, width)                                 # Back-Right
]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Apply fillets to vertical edges
# We select all vertical edges ("|Z") and then filter them.
# We want to fillet the 5 convex corners but leave the re-entrant (inner) corner sharp.
# The filter selects edges based on their position:
# - Edges at x ~ 0 (Left side)
# - Edges at x ~ length (Right side)
# - Edges at y ~ 0 (Front side of the wide part)
# This logic excludes the inner vertical edge located at (narrow_length, width - narrow_width).
result = result.edges("|Z").filter(lambda e: 
    e.Center().x < 0.1 or 
    e.Center().x > length - 0.1 or 
    e.Center().y < 0.1
).fillet(fillet_radius)